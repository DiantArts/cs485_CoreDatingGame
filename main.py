from typing import Type, TypeVar
import sys

# ENABLE_DEBUG = True
ENABLE_DEBUG = False
TAB_SIZE = 4



# =================================================== Tree definition

# Tree containing every story alternative
class TreeNode:

    # constructor
    def __init__(
        self, #: TreeNode
        string: str
    ):
        self.text = string
        self.answers = [] # user input
        self.children = [] # IA answer (TreeNode type)

    # append an answer with its child node
    def append(
        self, #: TreeNode
        answer: str,
        child #: TreeNode
    ):
        if not isinstance(child, TreeNode) and child is not None: # only accept TreeNode type
            raise ValueError("'child' object cannot be interpreted as a TreeNodes")
        self.answers.append(answer)
        self.children.append(child)

    # print the tree
    def display(
        self, #: TreeNode
        depth: int = 0
    ):
        print(self.asStr())

    # convert to string
    def __repr__(
        self
    ):
        return self.asStr()

    # convert to string
    def asStr(
        self, #: TreeNode
        depth: int = 0
    ):
        ret = (' ' * (depth * 4)) + self.text + '\n'
        for (answer, child) in zip(self.answers, self.children):
            ret += (' ' * (depth * 4)) + answer + '\n'
            if child is not None:
                ret += child.asStr(depth + 1)
        return ret

def printDebug(
    string: str
):
    if ENABLE_DEBUG:
        print(string)



# =================================================== Tree generator

# get the depth from the spaces at the begining of the line
def getDepth(
    line: str
) -> int:
    return (len(line) - len(line.lstrip())) / TAB_SIZE

# extract the answers from the current depth
def extractAnswers(
    string: str,
    depth: int,
    parent: TreeNode
) -> str:
    answers = []
    children = []

    printDebug("\t\t\t------ searching <depth:" + str(depth) + ">")
    printDebug(string)

    if getDepth(string) < depth:
        return string

    # extract current line from string into a child
    eolPos = string.find('\n')
    if eolPos < 0:
        # have text but no answer
        printDebug("\t\t\tanswer done")
        return string
    # answers.append(string[:eolPos]) # push the answer to the list of answers (tmp)
    answer = string[:eolPos].lstrip(' ') # push the answer to the list of answers (tmp)
    string = string[eolPos + 1:]
    printDebug("\t\t\t---------------------> '" + string[:eolPos] + "' <depth:" + str(depth) + ">")

    # recursively get children of current answer
    printDebug("\t\t\twhile " + str(getDepth(string)) + " > " + str(depth))
    if getDepth(string) > depth:
        while getDepth(string) > depth:
            printDebug("\t\t\twhile " + str(getDepth(string)) + " > " + str(depth))

            child, string = generateTree(string, depth + 1)
            printDebug(string)

            if child is not None:
                parent.append(answer, child)
    else:
        parent.append(answer, None)

    # check if should continue searching
    printDebug("\t\t\tif can continue searching")
    if getDepth(string) == depth:
        string = extractAnswers(string, depth, parent)

    # search is done at this depth, returning
    printDebug("\t\t\tsearch done <depth:" + str(depth) + ">")
    return string

# geneate the tree from a string (probably a file like CoreGameStory.txt)
# recurssively called by extractAnswers()
def generateTree(
    string: str,
    depth: int = 0
) -> (TreeNode, str):

    printDebug("\t\t\t===== diving <depth:" + str(depth) + ">")
    printDebug(string)

    # extract current line from string into the tree text
    eolPos = string.find('\n')
    if eolPos < 0:
        # no answers anymore, the game over if node reached
        return None, string
    tree = TreeNode(string[:eolPos].lstrip(' '))
    printDebug("\t\t\t=====================> '" + string[:eolPos].lstrip(' ') + "' <depth:" + str(depth) + ">")
    string = string[eolPos + 1:]

    # finding answers and recursively diving to generate subtrees
    string = extractAnswers(string, depth, tree)

    # node is complete, returning
    printDebug("\t\t\tdive done")
    return tree, string



# =================================================== main

def main(
) -> int:
    string = open("CoreGameStory.txt").read()
    # string = open("SimpleExampleFile.txt").read()
    printDebug(string)
    tree, _ = generateTree(string)
    if tree is None:
        raise ValueError("Invalid tree generation")
    tree.display()
    return 0

if __name__ == "__main__":
    sys.exit(main())
