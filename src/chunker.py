import re


SECTION_NAMES = [
    "PROFESSIONAL SUMMARY",
    "TECHNICAL SKILLS",
    "PROFESSIONAL EXPERIENCE",
    "PROJECTS",
    "EDUCATION",
    "CERTIFICATIONS"
]


def detect_sections(text):
    """
    Detect major resume sections and separate their content.
    """

    sections = []

    current_section = "HEADER"
    current_content = []

    lines = text.splitlines()

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.upper() in SECTION_NAMES:

            if current_content:
                sections.append({
                    "section": current_section,
                    "text": " ".join(current_content)
                })

            current_section = line.upper()
            current_content = []

        else:
            current_content.append(line)

    if current_content:
        sections.append({
            "section": current_section,
            "text": " ".join(current_content)
        })

    return sections


def create_section_chunks(
    text,
    source="Aman_Dadhich_Resume.pdf",
    max_words=500
):
    """
    Create section-aware chunks with metadata.
    """

    sections = detect_sections(text)

    chunks = []

    chunk_id = 1

    for section in sections:

        words = section["text"].split()

        if len(words) <= max_words:

            chunks.append({
                "chunk_id": chunk_id,
                "section": section["section"],
                "source": source,
                "text": section["text"]
            })

            chunk_id += 1

        else:

            for start in range(0, len(words), max_words):

                chunk_text = " ".join(
                    words[start:start + max_words]
                )

                chunks.append({
                    "chunk_id": chunk_id,
                    "section": section["section"],
                    "source": source,
                    "text": chunk_text
                })

                chunk_id += 1

    return chunks