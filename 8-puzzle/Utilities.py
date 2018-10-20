# check if the puzzle can be solved or not


def is_solvable_puzzle(state):
    inversions = 0
    list_state = [cell for row in state for cell in row]
    for i in range(len(list_state)):
        for j in range(i + 1, len(list_state)):
            if list_state[i] == 0 or list_state[j] == 0:
                continue
            if list_state[i] > list_state[j]:
                inversions += 1
    if inversions % 2 == 0:
        return True
    else:
        return False
