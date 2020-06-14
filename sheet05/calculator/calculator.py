'''
AlDa Blatt 05
Christopher Höllriegl, Marvin Schmitt

Aufgabe 2
'''

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class Number:
    def __init__(self, value):
        self.value = value


class Operator:
    def __init__(self, operator):
        self.operator = operator
        self.left = None
        self.right = None


# Operator Priority
priority = {
    '(': 0,     # Note: not higher than the others
    ')': 0,
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2
}


def shuntingYard(expression):
    '''
    converts an infix expression to reverse polish notation using the shunting yard algorithm
    https://de.wikipedia.org/wiki/Shunting-yard-Algorithmus
    :param expression: infix expression
    :return: expression as reverse polish notation
    '''
    stack = []
    output = []

    for token in expression:
        # Append digits without further processing
        if token.isdigit():
            output.append(token)

        # process operators
        else:
            # if last element then append directly
            if len(stack) == 0:
                stack.append(token)
            else:
                # handle brackets
                if token == "(":
                    stack.append(token)
                elif token == ")":
                    while stack[len(stack) - 1] != "(":
                        output.append(stack.pop())
                    stack.pop()

                # check if token has higher priority
                elif priority[token] > priority[stack[len(stack) - 1]]:
                    stack.append(token)
                else:
                    while len(stack) != 0:
                        # everything up to opening bracket
                        if stack[len(stack) - 1] == '(':
                            break
                        output.append(stack.pop())
                    stack.append(token)

    # move temporary stack to a return value
    # just to be sure, every element for it self. Forgot this :-/
    while len(stack) != 0:
       output.append(stack.pop())

    return output



def parse(s):
    '''
    create a tree from an expression.
    :param s: expression
    :return: root node of the tree
    '''
    # Create reverse polish notation from the expression
    rpn = shuntingYard(s)

    # tracking stack
    stack = []

    # Now parse every element
    for token in rpn:
        # check if element is a digit, then create a node
        if token.isdigit():
            node = Number(token)
            stack.append(node)

        # process operators
        else:
            # create a node and get the children from the stack
            node = Operator(token)
            node.right = stack.pop()
            node.left = stack.pop()

            # put the node on the stack
            stack.append(node)

    # return the root (last on the stack) node
    return stack.pop()


def evaluateTree(root):
    '''
    evaluate the tree and calculate the solution
    :param root: Root node of the tree
    :return: Solution
    '''

    # check for empty nodes
    if root is None:
        return None

    # if the Node is just a number, return
    if isinstance(root, Number):
        return int(root.value)  # compiler says to cast here...

    # now handle the operators. Recursion yeahhh
    elif isinstance(root, Operator):
        if root.operator == '*':
            return evaluateTree(root.left) * evaluateTree(root.right)
        elif root.operator == '/':
            return evaluateTree(root.left) / evaluateTree(root.right)
        elif root.operator == '+':
            return evaluateTree(root.left) + evaluateTree(root.right)
        elif root.operator == '-':
            return evaluateTree(root.left) - evaluateTree(root.right)
        else:
            raise RuntimeError("Operator not found.")

    # throw an error if there is a problem with the tree (unsupported elements)
    else:
        raise RuntimeError("Unsupported character used!")

if __name__ == "__main__":
    print("Expression: 2*4*(3+(4-7)*8)-(1-6):")
    print("Reverse polish notation: ", shuntingYard("2*4*(3+(4-7)*8)-(1-6)"))
    tree = parse("2*4*(3+(4-7)*8)-(1-6)")
    print("Evaluation: ", evaluateTree(tree))
    print("\n")
    print("Expression: 2+5*3:")
    print("Reverse polish notation: ", shuntingYard("2+5*3"))
    tree = parse("2+5*3")
    print("Evaluation: ", evaluateTree(tree))