import math
import imp
import time
import multiprocessing as mp

class Node:
    def __init__(self, value=0):
        self.lstChild = []
        self.value = value


    def addChild (self, childNode = None):
        if type(childNode) == Node:
            self.lstChild.append(childNode)
            return self
        else:
            raise Exception()

    def printValue(self, space):
        print (space + str(self.value))
        for child in self.lstChild:
            child.printValue(space + '   ')


# node1 = Node()
#
# node11 = Node(1).addChild(Node(-4).addChild(Node(3)))
# node12 = Node(5).\
#     addChild(Node(-3).addChild(Node(5))). \
#     addChild(Node(-4).addChild(Node())). \
#     addChild(Node(-6)).addChild(Node())
#
# node13 = Node(3)
#
# node1.addChild(node11).addChild(node12).addChild(node13)
#
#
# node1.printValue('')
#
# a = math.inf
# b = math.inf
#
# print (a < b)

if __name__ == "__main__":

    data = [None, None]


    def foo(process_number, value, pipe=None):
        print("Start process %i" % (process_number))
        start = time.time()

        i = 0
        while (i < value):
            i += 1
        end = time.time()
        eslape = end - start

        data[process_number] = i
        print("From process " + str(process_number) + " value " + str(data))
        if pipe:
            pipe.send(data)

        print("End process %i in %f" % (process_number, eslape))


    conn = mp.Pipe()

    processNo1 = mp.Process(target=foo, args=(1, 100000000, conn[1]))
    processNo1.start()

    foo(0, 10000)

    processNo1.join()
    obj = conn[0].recv()

    for i in range(len(data)):
        if not data[i]:
            data[i] = obj[i]


    # print (mp.cpu_count())
    #
    # file = open("/output/output.txt", 'w+')
    # file.write('Say hi from floyd')

    print (data)
    # processNo3 = mp.Process(target=foo, args=(3,))
    # processNo3.start()
    #
    # processNo1 = mp.Process(target=foo, args=(4,))
    # processNo1.start()
