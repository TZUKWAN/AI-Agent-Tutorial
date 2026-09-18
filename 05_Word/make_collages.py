from PIL import Image
import os

pages_dir = r'D:\AISOP\AI-Agent-Tutorial\05_Word\pages_full'
collage_dir = r'D:\AISOP\AI-Agent-Tutorial\05_Word\collages'
os.makedirs(collage_dir, exist_ok=True)

# Get all page images sorted
pages = sorted([f for f in os.listdir(pages_dir) if f.endswith('.png')])
print(f'Total pages: {len(pages)}')

# Create collages of 8 pages each (4x2 grid)
COLS, ROWS = 4, 2
PAGES_PER = COLS * ROWS

for batch_start in range(0, len(pages), PAGES_PER):
    batch = pages[batch_start:batch_start + PAGES_PER]
    if not batch:
        break
    
    # Load first image to get dimensions
    imgs = [Image.open(os.path.join(pages_dir, p)) for p in batch]
    w, h = imgs[0].size
    
    # Scale down
    scale = 0.25
    sw, sh = int(w * scale), int(h * scale)
    
    collage = Image.new('RGB', (sw * COLS, sh * ROWS), 'white')
    for idx, img in enumerate(imgs):
        r, c = divmod(idx, COLS)
        img_resized = img.resize((sw, sh), Image.LANCZOS)
        collage.paste(img_resized, (c * sw, r * sh))
    
    out_name = f'collage_{batch_start+1:04d}_{batch_start+len(batch):04d}.png'
    collage.save(os.path.join(collage_dir, out_name))
    print(f'Created {out_name} ({len(batch)} pages)')

print('Done')
