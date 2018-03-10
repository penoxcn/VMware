import re

pattern='''<serverIp>([^<>]*)</serverIp><serverPort>(\d+)</serverPort><hostIp>([^<>]*)</hostIp><hostPort>(\d+)</hostPort>'''
xml=open('vpxascanlog.txt').read()
ms=re.findall(pattern,xml)
#pairs=set(['"%s" -> "%s";' % (j[0],j[2]) for j in ms])
#rs='digraph demo{\n'+'\n'.join(sorted(pairs))+'\n}'

vms = dict()
logs=open('slp_vmware.all.txt').read().split('\n\n')
for log in logs:
    if log.find('product')<0:
        continue
    fs=re.findall('testing ([^\t]+).*?product="([^"]+)"', log.replace('\n','\t'))
    if fs and fs[0]:
        vms[fs[0][0]] = fs[0][1][len('VMware '):fs[0][1].find(' build')]

vmware = set()
for ln in open('vmware_banner.txt'):
    fs = ln.split('\t')
    if fs:
        vmware.add(fs[0])
    
vuls = dict()
for ln in open('ssltest2.log'):
    fs = ln.strip().split(' ')
    if fs and len(fs)==2 and fs[1]=='Y' and fs[0] in vmware:
        vuls[fs[0]] = 'SSL'

for ln in open('xxe_vm.txt'):
    fs = ln.strip().split(' - - ')
    if fs and len(fs)==2:
        if fs[0] in vuls:
            vuls[fs[0]] += '|XXE'
        else:
            vuls[fs[0]] = 'XXE'

for ln in open('rmivul.txt'):
    fs = ln.strip().split(' - - ')
    if fs and len(fs)==2:
        if fs[0] in vuls:
            vuls[fs[0]] += '|RMI'
        else:
            vuls[fs[0]] = 'RMI'    

allip = set(vms.keys()+vuls.keys()+[j[0] for j in ms]+[j[2] for j in ms])

ostr = 'digraph demo{\nnode [color=Green,fontcolor=Blue,font=Courier]\n'

lines = ''

for j in allip:
    label = j
    alert = ''
    if j in vms:
        label += '\\nver:'+vms[j]
    if j in vuls:
        label += '\\nvul:'+vuls[j]
        alert = 'style=filled fillcolor=red '
    lines += '"%s" [ label="%s" %s];\n' % (j,label,alert)

ostr += lines

lines = ''
dups = set()
for j in ms:
    if j[0]+j[2] not in dups:
        lines += '"%s" -> "%s";\n' % (j[0],j[2])
        dups.add(j[0]+j[2])
ostr += lines

lines = ''
for j in allip-set([j[0] for j in ms]+[j[2] for j in ms]):
    lines += '"%s";\n' % (j)

ostr += lines
ostr += '}\n'

print ostr
