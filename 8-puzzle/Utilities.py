#check if the puzzle can be solved or not


def is_solvable_puzzle(state):
    inversions = 0
    listState = [cell for row in state for cell in row]
    for i in range(len(listState)):
        for j in range(i+1, len(listState)):
            if listState[i] == 0 or listState[j] == 0:
                continue;
            if(listState[i] > listState[j]):
                inversions += 1
    if inversions%2 == 0:
        return True
    else:
        return False


def represents_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False