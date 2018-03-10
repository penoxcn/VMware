#!/usr/bin/env python

import sys
import requests
requests.packages.urllib3.disable_warnings()


apixml1='''<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"  xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<soapenv:Body><QueryVpxaStatus xmlns="urn:vpxa3"><_this type="VpxapiVpxaService">vpxa</_this></QueryVpxaStatus></soapenv:Body></soapenv:Envelope>'''

apixml2='''<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"  xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<soapenv:Body><GetVpxaInfo xmlns="urn:vpxa3"><_this type="VpxapiVpxaService">vpxa</_this></GetVpxaInfo></soapenv:Body></soapenv:Envelope>'''

targets = []
for f in open(sys.argv[1]):
    try:
        ip,t,port = f.strip().split(',')
        if int(port)==902:
            targets.append(ip+':443')
    except:
        pass

print 'load %d targets' % (len(targets))
url_fmt = 'https://%s/vpxa'

flog = open('vpxascanlog.txt','wb')

for target in targets:
    url = url_fmt % (target)

    headers = {'Content-Type': 'text/xml; charset=utf-8', 'User-Agent': 'VMware-client/5.5.0','SOAPAction':'"urn:vpxa3/5.5"'}
    print '*>>>: %s' % (url)
    try:
        rs = requests.post(url, data=apixml1, headers=headers, verify=False, timeout=8)
        #print '*ret: %r' % (rs.content)
        #print '-'*16
        if rs.status_code==200:
            flog.write('%s:QueryVpxaStatus:\n' % (target))
            flog.write(rs.content)
            flog.write('\n')
    except Exception as e:
        print 'Err: %s' % (str(e))
    try:
        rs = requests.post(url, data=apixml2, headers=headers, verify=False, timeout=8)
        if rs.status_code==200:
            flog.write('%s:GetVpxaInfo:\n' % (target))
            flog.write(rs.content)
            flog.write('\n\n')
        #print '*ret: %r' % (rs.content)
        #print '-'*16
    except Exception as e:
        print 'Err: %s' % (str(e))
    print

flog.close()
    
