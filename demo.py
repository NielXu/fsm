"""
This is an example of using FSM to compute number of tosses required
for getting HT (consecutively).

The result that I get is it requires 5 times in average. But the actual
expected tosses are 4 times. It might because the sequences were generated
beforehand and also the random number from computer is not so random.
"""
from fsm import State, Machine


# Modify this to test more or less
test_num = 10000
total_toss = 0
n = 0


def toss(max_length=25):
    import random
    s = ""
    for _ in range(max_length):
        rand = random.randint(0, 1)
        if rand == 0:
            s += "H"
        else:
            s += "T"
    return s


def increment():
    global n
    n += 1


def expect_test():
    global n
    n = 0

    s0 = State("start")
    s1 = State("s0", exe=increment)
    s2 = State("s1", exe=increment)
    s3 = State("exit", exe=increment)
    s0.add_transit("H", s1)
    s0.add_transit("T", s1)

    s1.add_transit("T", s1)
    s1.add_transit("H", s2)
    s2.add_transit("H", s2)
    s2.add_transit("T", s3)
    seq = toss()

    fsm = Machine(s0, [s3], exe_exit=True)
    fsm.start(seq)


if __name__ == "__main__":
    for _ in range(test_num):
        expect_test()
        total_toss += n
    print(total_toss)
    print("Average:", total_toss/test_num)
