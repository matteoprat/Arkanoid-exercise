from arka_settings import *
      
def get_level_map(level):
    level_array = []
    total_blocks = 0
    with open("levels/level_"+str(level)+".txt", "r") as f:
        for i, line in enumerate(f):
            for j, char in enumerate(line):
                if char != "." and char != "\n":
                    level_array.append((char, j * BLK_WIDTH + MARGIN_LEFT, i * BLK_HEIGHT + MARGIN_TOP))
    return level_array

def get_bricks_to_destroy(blocks):
    c = 0
    for block in blocks:
        if block[0] != "G":
            c += 1 
    return c