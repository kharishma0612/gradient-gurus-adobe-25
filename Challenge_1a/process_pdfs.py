# import json
# from pathlib import Path
# import fitz  # PyMuPDF
# import re

# def extract_outline_from_pdf(pdf_path):
#     """Extracts Title, H1, H2, and H3 from PDF using font size and text patterns."""
#     doc = fitz.open(pdf_path)
#     outline = []
#     font_sizes = []

#     # Pass 1: Collect font sizes (for relative ranking)
#     for page in doc:
#         for block in page.get_text("dict")["blocks"]:
#             for line in block.get("lines", []):
#                 for span in line.get("spans", []):
#                     font_sizes.append(span["size"])

#     if not font_sizes:
#         return {"title": pdf_path.stem, "outline": []}

#     avg_font = sum(font_sizes) / len(font_sizes)
#     max_font = max(font_sizes)

#     title = None
#     seen_headings = set()

#     # Pass 2: Extract headings based on font size + heuristics
#     for page_num, page in enumerate(doc, start=1):
#         for block in page.get_text("dict")["blocks"]:
#             for line in block.get("lines", []):
#                 for span in line.get("spans", []):
#                     text = span["text"].strip()

#                     # Skip very small texts or numbers
#                     if len(text) < 3 or text.isnumeric():
#                         continue

#                     font_size = span["size"]
#                     is_bold = "bold" in span["font"].lower()
                    
#                     # Title detection: Largest font on first page
#                     if page_num == 1 and font_size >= max_font * 0.95 and not title:
#                         title = text

#                     # Heading classification (heuristics)
#                     level = None
#                     if font_size >= avg_font * 1.5 or is_bold and font_size >= avg_font * 1.3:
#                         level = "H1"
#                     elif font_size >= avg_font * 1.3:
#                         level = "H2"
#                     elif font_size >= avg_font * 1.1:
#                         level = "H3"

#                     # Regex-based heading cue (optional enhancement)
#                     if not level and re.match(r"^\d+(\.\d+)*\s+\w+", text):
#                         level = "H2"

#                     if level and text not in seen_headings:
#                         seen_headings.add(text)
#                         outline.append({
#                             "level": level,
#                             "text": text,
#                             "page": page_num
#                         })

#     doc.close()
#     return {
#         "title": title or pdf_path.stem,
#         "outline": outline
#     }

import fitz  # PyMuPDF
import json
import re
from pathlib import Path

def extract_headings(pdf_path):
    doc = fitz.open(pdf_path)
    headings = []
    font_sizes = {}
    title = None

    # Collect font sizes and styles for all text blocks
    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")['blocks']
        for b in blocks:
            if 'lines' not in b:
                continue
            for line in b['lines']:
                for span in line['spans']:
                    size = span['size']
                    font = span['font']
                    text = span['text'].strip()
                    if not text:
                        continue
                    # Track font size frequency
                    font_sizes[size] = font_sizes.get(size, 0) + 1

    # Sort font sizes descending (largest likely title/H1)
    sorted_sizes = sorted(font_sizes.keys(), reverse=True)
    if sorted_sizes:
        title_size = sorted_sizes[0]
        h1_size = sorted_sizes[0]
        h2_size = sorted_sizes[1] if len(sorted_sizes) > 1 else sorted_sizes[0]
        h3_size = sorted_sizes[2] if len(sorted_sizes) > 2 else sorted_sizes[-1]
    else:
        title_size = h1_size = h2_size = h3_size = 0

    # Second pass: extract headings
    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")['blocks']
        for b in blocks:
            if 'lines' not in b:
                continue
            for line in b['lines']:
                for span in line['spans']:
                    size = span['size']
                    font = span['font']
                    text = span['text'].strip()
                    if not text:
                        continue
                    # Heuristic: centered, largest font = title
                    if size == title_size and b.get('bbox'):
                        x0, y0, x1, y1 = b['bbox']
                        page_width = page.rect.width
                        if abs((x0 + x1)/2 - page_width/2) < page_width*0.15:
                            if not title:
                                title = text
                    # Heading detection
                    level = None
                    if size == h1_size:
                        level = "H1"
                    elif size == h2_size:
                        level = "H2"
                    elif size == h3_size:
                        level = "H3"
                    # Bold or all caps or regex pattern
                    if level and (span.get('flags', 0) & 2 or text.isupper() or re.match(r'^[A-Z][A-Za-z0-9\s\-:]+$', text)):
                        headings.append({
                            "level": level,
                            "text": text,
                            "page": page_num + 1
                        })

    # Deduplicate headings (remove repeated headers/footers)
    seen = set()
    outline = []
    for h in headings:
        key = (h['level'], h['text'])
        if key not in seen:
            outline.append(h)
            seen.add(key)

    # Fallback title
    if not title and outline:
        title = outline[0]['text']
    elif not title:
        title = Path(pdf_path).stem

    return {
        "title": title,
        "outline": outline
    }

def process_pdfs():
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    output_dir.mkdir(exist_ok=True)

    for pdf_file in input_dir.glob("*.pdf"):
        result = extract_headings(pdf_file)
        output_file = output_dir / f"{pdf_file.stem}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    process_pdfs()

if __name__ == "__main__":
    process_pdfs()
