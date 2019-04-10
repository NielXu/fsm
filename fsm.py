"""
This module contains high level of finite state machine. It supports
features such as storing values across each state and in the Machine.
And also support boolean comparsion transit.
"""
class Signal():
    "A bool expression that being stored inside the signal"
    def __init__(self, bool_expr):
        """
        bool_expr: The boolean expression, must be a function that takes one or
        more variable and return True or False. The state will transit to next iff the
        bool_expr return True.

        Please notice that the bool_expr function's will take a map that
        have variables being stored in the Machine in order to do comparsion.
        """
        self.bool_expr = bool_expr
    
    def on(self, mapper):
        "Turn this signal on"
        return self.bool_expr(mapper)
    
    def __str__(self):
        return "{Signal, function=" + str(self.bool_expr)+"}"
    
    def __repr__(self):
        return self.__str__()