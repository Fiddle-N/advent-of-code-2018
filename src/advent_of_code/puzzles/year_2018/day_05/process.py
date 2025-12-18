import string


def _check_upper_or_lower(char1, char2):
    return char1.swapcase() == char2


def process_polymer(inpt):
    output = []
    for char in inpt:
        if output and _check_upper_or_lower(char, output[-1]):
            output.pop()
        else:
            output.append(char)
    return ''.join(output)
            

def main():
    with open('input.txt', 'r') as f:
        inpt = f.read().rstrip()
    output = process_polymer(inpt)
    print(f'Puzzle_1 {len(output)}')
    
    alleges = {
        char: len(process_polymer(output.replace(char, '').replace(char.upper(), '')))
        for char in string.ascii_lowercase
    }
    print(f'Puzzle_2 {min(alleges.values())}')


if __name__ == '__main__':
    main()
