import fitz
import os

pdf_path = r'D:\AISOP\AI-Agent-Tutorial\05_Word\preview.pdf'
out_dir = r'D:\AISOP\AI-Agent-Tutorial\05_Word\pages'
os.makedirs(out_dir, exist_ok=True)

doc = fitz.open(pdf_path)
print(f'Total pages: {doc.page_count}')

# Render key pages
pages_to_check = list(range(0, min(10, doc.page_count)))
# Add some middle and end pages
for p in [20, 50, 100, 150, 200, 250, doc.page_count-1]:
    if p not in pages_to_check and p < doc.page_count:
        pages_to_check.append(p)

for p in sorted(pages_to_check):
    page = doc[p]
    pix = page.get_pixmap(dpi=80)
    out = os.path.join(out_dir, f'page_{p+1:04d}.png')
    pix.save(out)
    text = page.get_text()[:80].replace('\n', ' ')
    print(f'Page {p+1}: {pix.width}x{pix.height} | {text}')

doc.close()
print('Done')
