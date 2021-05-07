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
    

def _update_grid(grid, ranges):
    top_range, left_range = ranges
    for top_idx, left_idx in itertools.product(left_range, top_range):
        grid[top_idx][left_idx] += 1



def _generate_ranges(claim):
    top_range = range(claim.top_coord, claim.top_coord + claim.height)
    left_range = range(claim.left_coord, claim.left_coord + claim.width)
    return top_range, left_range


def _collate_overlaps(grid):
    return sum((square >= 2) for row in grid for square in row) 


def main():
    grid = _create_square_grid(1000)
    
    claims = []
    with open('input.txt', 'r') as f:
        for raw_claim in f:
            claims.append(_read_claim(raw_claim))
    
    claim_ranges = (_generate_ranges(claim) for claim in claims)
    
    for ranges in claim_ranges:
        _update_grid(grid, ranges)

    overlaps = _collate_overlaps(grid)
    return overlaps
    
    
print(main())
