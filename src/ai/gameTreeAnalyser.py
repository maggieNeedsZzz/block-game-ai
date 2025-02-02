
from ai.gameTree import GameTree
from ai.heuristic import Heuristic

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
    def getBestLeafState(cls, treeRootNode : GameTree, heuristic : Heuristic = None) -> (GameTree, int): 
        cls.findBestLeafState(treeRootNode, heuristic)
        # print("Board is: " + str(cls.bestLeaf.board.board))
        print(cls.bestLeaf.score )
        print(cls.bestLeaf.runningCombo)
        return cls.bestLeaf, cls.bestLeafScore
    
    @classmethod
    def findBestLeafState(cls, node : GameTree, heuristic : Heuristic = None): 
        if node.isLeaf():
            if heuristic != None:
                nodeScore = heuristic.calculateScore(node)
                # print()
                # print("~~~~~~~~~~~~~~~~~~")
                # print("score: " + str(node.score))
                # print("~~~~~~~~~~~~~~~~~~")
                # print()
                # print("heuristic score: " + str(nodeScore))
            else: 
                nodeScore = node.score
            
            if nodeScore > cls.bestLeafScore:
                cls.bestLeafScore = nodeScore
                cls.bestLeaf = node
        else:
            for child in node.children:
                cls.findBestLeafState(child, heuristic)

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



