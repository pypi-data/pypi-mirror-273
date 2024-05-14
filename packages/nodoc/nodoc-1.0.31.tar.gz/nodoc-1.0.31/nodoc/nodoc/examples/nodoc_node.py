from nodoc.structure import docNode
from nodoc.structure import docTree

nodeA = docNode(content="foo", kind='title')
nodeA_child = docNode(content="foochild", kind='text')

nodeB = docNode(content="bar", kind='title')
nodeB_child = docNode(content="barchild", kind='text')