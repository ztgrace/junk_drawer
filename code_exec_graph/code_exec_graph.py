#!/usr/bin/env python

from graphviz import Digraph
from enum import Enum

class Type(Enum):
    PROTOCOL = 'protocol'
    APPLICATION = 'application'
    LANGUAGE = 'language'
    ENTRYPOINT = 'entrypoint'

class Node:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.type = kwargs.get('type', '')
        self.url = kwargs.get('url', None)

    def shape(self):
        shape='box'
        if self.type == Type.LANGUAGE:
            shape = 'diamond'
        elif self.type == Type.PROTOCOL:
            shape='oval'
        elif self.type == Type.APPLICATION or Type.ENTRYPOINT:
            shape='box'

        return shape

    def fill(self):
        fill=''
        if self.type == Type.ENTRYPOINT:
            fill = 'filled'

        return fill

    def color(self):
        color = ''
        if self.type == Type.ENTRYPOINT:
            color = 'lightgrey'

        return color
            
class Relationship:
    def __init__(self, **kwargs):
        self.source = kwargs.get('source', Node())
        self.target = kwargs.get('target', Node())
        self.label = kwargs.get('label', '')
        self.url = kwargs.get('url', None)

# TODO move data into a json or yaml file

nodes = {
    'wmi': Node(name='WMI', type=Type.PROTOCOL),
    'word': Node(name='winword.exe', type=Type.ENTRYPOINT),
    'dll': Node(name='DLL', type=Type.APPLICATION),
    'powershell': Node(name='powershell.exe', type=Type.APPLICATION),
    'msxsl': Node(name='msxsl.exe', type=Type.APPLICATION),
    'wmic': Node(name='wmic.exe', type=Type.APPLICATION),
    'vba': Node(name='VBA', type=Type.LANGUAGE),
    'vbscript': Node(name='VB Script', type=Type.LANGUAGE),
    'jscript': Node(name='JScript', type=Type.LANGUAGE),
    'xsl': Node(name='XSL', type=Type.LANGUAGE),
    'xml': Node(name='XML', type=Type.LANGUAGE),
    'sct': Node(name='SCT', type=Type.LANGUAGE),
    'C#': Node(name='C#', type=Type.LANGUAGE),
    'win32api': Node(name='Win32API', type=Type.PROTOCOL),
    'shellcode': Node(name='Shellcode', type=Type.LANGUAGE),
    'exe': Node(name='EXE', type=Type.APPLICATION),
    'cmstp': Node(name='cmstp.exe', type=Type.APPLICATION),
    'lnk': Node(name='LNK', type=Type.ENTRYPOINT),
    'pubprn.vbs': Node(name='PubPrn.vbs', type=Type.APPLICATION),
    'mshta': Node(name='mshta.exe', type=Type.APPLICATION),
    'htmla': Node(name='HTML Application', type=Type.LANGUAGE),
    'rdi': Node(name='Reflective DLL Injection', type=Type.APPLICATION),
    'regsrv32': Node(name='regsrv32.exe', type=Type.APPLICATION),
    'settingcontent-ms': Node(name='settingcontent-ms', type=Type.ENTRYPOINT),
    'reflection-assembly': Node(name='Reflection.Assembly', type=Type.LANGUAGE, URL='https://bohops.com/2018/02/26/leveraging-inf-sct-fetch-execute-techniques-for-bypass-evasion-persistence/'),
}

rels = list()
rels.append(Relationship(source=nodes.get('C#'), target=nodes.get('win32api')))
rels.append(Relationship(source=nodes.get('cmstp'), target=nodes.get('sct'), label='INF', url='https://bohops.com/2018/02/26/leveraging-inf-sct-fetch-execute-techniques-for-bypass-evasion-persistence/'))
rels.append(Relationship(source=nodes.get('dll'), target=nodes.get('win32api')))
rels.append(Relationship(source=nodes.get('htmla'), target=nodes.get('vbscript')))
rels.append(Relationship(source=nodes.get('htmla'), target=nodes.get('jscript')))
rels.append(Relationship(source=nodes.get('jscript'), target=nodes.get('C#'), label='DotNetToJScript', url='https://github.com/tyranid/DotNetToJScript'))
rels.append(Relationship(source=nodes.get('lnk'), target=nodes.get('exe')))
rels.append(Relationship(source=nodes.get('mshta'), target=nodes.get('htmla')))
rels.append(Relationship(source=nodes.get('msxsl'), target=nodes.get('xml')))
rels.append(Relationship(source=nodes.get('powershell'), target=nodes.get('exe'), label='Invoke-Item'))
rels.append(Relationship(source=nodes.get('powershell'), target=nodes.get('win32api')))
rels.append(Relationship(source=nodes.get('powershell'), target=nodes.get('reflection-assembly')))
rels.append(Relationship(source=nodes.get('reflection-assembly'), target=nodes.get('jscript'), labelURL='https://twitter.com/bohops/status/965085651199840258'))
rels.append(Relationship(source=nodes.get('reflection-assembly'), target=nodes.get('vbscript'), labelURL='https://twitter.com/bohops/status/965670898379476993'))
rels.append(Relationship(source=nodes.get('pubprn.vbs'), target=nodes.get('sct'), label='scrobj.dll', labelURL='https://enigma0x3.net/2017/08/03/wsh-injection-a-case-study/'))
rels.append(Relationship(source=nodes.get('rdi'), target=nodes.get('dll')))
rels.append(Relationship(source=nodes.get('regsrv32'), target=nodes.get('sct'), label='scrobj.dll'))
rels.append(Relationship(source=nodes.get('sct'), target=nodes.get('jscript')))
rels.append(Relationship(source=nodes.get('shellcode'), target=nodes.get('win32api')))
rels.append(Relationship(source=nodes.get('vba'), target=nodes.get('wmi')))
rels.append(Relationship(source=nodes.get('vba'), target=nodes.get('exe'), label='WScript.Shell'))
rels.append(Relationship(source=nodes.get('vba'), target=nodes.get('win32api')))
rels.append(Relationship(source=nodes.get('vbscript'), target=nodes.get('win32api')))
rels.append(Relationship(source=nodes.get('vbscript'), target=nodes.get('wmi')))
rels.append(Relationship(source=nodes.get('win32api'), target=nodes.get('shellcode')))
rels.append(Relationship(source=nodes.get('win32api'), target=nodes.get('rdi')))
rels.append(Relationship(source=nodes.get('wmi'), target=nodes.get('win32api')))
rels.append(Relationship(source=nodes.get('wmic'), target=nodes['wmi']))
rels.append(Relationship(source=nodes.get('wmic'), target=nodes.get('xsl'), label="subtee", url='https://subt0x11.blogspot.com/2018/04/wmicexe-whitelisting-bypass-hacking.html'))
rels.append(Relationship(source=nodes.get('word'), target=nodes['vba']))
rels.append(Relationship(source=nodes.get('xml'), target=nodes.get('jscript')))
rels.append(Relationship(source=nodes.get('xsl'), target=nodes.get('vbscript')))
rels.append(Relationship(source=nodes.get('xsl'), target=nodes.get('jscript')))
rels.append(Relationship(source=nodes.get('settingcontent-ms'), target=nodes.get('exe')))

for node in nodes:
    if '.exe' in nodes[node].name:
        rels.append(Relationship(source=nodes.get('exe'), target=nodes[node]))

graph = Digraph(name="code-exec")

for node in nodes:
    graph.node(nodes[node].name, shape=nodes[node].shape(), style=nodes[node].fill(), color=nodes[node].color())


for rel in rels:
    if rel.url is None:
        graph.edge(rel.source.name, rel.target.name, label=rel.label)
    else:
        graph.edge(rel.source.name, rel.target.name, label=rel.label, labelURL=rel.url)

graph.attr(label='\n\nCode Exec Graph\n')
graph.attr(fontsize='20')
graph.format = 'svg'
graph.render()  
