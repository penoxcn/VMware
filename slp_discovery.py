#!/usr/bin/env python

import sys
import subprocess

targets = []
for ln in open(sys.argv[1]):
    ln = ln.strip()
    if ln[-4:]==',427':
        targets.append(ln.replace(',T,427',''))

print '%d targets loaded' % (len(targets))

for ip in targets:
    print 'testing %s' % (ip)
    params = ['/usr/bin/slptool','unicastfindsrvs',ip,'service:VMwareInfrastructure']
    try:
        ostr = subprocess.check_output(params)
        print ostr.strip()
    except Exception as e:
        print 'error: %s' % (str(e))
        pass
    params = ['/usr/bin/slptool','unicastfindattrs',ip,'service:VMwareInfrastructure']
    try:
        ostr = subprocess.check_output(params)
        print ostr.strip()
    except Exception as e:
        print 'error: %s' % (str(e))
        pass

    print
