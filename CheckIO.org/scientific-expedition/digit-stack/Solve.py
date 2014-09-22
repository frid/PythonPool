def digit_stack(commands):
    if len(commands) == 0:
        return 0
    Stack = []
    Sum = 0
    for Cmd in commands:
        if Cmd.find('PUSH') != -1:
            Stack.append(int(Cmd.split(' ')[1]))

        if Cmd.find('POP') != -1:
            if len(Stack) != 0:
                Sum += Stack.pop()

        if Cmd.find('PEEK') != -1:
            if len(Stack):
                Sum += Stack[-1]
    return Sum


if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    a = digit_stack(["PUSH 3", "POP", "POP", "PUSH 4", "PEEK",
                        "PUSH 9", "PUSH 0", "PEEK", "POP", "PUSH 1", "PEEK"])
    print a
    assert digit_stack(["PUSH 3", "POP", "POP", "PUSH 4", "PEEK",
                        "PUSH 9", "PUSH 0", "PEEK", "POP", "PUSH 1", "PEEK"]) == 8, "Example"
    assert digit_stack(["POP", "POP"]) == 0, "pop, pop, zero"
    assert digit_stack(["PUSH 9", "PUSH 9", "POP"]) == 9, "Push the button"
    assert digit_stack([]) == 0, "Nothing"
