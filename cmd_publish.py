#!/usr/bin/python
"""
Arguments:

    exchange            name of exchange
    routing_key         interpretation of routing key depends on exchange type

Options:

    -i --input=PATH     content to send (- for stdin)
    -s --sender=        message sender
    -e --encrypt        encrypt message using secret TKLAMQ_SECRET
"""

import os
import sys
import getopt

from amqp import __doc__ as env_doc
from amqp import connect, encode_message

def usage(e=None):
    if e:
        print >> sys.stderr, "error: " + str(e)

    print >> sys.stderr, "Syntax: %s [-opts] <exchange> <routing_key>" % sys.argv[0]
    print >> sys.stderr, "Message is stdin"
    print >> sys.stderr, __doc__, env_doc
    sys.exit(1)

def fatal(s):
    print >> sys.stderr, "error: " + str(s)
    sys.exit(1)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'i:s:eh', ['input=', 'sender='])
    except getopt.GetoptError, e:
        usage(e)

    inputfile = None
    sender = None
    opt_encrypt = False
    for opt, val in opts:
        if opt == '-h':
            usage()

        if opt in ('-i', '--input'):
            inputfile = val

        if opt in ('-s', '--sender'):
            sender = val

        if opt in ('-e', '--encrypt'):
            opt_encrypt = True

    if not len(args) == 2:
        usage()

    secret = os.getenv('TKLAMQ_SECRET', None)
    if opt_encrypt and not secret:
        fatal('TKLAMQ_SECRET not specified, cannot encrypt')

    # unset secret if encryption was not specified
    if not opt_encrypt:
        secret = None

    content = ''
    if inputfile == '-':
        content = sys.stdin.read()
    elif inputfile:
        content = file(inputfile).read()

    exchange, routing_key = args
    message = encode_message(sender, content, secret=secret)

    conn = connect()
    conn.publish(exchange, routing_key, message)

if __name__ == "__main__":
    main()

