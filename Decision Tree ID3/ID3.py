from node import Node
import math

def ID3(examples, default):
  # get info of attributes and class
  attributes = examples[0].keys()
  attributes.remove('Class')
  attributevalues = getattributevalues(examples)
  labels = getclasslabels(examples)

  # attach info onto the current node (set up new tree root node)
  currentnode = Node()
  currentnode.examples = examples

  if not examples:
    currentnode.label = default
    return [currentnode]
  elif issameclass(examples):
    currentnode.label = examples[0]['Class']
    return [currentnode]
  elif isnonsplit(examples):
    currentnode.label = determineclasslabel(examples,labels)
    return [currentnode]
  else:
    best = choosebestattribute(examples,attributes,attributevalues,labels)
    values = attributevalues[best]

    # update current node info
    currentnode.label = determineclasslabel(examples,labels)
    currentnode.split = best
    tree = [currentnode]

    # divide examples into subexamples
    subexamples = divideexamples(examples,best,attributevalues)

    for i in range(len(subexamples)):
      subtree = ID3(subexamples[i],default)
      subtree[0].value = values[i]
      tree[0].children[i+1] = subtree[0]
      subtree[0].father = tree[0]
      #attach the subtrees to the current root node
      for index in range(len(subtree)):
        subtree[index].level = subtree[index].level + 1
      tree = tree + subtree
    return tree
  '''
  Takes in an array of examples, and returns a tree (an instance of Node) 
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''

def prune(tree, examples):
  havepruned = 0
  oldaccuracy = test(tree,examples)
  
  # go through all the node in the tree
  for node in tree:
    # check if leaf node
    if len(node.children) == 0:
      # check if all the brother nodes are leaf nodes
      if isbrothersallsplitnone(node):

        # get their father node and the list of these brother leaf nodes (removelist)
        father = node.father
        fatherposition = tree.index(father)
        removelist = getremovelist(tree,father)
        
        # get the newtree after removing these leaf nodes, and get the accuracy of it
        newtree = copynewtree(tree,fatherposition,removelist)
        newaccuracy = test(newtree,examples)

        # if the accuracy is better, remove the leafnodes on the original tree
        if newaccuracy > oldaccuracy:
          havepruned = 1
          print 'Pruned'
          tree = removeleafnodes(tree,fatherposition,removelist)
          tree = prune(tree,examples)
          break
  return tree
  '''
  Takes in a trained tree and a validation set of examples.  Prunes nodes in order
  to improve accuracy on the validation data; the precise pruning strategy is up to you.
  '''

def test(tree, examples):
  total = len(examples) + 0.0
  correct = 0.0
  for i in examples:
    classify = evaluate(tree,i)
    actual = i['Class']
    if classify == actual:
      correct = correct + 1.0
  accuracy = correct / total
  return accuracy
  '''
  Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
  of examples the tree classifies correctly).
  '''


def evaluate(tree, example):
  currentnode = tree[0]
  while currentnode.split != None:
    splitattribute = currentnode.split
    childrennodes = currentnode.children.values()
    examplevalue = example[splitattribute]
    match = 0
    for i in childrennodes:
      if examplevalue == i.value:
        currentnode = i
        match = 1
    if match == 0:
      return getclasslabelfromtree(tree)
  resultclass = currentnode.label
  return resultclass
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''

def choosebestattribute(examples,attributes,attributevalues,labels):
  examplesnum = len(examples)
  infogainlist = []
  count = countclasslabel(examples,labels)
  originalentropy = computeentropy(count)
  for i in attributes:
    subexamples = divideexamples(examples,i,attributevalues)
    valuenum = len(attributevalues[i])
    labelnum = len(labels)
    totalentropy = long(0)
    for j in range(valuenum):
      subcount = countclasslabel(subexamples[j],labels)
      subtotal = sum(subcount)
      entropy = computeentropy(subcount)
      totalentropy = totalentropy + entropy * subtotal / examplesnum
      infogain = originalentropy - totalentropy
    infogainlist.append(infogain)
  best = attributes[0]
  maxinfogain = infogainlist[0]
  for i in range(len(attributes))[1:]:
    if infogainlist[i] > maxinfogain:
      maxinfogain = infogainlist[i]
      best = attributes[i]
  return best
  '''
  Choose the best attribute
  Return the best attribute
  '''
def computeentropy(frequencies):
  totalnum = sum(frequencies)
  entropy = 0.0
  for i in range(len(frequencies)):
    p = frequencies[i] / totalnum
    if p != 0:
      entropy = entropy - (p * math.log(p,2.0))
  return entropy
  '''
  Compute the entropy given frequencies
  Return the entropy value
  '''

def getattributevalues(examples):
  attributes = examples[0].keys()
  attributes.remove('Class')
  attributevalues = {}
  for i in attributes:
    attributevalues[i] = []
  for i in attributes:
    for j in examples:
      value = j[i]
      if not value in attributevalues[i]:
        attributevalues[i].append(value)
  return attributevalues
  '''
  Get the values of all the attributes
  Return a dictionary with list of attributes' values as the value of dic
  '''

def getclasslabels(examples):
  labels = []
  for i in examples:
    if not i['Class'] in labels:
      labels.append(i['Class'])
  return labels

def issameclass(examples):
  if len(examples) == 1:
    return examples[0]['Class']
  else:
    sameclass = examples[0]['Class']
    for i in examples:
      if i['Class'] != sameclass:
        return 0
    return sameclass
  '''
  Check if all the examples have the same class value
  Return that class if have the same class
  Return 0 if not
  '''

def isnonsplit(examples):
  if len(examples) == 1:
    return 1
  else:
    attributes = examples[0].keys()
    attributes.remove('Class')
    for i in attributes:
      same = examples[0][i]
      for j in examples:
        if j[i] != same:
          return 0
    return 1

def determineclasslabel(examples,labels):
  count = countclasslabel(examples,labels)
  resultlabel = labels[0]
  maxcount = count[0]
  for index in range(len(count))[1:]:
    if count[index] >= maxcount:
      maxcount = count[index]
      resultlabel = labels[index]
  return resultlabel
  '''
  Determine what the label of the node is
  Return the label
  '''

def countclasslabel(examples,labels):
  num = len(labels)
  count = []
  for index in range(num):
    subcount = 0.0
    for i in examples:
      if i['Class'] == labels[index]:
        subcount = subcount + 1.0
    count.append(subcount)
  return count
  '''
  Count the frequency of each class label in the examples
  Return the count result
  '''

def divideexamples(examples,best,attributevalues):
  values = attributevalues[best]
  num = len(values)
  subexamples = []
  for index in range(num):
    sub = []
    for i in examples:
      if i[best] == values[index]:
        sub.append(i)
    subexamples.append(sub)
  return subexamples
  '''
  Divide the examples into several subexamples by the values of the best attribute
  Return a list of subexamples
  '''

def getclasslabelfromtree(tree):
  labels = []
  count = []
  for i in tree:
    if not i.label in labels:
      labels.append(i.label)
      count.append(0)
  for i in tree:
    for j in range(len(labels)):
      if i.label == labels[j]:
        count[j] = count[j] + 1
  resultlabel = labels[0]
  maxcount = count[0]
  for i in range(len(labels)):
    if count[i] > maxcount:
      maxcount = count[i]
      resultlabel = labels[i]
  return resultlabel

def copynewtree(tree,fatherposition,removelist):
  newtree = []
  for i in tree:
    newnode = i.copynode()
    newtree.append(newnode)
  for i in range(len(tree)):
    newtree[i].children = {}
    newtree[i].father = None
    childrenlist = tree[i].children.values()
    if childrenlist:
      for j in range(len(childrenlist)):
        position = tree.index(childrenlist[j])
        newtree[i].children[j+1] = newtree[position]
    father = tree[i].father
    if father != None:
      position = tree.index(father)
      newtree[i].father = newtree[position]
  newtree = removeleafnodes(newtree,fatherposition,removelist)
  return newtree
  '''
  Get a copy of newtree that has been modified by removing leaf nodes
  Return the new tree
  '''

def isbrothersallsplitnone(node):
  father = node.father
  isall = True
  for child in father.children.values():
    if len(child.children) != 0:
      isall = False
  return isall
  '''
  Check if the brother nodes of it are all leaf nodes
  Return True or False
  '''

def getremovelist(tree,father):
  removelist = []
  for child in range(len(tree)):
    if tree[child] in father.children.values():
      removelist.append(child)
  return removelist
  '''
  Get the removelist of the brother leaf nodes according to their father node
  Return the removelist
  '''

def removeleafnodes(tree,fatherposition,removelist):
  popnum = 0
  for i in removelist:
    tree.pop(i-popnum)
    popnum = popnum + 1
  tree[fatherposition].children = {}
  tree[fatherposition].split = None
  return tree
  '''
  Remove the leaf nodes in the removelist and set the father.children to {}
  Return the new tree
  '''