from typing import Type, TypeVar
import sys

TAB_SIZE = 4



# =================================================== Tree definition

# Tree containing every story alternative
class TreeNode:
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
        if not isinstance(child, TreeNode): # only accept TreeNode type
            raise ValueError("'child' object cannot be interpreted as a TreeNodes")
        self.answers.append(answer)
        self.children.append(child)

    def display(
        self, #: TreeNode
        depth: int = 0
    ):
        print(' ' * depth * 4 + self.text)
        for (answer, child) in zip(self.answers, self.children):
            print(' ' * depth * 4 + answer)
            child.display(depth + 1)



# =================================================== Tree generator

# get the depth from the spaces at the begining of the line
def getDepth(
    line: str
) -> int:
    return (len(line) - len(line.lstrip())) / TAB_SIZE

# extract the answers from the current depth
def extractAnswers(
    string: str,
    depth: int
) -> ([str], [TreeNode], str):
    answers = []
    children = []

    print("\t\t\t------ searching (depth " + str(depth) + ")")
    print(string)

    # extract current line from string into a child
    eolPos = string.find('\n')
    if eolPos < 0:
        # have text but no answer
        print("\t\t\tanswer done")
        return answers, children, string
    answers.append(string[:eolPos]) # contains the answer
    # tree = TreeNode(currentLine)
    string = string[eolPos + 1:]
    print("\t\t\t---------------------> '" + string[:eolPos] + "' (depth " + str(depth) + ")")

    # recursively get children of current answer
    print("\t\t\twhile " + str(getDepth(string)) + " > " + str(depth))
    while getDepth(string) > depth:
        print("\t\t\twhile " + str(getDepth(string)) + " > " + str(depth))

        child, string = generateTree(string, depth + 1)
        print(string)

        if child is not None:
            children.append(child)

    print("\t\t\tif can continue searching")
    if getDepth(string) == depth:
        retAnswers, retChildren, string = extractAnswers(string, depth)
        for answer in retAnswers:
            answers.append(answer)
        for child in retChildren:
            children.append(child)
    print("\t\t\tsearch done (depth " + str(depth) + ")")
    return answers, children, string

# geneate the tree from a string (probably a file like CoreGameStory.txt)
# recurssively called by extractAnswers()
def generateTree(
    string: str,
    depth: int = 0
) -> (TreeNode, str):

    print("\t\t\t===== diving (depth " + str(depth) + ")")
    print(string)

    # extract current line from string into the tree text
    eolPos = string.find('\n')
    if eolPos < 0:
        # no answers anymore, the game over if node reached
        return None, string
    currentLine = string[:eolPos]
    tree = TreeNode(currentLine)
    print("\t\t\t=====================> '" + currentLine + "' (depth " + str(depth) + ")")
    string = string[eolPos + 1:]

    # finding answers and recursively diving to generate subtrees
    answers, children, string = extractAnswers(string, depth)
    print(answers)
    print(children)
    for answer, child in zip(answers, children):
        if answer is not None and child is not None:
            tree.append(answer, child)

    print("\t\t\tdive done")
    return tree, string



# =================================================== main

def main(
) -> int:
    # string = open("CoreGameStory.txt").read()
    string = open("SimpleExampleFile.txt").read()
    print(string)
    tree, _ = generateTree(string)
    if tree is None:
        raise ValueError("Invalid tree generation")
    tree.display()
    return 0

if __name__ == "__main__":
    sys.exit(main())
