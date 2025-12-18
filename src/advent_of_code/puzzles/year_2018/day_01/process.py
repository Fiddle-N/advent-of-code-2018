 
l = []
 
with open('input.txt', 'r') as f:
    for freq in f:
        l.append(int(freq))

print(sum(l))