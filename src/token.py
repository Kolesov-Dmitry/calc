from enum import Enum


class TokenType(Enum):
    Integer = 1
    Variable = 2
    AssignOperator = 3
    PlusOperator = 4
    MinusOperator = 5
    MulOperator = 6
    DivOperator = 7
    PowerOperator = 8
    OpenParentheses = 9
    CloseParentheses = 10


class Token:
    def __init__(self, type_, value_=""):
        self.type = type_
        self.value = value_

    def __repr__(self):
        return f"{self.value}" if self.type == TokenType.Integer else f"{self.type}"
