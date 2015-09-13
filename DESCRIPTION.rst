pubkey
======
.. image:: https://secure.travis-ci.org/fxstein/pubkey.svg?branch=master
  :target: https://travis-ci.org/#!/fxstein/pubkey

Need to setup private/public key server connections for e.g. password less ssh
communications? Tired of manually having to copy around public keys?

pubkey creates a RESTful endpoint and replies with the public key you want to
share. Default is plain text so you can use curl to download and apply the
public key with a single step. Optionally the key can be wrapped in a json
document for other usecases.

Simply run the following command on the source server:

  $ pubkey --auto
  # Starts the pubkey server with default settings and IP auto detection

  INFO: pubkey file used: /Users/xxxxx/.ssh/id_rsa.pub
  INFO: pubkey server started at http://192.168.0.36:1080
  Remote host command:

  curl -s -S 192.168.0.36:1080 >> ~/.ssh/authorized_keys

  Press ctrl-C to stop.

Then copy the curl statement provide above to the terminal of the server you
would like to add the public key to:

  curl -s -S 192.168.0.36:1080 >> ~/.ssh/authorized_keys

Done. If you did not get an error (e.g. unreachable host) you are all set.

For more information head over to github:
https://github.com/fxstein/pubkey
