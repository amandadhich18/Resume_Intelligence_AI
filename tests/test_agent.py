from src.agent import ResumeAgent
from src.text_cleaner import extract_and_clean_pdf
from src.chunker import create_section_chunks
from src.embeddings import load_embedding_model, generate_embeddings


print("=" * 60)
print("RESUME AGENT TEST")
print("=" * 60)


# ==========================================
# 1. LOAD RESUME
# ==========================================

PDF_PATH = "Data/Resume/Aman_Dadhich_Resume.pdf"

print("\nLoading resume...")

text = extract_and_clean_pdf(PDF_PATH)

chunks = create_section_chunks(text)

print(f"Resume sections: {len(chunks)}")


# ==========================================
# 2. LOAD EMBEDDING MODEL
# ==========================================

print("\nLoading embedding model...")

model = load_embedding_model()


# ==========================================
# 3. CREATE EMBEDDINGS
# ==========================================

texts = [
    chunk["text"]
    for chunk in chunks
]

embeddings = generate_embeddings(
    model,
    texts
)

print(
    f"Embedding shape: {embeddings.shape}"
)


# ==========================================
# 4. CREATE RESUME AGENT
# ==========================================

print("\nCreating Resume Agent...")

agent = ResumeAgent(
    chunks=chunks,
    embeddings=embeddings,
    model=model
)

print("✅ Resume Agent created successfully")


# ==========================================
# 5. TEST QUESTION
# ==========================================

question = "Where does Aman currently work?"

print("\n" + "-" * 60)
print("QUESTION")
print("-" * 60)

print(question)


# ==========================================
# 6. ASK AGENT
# ==========================================

print("\nRunning Agent...")

result = agent.answer_question(question)


# ==========================================
# 7. DISPLAY RESULT
# ==========================================

print("\n" + "=" * 60)
print("AGENT RESULT")
print("=" * 60)

print(result)


print("\n" + "=" * 60)
print("AGENT TEST COMPLETED")
print("=" * 60)