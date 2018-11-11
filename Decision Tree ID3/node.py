import copy
class Node:
    def __init__(self):
        self.label = None
        self.children = {}
        self.examples = []
        self.split = None
        self.level = 1
        self.value = None
        self.father = None

    def copynode(self):
    	newnode = Node()
    	newnode.label = copy.copy(self.label)
    	newnode.children = copy.copy(self.children)
    	newnode.examples = copy.copy(self.examples)
    	newnode.split = copy.copy(self.split)
    	newnode.level = copy.copy(self.level)
    	newnode.value = copy.copy(self.value)
    	newnode.father = copy.copy(self.father)
    	return newnode
	# you may want to add additional fields here...