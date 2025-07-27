
# **Adobe India Hackathon 2025 - Connecting the Dots**  
**Team: Gradient Gurus**  
**Submission Date: July 28, 2025**  

---

## **Project Overview**  
We reimagined the humble PDF as an intelligent, interactive companion—transforming static documents into dynamic tools that understand structure, surface insights, and connect ideas seamlessly.  

Our solution tackles **Round 1A** by extracting structured outlines (titles, headings) from PDFs with high accuracy and speed. For **Round 1B**, we built a persona-driven document intelligence system that prioritizes relevant sections based on user roles (e.g., researchers, students, analysts).  

**Key Innovations:**  
✔ **Smart Outline Extraction** – Automatically detects titles, headings (H1-H3), and page numbers.  
✔ **Persona-Centric Analysis** – Identifies and ranks key sections tailored to specific user needs.  
✔ **Fast & Efficient** – Runs entirely offline, optimized for performance under strict constraints.  

---

## **How It Works**  

### **Round 1A: PDF Structure Extraction**  
1. **Input:** A PDF file (up to 50 pages).  
2. **Processing:** Our system analyzes the document’s hierarchy, detecting titles and headings.  
3. **Output:** A clean JSON outline with headings, levels, and page numbers.  

**Example Output:**  
```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
```

### **Round 1B: Persona-Driven Intelligence**  
1. **Input:** A collection of PDFs + a persona (e.g., "PhD Researcher") and their task (e.g., "Literature Review").  
2. **Processing:** Our system scans documents, extracts relevant sections, and ranks them by importance.  
3. **Output:** A structured JSON with prioritized content, refined text, and metadata.  

**Example Use Case:**  
- **Persona:** *Investment Analyst*  
- **Task:** *"Analyze revenue trends from annual reports."*  
- **Output:** Extracts and ranks financial sections, R&D investments, and market strategies.  

---

## **Why Our Solution Stands Out**  
✅ **Accuracy:** Advanced parsing ensures precise heading detection, even in complex layouts.  
✅ **Speed:** Processes 50-page PDFs in under 10 seconds (Round 1A) and document sets in ≤60 seconds (Round 1B).  
✅ **User-Centric:** Goes beyond generic extraction to deliver insights tailored to real-world needs.  

---

## **Technical Implementation**  
- **Lightweight & Offline:** No internet dependencies; runs on CPU within 200MB memory (Round 1A).  
- **Scalable Architecture:** Modular design allows easy extension for future enhancements.  

---

## **Future Possibilities**  
🔮 **Semantic Search** – Enable natural language queries across document libraries.  
🔮 **Collaborative Annotations** – Let users highlight and share connected insights.  

---

**Gradient Gurus** – Bridging documents and intelligence, one dot at a time.  

--- 

### **Appendix**  
For full code, Dockerfiles, and sample outputs, visit our private repository (to be made public post-deadline).  

--- 

