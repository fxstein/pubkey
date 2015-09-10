#!/usr/local/bin/python3 -u
__author__ = 'Oliver Ratzesberger <https://github.com/fxstein>'
__copyright__ = 'Copyright (C) 2015 Oliver Ratzesberger'
__license__ = 'Apache License, Version 2.0'

import os
import asyncio
import json
from aiohttp import web

import configparser

from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController # , expose
from cement.core import hook
from cement.core.exc import CaughtSignal
from cement.ext.ext_colorlog import ColorLogHandler
from cement.ext.ext_configparser import ConfigParserConfigHandler

# Default settings
from cement.utils.misc import init_defaults

defaults = init_defaults('pubkey', 'pubkey')
defaults['pubkey']['keyfile'] = '~/.ssh/id_rsa.pub'
defaults['pubkey']['server'] = 'localhost'
defaults['pubkey']['port'] = 1080


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
        description = "pubkey - Public Key distribution made easy"

        arguments = [
            (['-a', '--auto'],
             dict(action='store_true', help='auto detect IP address - TBD')),
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

        hook.register('post_run', self._post_run)
        hook.register('pre_close', self._pre_close)

    def _post_run(self, app):
        self.log.debug('running _post_run()')

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
        self.log.info('pubkey:\n%s' % self._pubkey)

        server = self.config.get('pubkey', 'server')
        port = self.config.get('pubkey', 'port')

        self._webapp = web.Application(loop=loop, logger=None)

        # Handle incoming events
        self._webapp.router.add_route('GET', '/', self.get_pubkey)
        self._webapp.router.add_route('GET', '/json', self.get_pubkeyjson)

        self._webapp_handler = self._webapp.make_handler()

        try:
            self._webapp_srv = yield from self._loop.create_server(
                self._webapp_handler, server, port)

            self.log.info("pubkey server started at http://%s:%s/" %
                          (server, port))

        except Exception as e:
            self.log.fatal("Error starting pubkey at http://%s:%s/" %
                           (server, port))
            self.log.fatal(e)
            self._loop.stop()

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

    # Workaround for potential cement 2.7 bug:
    if hasattr(app, '_keyfile') is False:
        app._post_run(app)

    try:
        app.run_forever()
    except (KeyboardInterrupt, SystemExit, CaughtSignal):
        app.log.info('Shutting down pubkey REST server')
