import pymupdf, os, json
from pathlib import Path

# Paths relative to this script's location
script_dir = Path(__file__).resolve().parent
repo_root = script_dir.parent
pdf_path = str(script_dir / 'preview.pdf')
out_dir = str(script_dir / 'pages_full')
audit_json = str(script_dir / 'page_audit.json')
os.makedirs(out_dir, exist_ok=True)

doc = pymupdf.open(pdf_path)
total = doc.page_count
print(f'Total pages: {total}')

results = []
for i in range(total):
    page = doc[i]
    text = page.get_text().strip()
    images = page.get_images()
    text_len = len(text)
    img_count = len(images)
    
    issues = []
    if text_len < 10 and img_count == 0:
        issues.append('BLANK_OR_NEAR_EMPTY')
    if text_len < 50 and img_count == 0 and i > 5:
        issues.append('POSSIBLY_EMPTY')
    
    results.append({
        'page': i+1,
        'text_chars': text_len,
        'images': img_count,
        'issues': issues
    })
    
    pix = page.get_pixmap(dpi=72)
    pix.save(os.path.join(out_dir, f'p{i+1:04d}.png'))

doc.close()

blanks = [r for r in results if 'BLANK_OR_NEAR_EMPTY' in r['issues']]
low_text = [r for r in results if r['text_chars'] < 100 and r['images'] == 0]
print(f'Blank/near-empty pages: {len(blanks)}')
for b in blanks:
    print(f'  Page {b["page"]}: {b["text_chars"]} chars, {b["images"]} images')
print(f'Pages with <100 chars and no images: {len(low_text)}')
for l in low_text[:20]:
    print(f'  Page {l["page"]}: {l["text_chars"]} chars')

with open(audit_json, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print('Done')
