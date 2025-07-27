import json
from pathlib import Path
import fitz  # PyMuPDF
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Try to use MiniLM if installed
try:
    from sentence_transformers import SentenceTransformer
    USE_MINILM_AVAILABLE = True
except ImportError:
    USE_MINILM_AVAILABLE = False

# -----------------------------
# PDF TEXT EXTRACTION
# -----------------------------
def extract_sections(pdf_path):
    """Extract sections/paragraphs with page mapping."""
    doc = fitz.open(pdf_path)
    sections = []

    for page_num, page in enumerate(doc, start=1):
        text_blocks = page.get_text("blocks")
        for block in text_blocks:
            text = block[4].strip()
            if len(text.split()) > 5:  # Skip very short lines
                sections.append({
                    "document": pdf_path.name,
                    "text": text,
                    "page_number": page_num
                })
    doc.close()
    return sections

# -----------------------------
# TF-IDF / BM25 BASED RANKING
# -----------------------------
def rank_sections_tfidf(sections, query, top_n=5):
    corpus = [s["text"] for s in sections]
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(corpus + [query])
    sim_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()
    ranked_indices = np.argsort(sim_scores)[::-1][:top_n]
    return [(sections[i], sim_scores[i]) for i in ranked_indices]

# -----------------------------
# MiniLM SEMANTIC RANKING
# -----------------------------
def rank_sections_minilm(sections, query, top_n=5):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    corpus = [s["text"] for s in sections]
    embeddings = model.encode(corpus + [query])
    sim_scores = cosine_similarity([embeddings[-1]], embeddings[:-1]).flatten()
    ranked_indices = np.argsort(sim_scores)[::-1][:top_n]
    return [(sections[i], sim_scores[i]) for i in ranked_indices]

# -----------------------------
# MAIN PROCESSING
# -----------------------------
def process_persona(input_json_path, method="tfidf"):
    with open(input_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    persona = data["persona"]["role"]
    job = data["job_to_be_done"]["task"]
    query = f"{persona} needs to {job}"

    # Collect all sections from PDFs inside /app/input/PDFs
    pdf_dir = Path("/app/input/PDFs")
    sections = []
    for pdf_file in pdf_dir.glob("*.pdf"):
        sections.extend(extract_sections(pdf_file))

    # Rank sections
    if method == "minilm" and USE_MINILM_AVAILABLE:
        ranked_sections = rank_sections_minilm(sections, query)
    else:
        ranked_sections = rank_sections_tfidf(sections, query)

    # Prepare output JSON
    output = {
        "metadata": {
            "input_documents": [s["document"] for s in sections],
            "persona": persona,
            "job_to_be_done": job
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }

    for rank, (section, score) in enumerate(ranked_sections, start=1):
        output["extracted_sections"].append({
            "document": section["document"],
            "section_title": section["text"][:60] + "...",
            "importance_rank": rank,
            "page_number": section["page_number"]
        })
        refined_text = " ".join(re.split(r'(?<=[.!?]) +', section["text"])[:2])
        output["subsection_analysis"].append({
            "document": section["document"],
            "refined_text": refined_text,
            "page_number": section["page_number"]
        })

    # Save output
    output_path = Path("/app/output/challenge1b_output.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"✅ Processed → {output_path}")

if __name__ == "__main__":
    input_path = Path("/app/input/challenge1b_input.json")
    process_persona(input_path, method="minilm")  # change to "tfidf" if needed
