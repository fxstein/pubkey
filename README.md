pubkey
======

[![Build Status](https://travis-ci.org/fxstein/pubkey.svg?branch=master)](https://travis-ci.org/fxstein/pubkey)

Need to setup private/public key server connections for password less ssh
communications? Tired of manually having to copy around public keys?

pubkey creates a RESTful endpoint and replies with the public key you want to
share. Default is plain text so you can use curl to download and apply the
public key with a single step. Optionally the key can be wrapped in a json
document for other use-cases.

INSTALLATION
------------

```shell
$ [sudo] pip[3] install pubkey
or
$ [sudo] pip[3] install --upgrade pubkey
# Upgrades older versions of the tool
```

The module is hosted on PyPi: <https://pypi.python.org/pypi/pubkey>

To install from github clone the repository onto your local machine then run

```shell
$ [sudo] setup.py install
# From the repository root directory e.g. /Users/xxxxx/pubkey
```

USAGE
-----

Simply head to the host that has the public key and run

```shell
$ pubkey --auto
# Starts the pubkey server with default settings and IP auto detection
```

Example output:

```text
INFO: pubkey file used: /Users/xxxxx/.ssh/id_rsa.pub
INFO: pubkey server started at http://192.168.0.36:1080
Remote host command:

curl -s -S 192.168.0.36:1080 >> ~/.ssh/authorized_keys

Press ctrl-C to stop.
```

Now head to your first remote host on the same network e.g. ssh with password
and run

```shell
$ curl -s -S 192.168.0.36:1080 >> ~/.ssh/authorized_keys
# Downloads the public key from the first host and appends it to the users authorized_keys
```

If you don't see an error message you should be done. Logout and and attempt an
ssh connection from the first to the second host. If usernames match up you
should not be required a password any longer.

You can also validate that the key has been successfully added by running

```shell
$ cat ~/.ssh/authorized_keys
```

You should see the content of the public key appended at the end of the file
(which might be the very first entry in case authorized_keys did not exist
before)

And just in case you appended the same public key more than once for whatever
reason no harm is done. Simple sort the file and remove duplicates by running

```shell
$ sort -u ~/.ssh/authorized_keys -o ~/.ssh/authorized_keys
```

In case you need to get access to the public key via JSON simply append /json to
the GET request:

```shell
$ curl -s -S 192.168.0.36:1080/json
{"keyfile": "/Users/xxxxx/.ssh/id_rsa.pub", "pubkey": "ssh-rsa AAAAB3NzaC1yc2EBBBBDAQABAAACAQC48EkBhgKDBP3ziBrHUCEoWIiY74OkarBVrLFkQz2MC+u5cKpE3zU7OXDI1AvtBt1Gb7mBvocztoa6r+YkPodOwjJK7N/FtLIO8yevIz2H3bClEryxb0yKmhrAB2jDlTPZoBd8gIFUdCUyAN+BVTXF9sNsyhOpVaycsUaMmocqEWmTm7Awl3PJhZq6nwaSy4Etb9Mkj0DCiDCwL9auDRbHbyw3kekQ5q7bBF7cIzQAUN2EWCTI1dMvv8KgHsrctfwfmN0Bu/Dy4vCp47UMXzlNI2wrKhYvVCKi9MU+K5bWRMmv76vHctvMnrcwvwllYDG3+ltgDhZAvIKKTrXBuMS4zGoDM7dF1Rz825olUkyd+9LgqW+tMy7tOM1edE9lBsB/rJYwtGWCH1zHmg65+W/Sfx2X5mLZ27BOHs46f5o0zyuST8LOgQNNDhuiJWLQGlsgsQ1RTPtlysgnGx300WEvc9lKMaAE9ixTSwq1R5GrNrt9PnB3jQp6BnTsxdZuOv8nicfqkSoRRBRcNEIz7wMXIzZOgTJCMu+5l3nOOijHZKfUA0AMjwr1LwCZWHnZ12k1XE5RteUqroXANs66WfEkIMpxHAL+pjqozZ7e1cRphIPVk7HskWyzLWM/DoXYnfSas6KrSNfv5TUdu45mWiKFGIEVZExsC3sQJ1Kun3fCgQ== another@email.com\n"}
```

For more options please run

```shell
$ pubkey --help
```

```text
usage: pubkey {arguments ...}

pubkey - Public Key distribution made easy.

Ever needed to quickly setup trusted keys for password less ssh sessions?
pubkey helps by making public keys avaialble on the local network with a
simple REST interface and a matching command to append the public key to
various machines on the same network.

Simply start pubkey on the source of the public key. Then head over to your
remote target and run:

curl -s -S host:port >> ~/.ssh/authorized_keys

on the various hosts that require the key to be added to their trusted keys.
Done.

optional arguments:
  -h, --help            show this help message and exit
  --debug               toggle debug output
  --quiet               suppress all output
  -a, --auto            Auto detect IP address to bind REST server to.
  --host HOST           IP address to bind REST server to. Default is
                        <localhost> and therefore NOT visible on the network.
  --key KEYFILE         Keyfile of public key. Commonly ~/.ssh/id_rsa.pub Only
                        public key filenames [.pub] allowed.
  -n NUM, --num NUM     Reply to only (num) requests then quit. 0 for no
                        limit. Deafult is 0 (no limit)
  -o, --once            Reply to only 1 request then quit.
  --port PORT           Port to be used by REST server. Default is 1080.
  -t TIME, --time TIME  Timeout ater (time) seconds then quit. 0 for no
                        timeout. Default is 300s (5min)
  -v, --version         show program's version number and exit

Examples:

$ pubkey --auto

  Run pubkey in host auto detection mode. Should detect the correct server IP
  for the local host on the local network in most cases. If not use --host
  option to override with desired hostname or IP.
  Timeout after 300 seconds by default

$ pubkey --host 10.1.1.124 --port 6080 --time 0

  Run pubkey and open REST server at 10.1.1.124:6080 and no timeout.

$ pubkey --auto --once

  Run pubkey in host auto detection mode and finish after 1 request or the
  default of 300s - whichever comes first

$ pubkey -auto -n 10 -t 600

  Run pubkey in auto detection mode and finish after 10 requests or 600 seconds
  whichever comes first

Report bugs, submit feature requests, and/or contribute code over at:
https://github.com/fxstein/pubkey
```

REQUIREMENTS
------------

pubkey requires Python 3.4+ to run. This is because pubkey leverages the new
asyncio framework of Python 3.4 or newer.

pubkey also leverages the following modules:

*   asyncio >= 3.4.0
*   aiohttp >= 0.17.0
*   cement >= 2.6.0
*   colorlog >= 2.6.0

pubkey leverages an async http web-server to implement is server side REST
interface.

pubkey also leverages the [Cement](http://builtoncement.com/) framework to
implement command-line options, logging, configuration as well as overall
application orchestration.

LICENSE
-------

The MIT License (MIT)

Copyright (c) 2015 Oliver Ratzesberger

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
