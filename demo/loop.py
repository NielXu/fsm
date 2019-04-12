"""
This is an example of how to make a loop using fsm
"""
import sys
sys.path.append("..")
from fsm import State, Machine, Signal, set_any, get_any

# Loop from 1 to 10
mapper = {"a":1, "k":10}


def foo(mapper):
    if mapper["a"] < mapper["k"]:
        return False
    return True

def incre(mapper):
    print("Looping:", mapper["a"])
    mapper["a"] += 1


set_any("*")

start = State("Start")
s0 = State("Loop", exe=incre)
end = State("End")

# Start state go to s0 directly
start.add_transit(get_any(), s0)
# Define bool expr
sin0 = Signal(foo)

# Define two transits, if a >= k go to end
# Otherwise, go back to itself
s0.add_transit(sin0, end)
s0.add_transit(get_any(), s0)

m = Machine(start, [end], mapper)
m.start()
