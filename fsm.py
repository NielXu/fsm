"""
This module contains high level of finite state machine. It supports
features such as storing values across each state and in the Machine.
And also support boolean comparsion transit.
"""
from simplefsm import RepeatedSignal, UnknownSignal


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


class State():
    "A state representation on fsm"
    def __init__(self, name, exe=lambda :None):
        """
        name: Name of this state\n
        exe: Function that being called when it reaches this state, default is a
            function that takes no argument and return None.
        """
        self.transit_map = {}
        self.name = name
        self.exe = exe
    
    def read(self, mapper):
        """
        Different from simple fsm, this state will NOT read a signal, it will use
        the variable mapper and the internal signal to determine if transit to
        next state or not. This state will transit to next state iff the signal
        returns True
        """

    def add_transit(self, signal, next_state):
        """
        Add transition to next state. If state reads a signal, it
        will go to a corresponding next state. Signals should be 
        different, i.e one signal goes to one state. However, signal
        can be defined as ANY, in this case, if the signal is unknown
        for this state, it will automatically go to the state that ANY points to.
        The ANY can be changed directly since it is a global variable.
        Default is: ANY = "*"
            add_transit(ANY, next_state)
        """
    
    def execute(self):
        """
        Execute the function that this state contains. And return whatever the function returns
        """
        return self.exe()