import itertools
import collections

Claim = collections.namedtuple('Claim', 'left_coord top_coord width height')


def _create_square_grid(length):
    tuple_grid = ((0,) * length,) * length
    list_grid = list(list(row) for row in tuple_grid)
    return list_grid
    
    
def _read_claim(raw_claim):
    id, area = raw_claim.split(' @ ')
    coords, dimensions = area.split(': ')
    left_coord, top_coord = coords.split(',')
    width, height = dimensions.split('x')
    return Claim(int(left_coord), int(top_coord), int(width), int(height))
   
    
    
def _update_grid(grid, claim_ranges):
    for ranges in claim_ranges:
        top_range, left_range = ranges
        for top_idx, left_idx in itertools.product(left_range, top_range):
            grid[top_idx][left_idx] += 1


def _search_grid(grid, claim_ranges):
    for idx, ranges in enumerate(claim_ranges):
        top_range, left_range = ranges
        claim_overlap = set(
            grid[top_idx][left_idx] 
            for top_idx, left_idx in itertools.product(left_range, top_range)
        )
        if set(claim_overlap) == set([1]):
            claim_id = idx + 1
            return claim_id


def _generate_ranges(claim):
    top_range = range(claim.top_coord, claim.top_coord + claim.height)
    left_range = range(claim.left_coord, claim.left_coord + claim.width)
    return top_range, left_range


def main():
    grid = _create_square_grid(1000)
    
    claims = []
    with open('input.txt', 'r') as f:
        for raw_claim in f:
            claims.append(_read_claim(raw_claim))
    
    claim_ranges = [_generate_ranges(claim) for claim in claims]
    
    _update_grid(grid, claim_ranges)

    claim_id = _search_grid(grid, claim_ranges)
    return claim_id
    
    
print(main())
