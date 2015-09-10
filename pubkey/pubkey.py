#!/usr/local/bin/python3 -u
__author__ = 'Oliver Ratzesberger <https://github.com/fxstein>'
__copyright__ = 'Copyright (C) 2015 Oliver Ratzesberger'
__license__ = 'Apache License, Version 2.0'

import os
import json
import socket
import configparser
import asyncio
from aiohttp import web

from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController  # , expose
from cement.core import hook
from cement.core.exc import CaughtSignal
from cement.ext.ext_colorlog import ColorLogHandler
from cement.ext.ext_configparser import ConfigParserConfigHandler

VERSION = '0.9.0'

BANNER = """
pubkey v%s
Copyright (c) 2015 Oliver Ratzesberger
""" % VERSION

CMD = """
curl -s -S %s:%s >> ~/.ssh/authorized_keys
"""

DEFAULT_KEYFILE = """~/.ssh/id_rsa.pub"""
DEFAULT_HOST = """localhost"""
DEFAULT_PORT = 1080

DESCRIPTION = """
pubkey - Public Key distribution made easy.

Ever needed to quickly setup trusted keys for password less ssh sessions?
pubkey helps by making public keys avaialble on the local network with a
simple REST interface and a matching command to append the public key to
various machines on the same network.

Simply start pubkey on the source of the public key. Then head over to your
remote target and run:

%s

on the various hosts that require the key to be added to their trusted keys.
Done.
""" % CMD % ('host', 'port')

EPILOG = """

Report bugs, submit feature requests, and/or contribute code over at:
https://github.com/fxstein/pubkey\n
"""

HELP_AUTO = """
Auto detect IP address to bind REST server to.
"""
HELP_HOST = """
IP address to bind REST server to. Default is <%s> and
therefore NOT visible on the network.
"""
HELP_KEYFILE = """
Keyfile of public key. Commonly %s
Only public key filenames [.pub] allowed.
"""
HELP_PORT = """
Port to be used by REST server. Default is %s.
"""

# Default settings
from cement.utils.misc import init_defaults

defaults = init_defaults('pubkey', 'pubkey')
defaults['pubkey']['keyfile'] = DEFAULT_KEYFILE
defaults['pubkey']['host'] = DEFAULT_HOST
defaults['pubkey']['port'] = DEFAULT_PORT
defaults['pubkey']['auto'] = False


class PubKeyConfigHandler(ConfigParserConfigHandler):
    class Meta:
        label = 'config_handler'

    def get(self, *args, **kw):
        try:
            return super(PubKeyConfigHandler, self).get(*args, **kw)
        except configparser.Error as e:
            self.app.log.fatal('Missing configuration setting: %s' % e)
            self.app.close(1)


class PubKeyBaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = DESCRIPTION
        epilog = EPILOG
        arguments = [
            (['-a', '--auto'],
             dict(action='store_true', help=HELP_AUTO, dest='auto')),
            (['--host'],
             dict(action='store', help=HELP_HOST % DEFAULT_HOST, dest='host')),
            (['--key'],
             dict(action='store', help=HELP_KEYFILE % DEFAULT_KEYFILE,
             dest='keyfile')),
            (['--port'],
             dict(action='store', help=HELP_PORT % DEFAULT_PORT, dest='port')),
            (['-v', '--version'], dict(action='version', version=BANNER)),
            ]

    # @expose(hide=True)
    # def default(self):
    #     self.app.log.debug('running PubKeyBaseController.default()')


COLORS = {
    'DEBUG':    'cyan',
    'INFO':     'green',
    'WARNING':  'yellow',
    'ERROR':    'red',
    'CRITICAL': 'white,bg_red',
}


class PubKeyApp(CementApp):
    class Meta:
        label = 'pubkey'
        config_defaults = defaults

        base_controller = 'base'
        config_handler = 'config_handler'
        handlers = [PubKeyBaseController, PubKeyConfigHandler]

        extensions = ['colorlog']
        arguments_override_config = True

        log_handler = ColorLogHandler(colors=COLORS)

    def setup(self):
        # always run core setup first
        super(PubKeyApp, self).setup()

        self.log.debug('running setup()')

        self._loop = asyncio.get_event_loop()

        hook.register('post_argument_parsing', self._post_argument_parsing)
        hook.register('pre_close', self._pre_close)

    def _post_argument_parsing(self, app):
        self.log.debug('running _post_argument_parsing()')

        self._keyfile = os.path.expanduser(self.config.get(
            'pubkey', 'keyfile')).strip()

        self._loop.run_until_complete(self._init(self._loop))

    def _pre_close(self, app):
        self.log.debug('running _pre_close()')
        self._loop.run_until_complete(self._finish())

    @asyncio.coroutine
    def _init(self, loop):
        self.log.debug('running _init()')

        # First we check if this is a pubkey. Wont proceed if it is not
        if self._keyfile[::-1].find('.pub'[::-1]) is not 0:
            self.log.fatal("Keyfile is not a public key. Sorry won't continue.")
            self.log.fatal("Keyfile does not end in .pub: %s" % self._keyfile)
            exit(2)

        # Next read in pubkey and fail if needed
        try:
            with open(self._keyfile, 'rt') as file:
                self._pubkey = file.read()
        except Exception as e:
            self.log.fatal("Unable to read pubkey file: %s" % self._keyfile)
            self.log.fatal(e)
            exit(3)

        self.log.info('pubkey file used: %s' % self._keyfile)
        self.log.debug('pubkey:\n%s' % self._pubkey)

        host = self.config.get('pubkey', 'host')
        port = self.config.get('pubkey', 'port')

        # If auto flag is set, attempt to determine local host ip
        if self.config.get('pubkey', 'auto') is True:
            host = ([(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close())
                    for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]]
                    [0][1])

        self._webapp = web.Application(loop=loop, logger=None)

        # Handle incoming events
        self._webapp.router.add_route('GET', '/', self.get_pubkey)
        self._webapp.router.add_route('GET', '/json', self.get_pubkeyjson)

        self._webapp_handler = self._webapp.make_handler()

        try:
            self._webapp_srv = yield from self._loop.create_server(
                self._webapp_handler, host, port)

            self.log.info("pubkey server started at http://%s:%s" %
                          (host, port))

        except Exception as e:
            self.log.fatal("Error starting pubkey at http://%s:%s" %
                           (host, port))
            self.log.fatal(e)
            self._loop.stop()

        if host in ['localhost', '127.0.0.1']:
            self.log.warn('%s not reachable outside local host.' % host)
            self.log.warn('Provide valid ip or hostname or use --auto')

        print('Remote host command: \n%s' % CMD % (host, port))

    @asyncio.coroutine
    def _finish(self):
        self.log.debug('running _finish()')

        yield from asyncio.sleep(0.1)

        if hasattr(self, '_webapp_srv'):
            self._webapp_srv.close()
            yield from self._webapp_handler.finish_connections()
            yield from self._webapp_srv.wait_closed()

    def run_forever(self):
        self.log.debug('run_forever()')

        self._loop.run_forever()

    @asyncio.coroutine
    def get_pubkey(self, request):
        self.log.debug('running get_pubkey()')

        output = self._pubkey

        self.log.info('Request: %s' % request)

        return web.Response(body=output.encode('utf-8'))

    @asyncio.coroutine
    def get_pubkeyjson(self, request):
        self.log.debug('running get_pubkeyjson()')

        output = {'keyfile': self._keyfile,
                  'pubkey': self._pubkey}

        self.log.info('Request: %s' % request)

        return web.Response(body=json.dumps(output,
                                            sort_keys=True).encode('utf-8'))


with PubKeyApp() as app:
    app.run()

    print('Press ctrl-C to stop.')

    try:
        app.run_forever()
    except (KeyboardInterrupt, SystemExit, CaughtSignal):
        app.log.info('Shutting down pubkey REST server')
