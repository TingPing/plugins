#!/usr/bin/env python

import sys

if len(sys.argv) < 3 or not sys.argv[2]:
    print('/echo nick required to ban.')
    sys.exit()

chan = sys.argv[1]
nick = sys.argv[2]

print('/echo banning {}...'.format(nick))
print('/cs op {}'.format(chan))
print('/timer 3 ban {}'.format(nick))
print('/timer 5 cs deop {}'.format(chan))
