#!/usr/bin/env python

from graphviz import Digraph
from enum import Enum
import yaml

tech_yaml = 'tech.yml'
rels_yaml = 'relationships.yml'

nodes = yaml.load(open(tech_yaml, 'r').read())
rels = yaml.load(open(rels_yaml, 'r').read())

def getShape(tech_type):
    shape = 'box'
    if tech_type == 'language':
        shape = 'diamond'
    elif tech_type == 'protocol':
        shape = 'oval'
    elif tech_type == 'application' or 'entrypoint':
        shape = 'box'

    return shape


def getFill(tech_type):
    fill = ''
    if tech_type == 'entrypoint':
        fill = 'filled'

    return fill


def getColor(tech_type):
    color = ''
    if tech_type == 'entrypoint':
        color = 'lightgrey'

    return color


# Crosslink all *.exe with EXE
for node in nodes:
    if '.exe' in node['name']:
        rels.append({'source':'EXE', 'target':node['name']})

graph = Digraph(name="code-exec")

# Create nodes
for node in nodes:
    graph.node(node['name'], shape=getShape(node['type']), style=getFill(node['type']), color=getColor(node['type']))


# Create edges
for rel in rels:
    if rel.get('url', None) is None:
        graph.edge(rel['source'], rel['target'], label=rel.get('label', ''))
    else:
        graph.edge(rel['source'], rel['target'], label=rel.get('label', ''), labelURL=rel['url'])

# Render graph
graph.attr(label='\n\nCode Exec Graph\n')
graph.attr(fontsize='20')
graph.format = 'svg'
graph.render()  
