from collections import deque
from token import TokenType


# Convert the expression from infix to Reverse Polish notation
class RPNConverter:
    def __init__(self):
        self.stack = deque()
        self.priorities = {TokenType.PlusOperator: 1, TokenType.MinusOperator: 1, TokenType.MulOperator: 2,
                           TokenType.DivOperator: 2, TokenType.PowerOperator: 3, TokenType.OpenParentheses: 0}

    def __pop_until(self, priority_, output_):
        while len(self.stack) > 0 and self.priorities[self.stack[-1].type] >= priority_:
            output_.append(self.stack.pop())

    def convert(self, tokens_):
        output = deque()
        for token in tokens_:
            if token.type == TokenType.Integer or token.type == TokenType.Variable:
                output.append(token)
            elif token.type != TokenType.OpenParentheses and token.type != TokenType.CloseParentheses:
                self.__pop_until(self.priorities[token.type], output)
                self.stack.append(token)
            elif token.type == TokenType.OpenParentheses:
                self.stack.append(token)
            elif token.type == TokenType.CloseParentheses:
                if len(self.stack) == 0:
                    raise ValueError("Invalid expression")
                while self.stack[-1].type != TokenType.OpenParentheses:
                    output.append(self.stack.pop())
                    if len(self.stack) == 0:
                        raise ValueError("Invalid expression")
                self.stack.pop()

        self.__pop_until(0, output)
        return output
