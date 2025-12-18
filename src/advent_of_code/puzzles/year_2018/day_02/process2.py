import itertools

def main():
    with open('input.txt', 'r') as f:
        box_ids = f.readlines()
    
    for box_id_1, box_id_2 in itertools.combinations(box_ids, 2):
        differences = 0
        for char_idx, (char1, char2) in enumerate(zip(box_id_1, box_id_2)):
            if char1 != char2:
                differences += 1
                last_idx = char_idx
        if differences == 1:
            box_id_1_allege = box_id_1[:last_idx] + box_id_1[last_idx+1:]
            box_id_2_allege = box_id_2[:last_idx] + box_id_2[last_idx+1:]
            assert box_id_1_allege == box_id_2_allege
            transformed_box_id = box_id_1_allege
            return transformed_box_id
                

print(main())