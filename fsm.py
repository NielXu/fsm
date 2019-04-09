"""
A finite state machine way of programming. The whole process will
be:
    state exec -> read -> next state
until exit state
"""


class RepeatedSignal(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class UnknownSignal(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class State():
    def __init__(self, name, exe=lambda:None):
        """
        name: Name of this state\n
        exe: Function that being called when it reaches this state, default is a
            function that do nothing and return None
        """
        self.transit_map = {}
        self.name = name
        self.exe = exe
    
    def read(self, signal):
        """
        Read a signal and return next state. If ANY signal
        is defined for this state, no matter what signal being
        passed, it will always go to a fixed next state.
        """
        if 'any' in self.transit_map:
            return self.transit_map['any']
        if signal not in self.transit_map:
            raise UnknownSignal("Unknown signal: " + str(signal))
        return self.transit_map[signal]

    def add_transit(self, signal, next_state):
        """
        Add transition to next state. If state reads a signal, it
        will go to a corresponding next state. Signals should be 
        different, i.e one signal goes to one state. However, signal
        can be defined as 'any', in this case, no matter what signal
        this state detected, it will go to next_state automatically.
            add_transit('any', next_state)
        """
        if signal in self.transit_map:
            raise RepeatedSignal("Signal: " + str(signal) + " is repeated in the machine")
        self.transit_map[signal] = next_state
    
    def execute(self):
        """
        Execute the function that this state contains
        """
        self.exe()


class Machine():
    "The FSM"
    def __init__(self, initial_state, exit_states, machine_id="DEFAULT", exe_initial=False, exe_exit=False):
        """
        initial_state: The initial_state of the FSM\n
        exit_states: A list of exit states\n
        machine_id: ID of this machine, default is 'DEFAULT'\n
        exe_initial: Execute when starting from the initial state, default is False\n
        exe_exit: Execute when reaches the exit state, default is False
        """
        self.initial_state = initial_state
        self.exit_states = exit_states
        self.machine_id = machine_id
        self.exe_initial = exe_initial
        self.exe_exit = exe_exit
    
    def start(self, seq):
        """
        Start the FSM and read the given seq. The seq should
        be a sequence(list) that matches the transitions.
        """
        self._process(seq, 0, self.initial_state)
    
    def _process(self, seq, index, state):
        "Process the seq, the first state will not be executed"
        if index == 0:
            if self.exe_initial:
                state.execute()
        elif state in self.exit_states:
            if self.exe_exit:
                state.execute()
            return
        else:
            state.execute()
        s = seq[index]
        next_state = state.read(s)
        self._process(seq, index+1, next_state)
