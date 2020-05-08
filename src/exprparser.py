from collections import deque
from token import TokenType, Token


# Parse the raw expression to the list of Tokens
class ExpressionParser:
    def __init__(self):
        self.tokens = deque()
        self.__has_assign = False

    def __parse_buf(self, buf_):
        if len(buf_) > 0:
            token_type = TokenType.Integer if buf_[-1].isdigit() else TokenType.Variable
            if buf_ == '-':
                token_type = TokenType.MinusOperator
            self.tokens.append(Token(token_type, buf_))
            return ""
        return buf_

    def __parse_parentheses(self, par_, buf_):
        buf = self.__parse_buf(buf_)
        if par_ == '(':
            self.tokens.append(Token(TokenType.OpenParentheses))
        else:
            self.tokens.append(Token(TokenType.CloseParentheses))
        return buf

    def __parse_operator(self, op_, buf_):
        buf = self.__parse_buf(buf_)
        if op_ == '+':
            self.tokens.append(Token(TokenType.PlusOperator))
        elif op_ == '=':
            self.tokens.append(Token(TokenType.AssignOperator))
        elif op_ == '*':
            self.tokens.append(Token(TokenType.MulOperator))
        elif op_ == '/':
            self.tokens.append(Token(TokenType.DivOperator))
        elif op_ == '^':
            self.tokens.append(Token(TokenType.PowerOperator))
        return buf

    def __parse_minus_operator(self, buf_):
        if len(buf_) == 0:
            return buf_ + '-'
        else:
            buf = self.__parse_buf(buf_)
            self.tokens.append(Token(TokenType.MinusOperator))
            return buf

    def __parse_assign_operator(self, buf_):
        buf = self.__parse_buf(buf_)
        self.tokens.append(Token(TokenType.AssignOperator))
        self.__has_assign = True
        return buf

    def __parse_digit(self, c, buf_):
        if len(buf_) == 0 or not buf_.isalpha():
            return buf_ + c
        else:
            raise ValueError("Invalid assignment" if self.__has_assign else "Invalid identifier")

    def __parse_identifier(self, c, buf_):
        if len(buf_) == 0 or buf_.isalpha():
            return buf_ + c
        else:
            raise ValueError("Invalid assignment" if self.__has_assign else "Invalid identifier")

    def __simplify(self):
        output = deque()
        for token in self.tokens:
            if len(output) > 0:
                if token.type == TokenType.MinusOperator and output[-1].type == TokenType.MinusOperator:
                    output.pop()
                    output.append(Token(TokenType.PlusOperator))
                    continue
                elif token.type == TokenType.MinusOperator and output[-1].type == TokenType.PlusOperator:
                    output.pop()
                    output.append(Token(TokenType.MinusOperator))
                    continue
                elif token.type == TokenType.PlusOperator and output[-1].type == TokenType.PlusOperator:
                    output.pop()
                    continue
                elif (token.type == TokenType.MulOperator and output[-1].type == TokenType.MulOperator) or (
                      token.type == TokenType.DivOperator and output[-1].type == TokenType.DivOperator):
                    raise ValueError("Invalid expression")

            output.append(token)
        self.tokens = output

    def parse(self, expression):
        buf = ""
        for c in expression:
            if c == '-':
                buf = self.__parse_minus_operator(buf)
            elif c == '+' or c == '=' or c == '*' or c == '/' or c == '^':
                buf = self.__parse_operator(c, buf)
            elif c == '(' or c == ')':
                buf = self.__parse_parentheses(c, buf)
            elif c == ' ':
                buf = self.__parse_buf(buf)
            elif c.isdigit():
                buf = self.__parse_digit(c, buf)
            elif c.isalpha():
                buf = self.__parse_identifier(c, buf)
        self.__parse_buf(buf)
        self.__simplify()
