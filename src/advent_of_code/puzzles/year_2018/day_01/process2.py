import itertools

def main():
    freqs = []
    with open('input.txt', 'r') as f:
        for freq_str in f:
            freqs.append(int(freq_str))
    
    freq_pool = itertools.cycle(freqs)
    cum_freq_pool = itertools.accumulate(freq_pool)
    seen_freqs = set()

    for iteration, freq in enumerate(cum_freq_pool):
        if freq in seen_freqs:
            return f'freq: {freq}; iteration: {iteration}'
        seen_freqs.add(freq)


print(main())