import os
import json
from pathlib import Path
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTChar
from jsonschema import validate, ValidationError

# Load schema once
with open("/app/schema/output_schema.json", "r", encoding="utf-8") as f:
    schema = json.load(f)

def extract_headings(pdf_path):
    candidates = []
    for page_num, layout in enumerate(extract_pages(pdf_path), start=1):
        for element in layout:
            if isinstance(element, LTTextBoxHorizontal):
                for line in element:
                    if not isinstance(line, LTChar) and hasattr(line, "get_text"):
                        text = line.get_text().strip()
                        if not text:
                            continue
                        font_sizes = [char.size for char in line if isinstance(char, LTChar)]
                        avg_font = sum(font_sizes) / len(font_sizes) if font_sizes else 0
                        candidates.append({
                            "text": text,
                            "page": page_num,
                            "font_size": avg_font,
                            "y": line.y0
                        })

    if not candidates:
        return "Untitled", []

    # Sort by font size descending, then vertical position descending
    candidates.sort(key=lambda x: (-x["font_size"], -x["y"]))

    title = candidates[0]["text"]

    # Take top 3 font sizes for H1, H2, H3
    top_fonts = sorted(set([c["font_size"] for c in candidates]), reverse=True)[:3]
    level_map = {size: f"H{i+1}" for i, size in enumerate(top_fonts)}

    outline = []
    for c in candidates[1:]:
        level = level_map.get(c["font_size"])
        if level:
            outline.append({
                "level": level,
                "text": c["text"],
                "page": c["page"]
            })

    return title, outline

def process_pdf_file(pdf_path: Path, output_dir: Path):
    try:
        title, outline = extract_headings(str(pdf_path))
        result = {
            "title": title,
            "outline": outline
        }

        # Validate against schema
        validate(instance=result, schema=schema)

        # Write to output
        output_path = output_dir / f"{pdf_path.stem}.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"✔ Processed {pdf_path.name}")
    except Exception as e:
        print(f"✖ Failed to process {pdf_path.name}: {e}")

def main():
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    for pdf in input_dir.glob("*.pdf"):
        process_pdf_file(pdf, output_dir)

if __name__ == "__main__":
    main()
