#!/usr/bin/env python

import json
import sys

if len(sys.argv) < 2:
    print "Usage: ", sys.argv[0], " json.file\n"
    sys.exit(-1)


data = open(sys.argv[1]).read()
try:
    decoded = json.loads(data)
    print "decode succ"
except Exception, e:
    print "Error:", str(e)


#print "="*80
#print json.dumps(data, sort_keys=True, indent=2)

