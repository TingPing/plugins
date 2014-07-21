#!/usr/bin/env python

import sys

if len(sys.argv) < 3 or not sys.argv[2]:
    print('/echo nick required.')
    sys.exit()

nick = sys.argv[2]

print('/ctcp {} VERSION'.format(nick))
