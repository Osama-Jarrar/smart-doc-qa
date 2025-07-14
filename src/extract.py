import os
import pdfplumber
import docx
from bs4 import BeautifulSoup
import pandas as pd

def extract_text(file_path: str) -> str:
    """
    Extracts clean text from PDF, DOCX, HTML, XLSX, or CSV files.
    Returns empty string if format unsupported or extraction fails.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    try:
        if ext == ".pdf":
            return _extract_pdf(file_path)
        elif ext == ".docx":
            return _extract_docx(file_path)
        elif ext in [".html", ".htm"]:
            return _extract_html(file_path)
        elif ext == ".xlsx":
            return _extract_excel(file_path)
        elif ext == ".csv":
            return _extract_csv(file_path)
        else:
            print(f"[WARN] Unsupported file type: {ext}")
            return ""
    except Exception as e:
        print(f"[ERROR] Extraction failed for {file_path}: {e}")
        return ""

def _extract_pdf(path: str) -> str:
    with pdfplumber.open(path) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    return text.strip()

def _extract_docx(path: str) -> str:
    doc = docx.Document(path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()

def _extract_html(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        return "\n".join(t.get_text(strip=True) for t in soup.find_all(["h1", "p", "li", "table"]))

def _extract_excel(path: str) -> str:
    df_dict = pd.read_excel(path, sheet_name=None)
    output = []
    for sheet, df in df_dict.items():
        output.append(f"--- Sheet: {sheet} ---\n")
        output.append(df.to_csv(index=False))
    return "\n".join(output)

def _extract_csv(path: str) -> str:
    df = pd.read_csv(path)
    return df.to_csv(index=False)
