# pubkey
[![Build Status](https://travis-ci.org/fxstein/pubkey.svg?branch=master)](https://travis-ci.org/fxstein/pubkey)

Need to setup private/public key server connections for password less ssh communications? Tired of manually having to copy around public keys? pubkey creates a RESTful endpoint and replies with the public key you want to share. Default is plain text so you can use curl to download and apply the public key with a single step. Optionally the key can be wrapped in a json document for other usecases.

INSTALLATION
------------
```bash
$ [sudo] pip install --upgrade pubkey
```
The module is hosted on PyPi: https://pypi.python.org/pypi/pubkey

USAGE
-----

Simply head to the host that has the public key and run

```bash
$ pubkey --auto
# Starts the pubkey server with default settings and IP auto detection
```
Example output:
```
INFO: pubkey file used: /Users/xxxxx/.ssh/id_rsa.pub
INFO: pubkey server started at http://192.168.0.36:1080
Remote host command:

curl -s -S 192.168.0.36:1080 >> ~/.ssh/authorized_keys

Press ctrl-C to stop.

```
Now head to your first remote host on the same network e.g. ssh with password and run
```bash
$ curl -s -S 192.168.0.36:1080 >> ~/.ssh/authorized_keys
# Downloads the public key from the first host and appends it to the users authorized_keys
```
If you don't see an error message you should be done. Logout and and attempt an ssh connection from the first to the second host. If usernames match up you should not be required a password any longer.

You can also validate that the key has been successfully added by running
```bash
$ cat ~/.ssh/authorized_keys
```
You should see the content of the public key appended at the end of the file (which might be the very first entry in case authorized_keys did not exist before)

And just in case you appended the same public key more than once for whatever reason no harm is done. Simple sort the file and remove duplicates by running
```
$ sort -u ~/.ssh/authorized_keys -o ~/.ssh/authorized_keys
```

For more options please run
```bash
$ pubkey --help
```
```
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
 -h, --help     show this help message and exit
 --debug        toggle debug output
 --quiet        suppress all output
 -a, --auto     Auto detect IP address to bind REST server to.
 -o, --once     Reply to only 1 request then quit.
 --host HOST    IP address to bind REST server to. Default is <localhost> and
                therefore NOT visible on the network.
 --key KEYFILE  Keyfile of public key. Commonly ~/.ssh/id_rsa.pub Only public
                key filenames [.pub] allowed.
 --port PORT    Port to be used by REST server. Default is 1080.
 -v, --version  show program's version number and exit

Report bugs, submit feature requests, and/or contribute code over at:
https://github.com/fxstein/pubkey
```
