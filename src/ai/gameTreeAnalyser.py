
from ai.gameTree import GameTree

class GameTreeAnalyser:
    leafList = []
    bestLeafScore = -1023
    bestLeaf = None

    @classmethod
    def reset(cls):
        GameTreeAnalyser.leafList = []
        GameTreeAnalyser.bestLeafScore = -1023
        GameTreeAnalyser.bestLeaf = None
        
    @classmethod
    def getLeafStates(cls, treeRootNode : GameTree) -> (GameTree): 
        print("Score is always: " + str(cls.bestLeafScore))
        cls.findLeafStates(treeRootNode)
        return cls.leafList
    
    @classmethod
    def getBestLeafState(cls, treeRootNode : GameTree) -> (GameTree, int): 
        cls.findBestLeafState(treeRootNode)
        return cls.bestLeaf, cls.bestLeafScore
    
    @classmethod
    def findBestLeafState(cls, node : GameTree): 
        if node.isLeaf() or node.isTerminal():
            if node.score > cls.bestLeafScore:
                cls.bestLeafScore = node.score
                cls.bestLeaf = node
        else:
            for child in node.children:
                cls.findBestLeafState(child)

    @classmethod
    def findLeafStates(cls, node : GameTree): 
        if node.isLeaf():
            cls.leafList.append(node)    
        else:
            for child in node.children:
                cls.findLeafStates(child)

    @classmethod
    def getLeafStatesWithoutRepetitions(cls, node : GameTree, leafList):
        if node.isLeaf():
            for i, listNode in enumerate(leafList):
                if listNode.board == node.board:
                    found = True
                    if listNode.score < node.score:
                        del leafList[i]
                        leafList.append(node)
                    break
            if not found:
                leafList.append(node)    
        else:
            for child in node.children:
                cls.getLeafStatesWithoutRepetitions(child, leafList)



