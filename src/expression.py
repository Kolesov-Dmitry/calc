from token import TokenType
from exprparser import ExpressionParser
from rpnconverter import RPNConverter


# Evaluate the expression
class Expression:

    @staticmethod
    def __has_token(tokens_, token_type):
        for token in tokens_:
            if token.type == token_type:
                return True
        return False

    @staticmethod
    def __solve_variable(token_value, vars_, stack_):
        if token_value not in vars_:
            raise ValueError("Unknown variable")

        stack_.append(vars_[token_value])
        return ""

    @staticmethod
    def __solve_operator(token_type, stack_):
        if len(stack_) < 2:
            raise ValueError("Invalid expression")

        a = stack_.pop()
        if token_type == TokenType.PlusOperator:
            a += stack_.pop()
        elif token_type == TokenType.MinusOperator:
            a = stack_.pop() - a
        elif token_type == TokenType.MulOperator:
            a *= stack_.pop()
        elif token_type == TokenType.DivOperator:
            a = stack_.pop() // a
        elif token_type == TokenType.PowerOperator:
            a = stack_.pop() ** a

        stack_.append(a)
        return ""

    @staticmethod
    def __solve_expression(tokens_, vars_):
        stack = []
        converter = RPNConverter()
        rpn_expr = converter.convert(tokens_)
        for token in rpn_expr:
            if token.type == TokenType.Integer:
                stack.append(int(token.value))
            elif token.type == TokenType.Variable:
                Expression.__solve_variable(token.value, vars_, stack)
            elif (token.type == TokenType.PlusOperator or token.type == TokenType.MinusOperator or
                  token.type == TokenType.MulOperator or token.type == TokenType.DivOperator or
                  token.type == TokenType.PowerOperator):
                Expression.__solve_operator(token.type, stack)
            elif token.type == TokenType.AssignOperator:
                raise ValueError("Invalid assignment")
            else:
                raise ValueError("Invalid expression")

        if len(stack) != 1:
            raise ValueError("Invalid expression")

        return str(stack[0])

    @staticmethod
    def __solve_assignment(tokens_, vars_):
        if (len(tokens_) < 3
                or tokens_[0].type != TokenType.Variable
                or tokens_[1].type != TokenType.AssignOperator):
            raise ValueError("Invalid assignment")

        try:
            var_name = tokens_[0].value
            tokens_.popleft()
            tokens_.popleft()
            r = Expression.__solve_expression(tokens_, vars_)
            vars_.update({var_name: int(r)})
        except ValueError:
            raise ValueError("Invalid assignment")

    @staticmethod
    def evaluate(expr_, vars_):
        p = ExpressionParser()
        p.parse(expr_)
        if Expression.__has_token(p.tokens, TokenType.AssignOperator):
            Expression.__solve_assignment(p.tokens, vars_)
            return ""

        return Expression.__solve_expression(p.tokens, vars_)
