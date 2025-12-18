import itertools
import collections

Claim = collections.namedtuple('Claim', 'claim_id left_coord top_coord width height')

    
def _read_claim(raw_claim):
    raw_id, area = raw_claim.split(' @ ')
    _, claim_id = raw_id.split('#')
    coords, dimensions = area.split(': ')
    left_coord, top_coord = coords.split(',')
    width, height = dimensions.split('x')
    return Claim(int(claim_id), int(left_coord), int(top_coord), int(width), int(height))
    

def _calculate_coords(claim):
    top_range = range(claim.top_coord, claim.top_coord + claim.height)
    left_range = range(claim.left_coord, claim.left_coord + claim.width)
    return list(itertools.product(left_range, top_range))


def _collate_overlaps(counts):
    return sum((count >= 2) for count in counts.values()) 


def _calculate_no_overlap(counts, grouped_coords, claims):
    for idx, groups in enumerate(grouped_coords):
        if all(counts[coord] == 1 for coord in groups):
            claim = claims[idx]
            return claim.claim_id


def main():
    claims = []
    with open('input.txt', 'r') as f:
        for raw_claim in f:
            claims.append(_read_claim(raw_claim))
            
    grouped_coords = [_calculate_coords(claim) for claim in claims]
    coords = [coord for groups in grouped_coords for coord in groups]

    counts = collections.Counter(coords)
    
    print(f'Solution 1: {_collate_overlaps(counts)}')
    print(f'Solution 2: {_calculate_no_overlap(counts, grouped_coords, claims)}')
    
    
main()
