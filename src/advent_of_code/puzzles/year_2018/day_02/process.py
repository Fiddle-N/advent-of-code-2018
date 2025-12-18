
def main():
    twos = 0
    threes = 0
    with open('input.txt', 'r') as f:
        for string in f:
            is_two_found = False
            is_three_found = False
            unique = set(string)
            for char in unique:
                count = string.count(char)
                if count == 2:
                    if not is_two_found:
                        twos += 1
                        is_two_found = True
                if count == 3:
                    if not is_three_found:
                        threes += 1
                        is_three_found = True
                if is_two_found and is_three_found:
                    break
    chksum = twos * threes
    return chksum
    

print(main())