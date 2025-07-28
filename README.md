# PDF Outline Extractor

This project extracts structured outlines (titles, section headings) from PDF documents and stores them in JSON format conforming to a predefined schema.

## 📂 Project Structure

```
.
├── Dockerfile
├── process_pdfs.py
├── output_schema.json
├── WG1AR5_SPM_FINAL.pdf
├── WG1AR5_SPM_FINAL.json
```

## 🧠 How It Works

1. **`process_pdfs.py`**: 
   - Extracts headings from PDF using `pdfminer.six`.
   - Categorizes them into levels: H1, H2, H3 based on font size.
   - Validates the output JSON against `output_schema.json`.

2. **`output_schema.json`**: 
   - JSON Schema ensuring structure compliance for extracted outlines.

3. **`WG1AR5_SPM_FINAL.pdf`**: 
   - Sample PDF used for outline extraction.

4. **`WG1AR5_SPM_FINAL.json`**: 
   - Output generated after processing the above PDF.

## 🐳 Docker Setup

### Build the image
```bash
docker build -t pdf-outline-extractor .
```

### Run the container
```bash
docker run -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output pdf-outline-extractor
```

- Input PDFs go into `input/`
- Output JSONs are saved to `output/`

## 📥 Sample Output Format

```json
{
  "title": "SPM",
  "outline": [
    {
      "level": "H2",
      "text": "Summary",
      "page": 1
    },
    {
      "level": "H3",
      "text": "A. Introduction",
      "page": 2
    }
  ]
}
```

## ✅ Validation

The outline JSON is validated against `output_schema.json` to ensure correctness. If validation fails, the program logs the error and skips the file.

## 🛠 Dependencies

- `pdfminer.six`
- `jsonschema`
- `python >= 3.7`

Install via pip:
```bash
pip install pdfminer.six jsonschema
```

## ✍️ Author

This utility was built to process and analyze structured outlines from scientific documents like IPCC reports.