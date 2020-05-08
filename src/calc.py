from expression import Expression


class Calc:
    def __init__(self):
        self.vars_dict = {}

    @staticmethod
    def __handle_command(command_):
        if command_ == "/exit":
            print("Bye!")
            return True
        elif command_ == "/help":
            print("The program calculates the sum of numbers")
        else:
            print("Unknown command")
        return False

    def __handle_expression(self, expr):
        if len(expr) > 0:
            e = Expression()
            try:
                result = e.evaluate(expr, self.vars_dict)
                if len(result) > 0:
                    print(result)
            except ValueError as e:
                print(str(e))

    def start(self):
        stop = False
        while not stop:
            user_input = input("> ").strip()
            # check commands
            if user_input.startswith('/'):
                stop = self.__handle_command(user_input)
            else:
                self.__handle_expression(user_input)
