import re
import pymupdf


def extract_text_from_pdf(pdf_path):
    """
    Extract text from every page of a PDF.
    """

    document = pymupdf.open(pdf_path)

    all_text = []

    for page in document:
        text = page.get_text()
        all_text.append(text)

    document.close()

    return "\n".join(all_text)


def clean_text(text):
    """
    Clean extracted PDF text.
    """

    # Replace multiple spaces/tabs with a single space
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Remove spaces at the beginning/end of each line
    text = "\n".join(
        line.strip()
        for line in text.splitlines()
    )

    # Remove leading/trailing whitespace
    text = text.strip()

    return text


def extract_and_clean_pdf(pdf_path):
    """
    Extract text from PDF and clean it.
    """

    raw_text = extract_text_from_pdf(pdf_path)

    cleaned_text = clean_text(raw_text)

    return cleaned_text