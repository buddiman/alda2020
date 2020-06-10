class Number:
    def __init__(self, num):
        self.value = num

class Operator:
    def __init__(self, l, o, r):
        self.left = l
        self.right = r
        self.operator = o


# Tupel to define the priority of the operators
priority = {'*': 3,
            '/': 3,     # punkt vor strich
            '+': 2,
            '-': 2,
            '(': 9,
            ')': 0}     # last


# Shunting-Yard Algorithm
def shunting_yard(infix):
    # If param is null raise exception
    if infix is None:
        raise SyntaxError

    # make a list from
    expression = list(infix)

    output, operatorStack = [], []

    for token in expression:
        # check if element is a digit
        if token.isdigit():
            output.append(token)
        # if not digit check if present in
        elif token in priority:
            while operatorStack:
                stackTop = operatorStack[-1]
                if priority[token] <= priority[stackTop]:
                    if token != ')':
                        if stackTop != '(':
                            operatorStack.pop()
                            output.append(stackTop)
                        else:
                            break
                    else:
                        if stackTop != '(':
                            operatorStack.pop()
                            output.append(stackTop)
                        else:
                            operatorStack.pop()
                            break
                else:
                    break

            if token != ')':
                operatorStack.append(token)

    while operatorStack:
        remainingItem = operatorStack[-1]
        operatorStack.pop()
        output.append(remainingItem)
    return output

def parse (input):
    shuntingYard = shunting_yard(input)

    if shuntingYard is None:
        raise SyntaxError

    stack = []

    for token in shuntingYard:
        if token in priority:
            stack.append(Operator(stack.pop(), token, stack.pop()))
        else:
            stack.append(Number(token))

    if len(stack) != 1:
        raise SyntaxError

    return stack[0]

## todo FIX THIS
def evaluateTree(root):
    if root is None:
        raise SyntaxError("tree is empty")

    # check if root is a instance of Number
    if isinstance(root, Number):
        return root.value

    leftEvaluation = int(evaluateTree(root.left))       # round to int if float
    rightEvaluation = int(evaluateTree(root.right))

    # evaluate operators
    if root.operator == '+':
        return rightEvaluation + leftEvaluation
    elif root.operator == '-':
        return rightEvaluation - leftEvaluation
    elif root.operator == '*':
        return rightEvaluation * leftEvaluation
    elif root.operator == '/':
        return rightEvaluation / leftEvaluation

if __name__ == '__main__':
    infix = '2*4*(3+(4-7)*8)-(1-6)'
    print("Converted String polish form: {}", shunting_yard(infix)) # expect 2 4 * 3 4 7 − 8 * + * 1 6 − −  YAYY works right
    converted= shunting_yard(infix)

    # 2*4*(3+(4-7)*8)-(1-6) = -163
    print(evaluateTree(parse(converted)))   # WRONG Output...