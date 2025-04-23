from PIL import Image, ImageDraw

def export_to_image(model, path):
    cell_size = 40
    size = model.size * cell_size
    img = Image.new('RGB', (size, size), color='white')
    draw = ImageDraw.Draw(img)

    for i in range(model.size):
        for j in range(model.size):
            x0, y0 = j * cell_size, i * cell_size
            x1, y1 = x0 + cell_size, y0 + cell_size
            draw.rectangle([x0, y0, x1, y1], outline='black')
            ch = model.grid[i][j]
            if ch != ' ':
                draw.text((x0 + 12, y0 + 10), ch, fill='black')

    img.save(path)
