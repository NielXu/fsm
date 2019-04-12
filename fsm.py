"""
This module contains high level of finite state machine. It supports
features such as storing values across each state and in the Machine.
And also support boolean comparsion transit.
"""
from simplefsm import RepeatedSignal, UnknownSignal


"This need to be defined"
ANY = None


def set_any(p):
    "Define ANY, default is None"
    global ANY
    ANY = p


def get_any():
    "Get ANY, default is None"
    return ANY


class NonTransitSignal(Exception):
    "This exception will be raised when there is no signal to go to next state"
    def __init__(self, msg):
        super().__init__(msg)


class Signal():
    "A bool expression that being stored inside the signal"
    def __init__(self, bool_expr):
        """
        bool_expr: The boolean expression, must be a function that returns True or False.
        The state will transit to next iff the bool_expr return True.

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
    def __init__(self, name, exe=lambda m:None):
        """
        name: Name of this state\n
        exe: Function that being called when it reaches this state, the defined
        function should take a dict as a argument, it contains all variables in
        the machine. The default function returns None.
        """
        self.transit_map = {}
        self.name = name
        self.exe = exe
    
    def read(self, mapper):
        """
        Different from simple fsm, this state will NOT read a signal, it will use
        the variable mapper and the internal signal to determine if transit to
        next state or not. This state will transit to next state iff the signal
        returns True.
        The idea of read is, the state will run throguh all the transits and as long
        as there is one True, it will automatically go to the state that it points to.
        """
        li = list(self.transit_map)
        for i in li:
            if i != ANY and i.on(mapper):
                return self.transit_map[i]
        if ANY is not None and ANY in self.transit_map:
            return self.transit_map[ANY]
        raise NonTransitSignal("At state: " + str(self.name)+", cannot reach next state")

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
        if signal in self.transit_map:
            raise RepeatedSignal("Signal: " + str(signal) + " is repeated in the machine")
        self.transit_map[signal] = next_state
    
    def execute(self, mapper):
        """
        Execute the function that this state contains. And return whatever the function returns
        """
        return self.exe(mapper)


class Machine():
    "The FSM"
    def __init__(self, initial_state, exit_states, mapper, machine_id="DEFAULT", exe_initial=False, exe_exit=False):
        """
        initial_state: The initial_state of the FSM\n
        exit_states: A list of exit states\n
        mapper: A dict that stores variables and pass it to each state\n
        machine_id: ID of this machine, default is 'DEFAULT'\n
        exe_initial: Execute state when starting from the initial state, default is False\n
        exe_exit: Execute state when reaches the exit state, default is False
        """
        self.initial_state = initial_state
        self.exit_states = exit_states
        self.mapper = mapper
        self.machine_id = machine_id
        self.exe_initial = exe_initial
        self.exe_exit = exe_exit
    
    def start(self):
        """
        Start the FSM
        """
        self._process(0, self.initial_state)
    
    def _process(self, index, state):
        "Process the seq"
        if index == 0:
            if self.exe_initial:
                state.execute(self.mapper)
        elif state in self.exit_states:
            if self.exe_exit:
                state.execute(self.mapper)
            return
        else:
            state.execute(self.mapper)
        next_state = state.read(self.mapper)
        self._process(index+1, next_state)
