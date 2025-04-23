import random

def calculate_overlap(word, row, col, direction, grid):
    overlap = 0
    for i, ch in enumerate(word):
        r = row + (i if direction == 'V' else 0)
        c = col + (i if direction == 'H' else 0)
        if grid[r][c] == ch:
            overlap += 1
    return overlap

def generate_crossword(model, difficulty):
    size_map = {'Лёгкий': (10, 0), 'Средний': (15, 2), 'Сложный': (20, 4)}
    model.size, min_overlap = size_map[difficulty]
    grid = [[' ']*model.size for _ in range(model.size)]

    for word_entry in model.word_list:
        word = word_entry.word
        best_position = None
        best_overlap = -1

        for _ in range(100):
            direction = random.choice(['H', 'V'])
            if direction == 'H':
                row = random.randint(0, model.size - 1)
                col = random.randint(0, model.size - len(word))
            else:
                row = random.randint(0, model.size - len(word))
                col = random.randint(0, model.size - 1)

            can_place = True
            for i, ch in enumerate(word):
                r = row + (i if direction == 'V' else 0)
                c = col + (i if direction == 'H' else 0)
                if grid[r][c] not in [' ', ch]:
                    can_place = False
                    break

            if can_place:
                overlap = calculate_overlap(word, row, col, direction, grid)
                if overlap >= min_overlap and overlap > best_overlap:
                    best_position = (row, col, direction)
                    best_overlap = overlap

        if best_position:
            row, col, direction = best_position
            for i, ch in enumerate(word):
                r = row + (i if direction == 'V' else 0)
                c = col + (i if direction == 'H' else 0)
                grid[r][c] = ch

    model.grid = grid
