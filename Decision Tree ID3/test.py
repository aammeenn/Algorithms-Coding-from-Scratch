import parse,math,unit_tests,ID3,copy
from node import Node


filename = 'house_votes_84.data'
examples = parse.parse(filename)
'''
test = examples[:50] + examples[200:230] + examples[400:]
train = []
for i in examples:
    if not i in test:
        train.append(i)
tree = ID3.ID3(train,'democrat')
print len(tree)

accuracy = ID3.test(tree,test)
print accuracy
print tree

print ' '
tree = ID3.prune(tree,test)
print tree
accuracy = ID3.test(tree,test)
print accuracy
'''
#unit_tests.testID3AndEvaluate()
#unit_tests.testPruning()
unit_tests.testPruningOnHouseData(filename)
