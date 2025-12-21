# Mini Unified Data Intelligence Engine

A beginner-friendly **enterprise data intelligence prototype** that ingests structured and unstructured data, builds semantic and graph-based indexes, and answers user questions using an **AI-powered agent with intelligent tool routing**.

This project demonstrates how modern data systems combine **SQL databases, vector search, knowledge graphs, and LLM agents** into a unified intelligence layer.

---

## 🚀 Project Scope

This system can:

- Ingest structured data (CSV / spreadsheets) into **DuckDB**
- Parse unstructured data (PDFs, emails) into clean text with metadata
- Generate embeddings and store them in a **vector database**
- Perform **hybrid retrieval** (SQL + semantic search)
- Build a **knowledge graph** with entities and relationships
- Use a **LangChain agent** to automatically choose the best tool to answer a query

---

## 🧠 Architecture Overview

### Data Sources
- CSV / Spreadsheets → DuckDB
- PDFs / Emails → Text + Metadata

### Storage & Indexes
- DuckDB → Structured analytics
- Qdrant → Semantic vector search

### Intelligence Layer
- LangChain tools (SQL, Vector, Graph)
- Agent with routing logic
- Trace logging for observability

---

## 📁 Project Structure

```text
project/
│
├── ingest/
│   ├── load_structured.py        # Load CSVs into DuckDB
│   ├── parse_unstructured.py     # Parse PDFs and emails
│
├── tools/
│   ├── embedding.py              # Chunking + embedding generation
│   ├── router.py                 # Hybrid retrieval fallback logic
│
├── retrievers/
│   ├── sql.py                    # DuckDB SQL retriever
│   ├── vector.py                 # Qdrant vector retriever
│   ├── graph.py                  # Neo4j graph queries
│
├── agents/
│   └── router_agent.py           # LangChain agent with tool routing
│
├── config/
│   ├── settings.py               # Constants, paths, API keys
│
├── data/
│   ├── raw/                      # Original CSV, PDF, EML files
│   ├── processed/                # Parsed JSON / cleaned outputs
│
├── notebooks/
│   └── testing.ipynb             # Query and retrieval testing
│
├── requirements.txt
└── README.md

---

## ✅ Conclusion

The **Mini Unified Data Intelligence Engine** demonstrates how modern enterprise data systems can be designed by unifying **structured analytics, semantic search, knowledge graphs, and LLM-driven agents** into a single intelligent layer.

Through this project, we successfully built an end-to-end prototype capable of:
- Handling both structured and unstructured data sources
- Enabling hybrid retrieval using SQL and vector-based search
- Representing relationships and entities via a knowledge graph
- Dynamically routing user queries using an AI agent instead of static logic

This system highlights key real-world concepts such as **tool orchestration, data abstraction, retrieval-augmented generation (RAG), and observability**, making it an excellent learning and portfolio project for early-career developers exploring applied AI and data engineering.

---

## 🔮 Future Scope

The project can be extended in several impactful directions:

### 1. Advanced User Interface
- Build a full **Streamlit or React-based UI**
- Add query history, tool usage indicators, and citation highlights
- Enable document preview and inline answer explanations

### 2. Feedback & Learning Loop
- Capture user feedback (thumbs up/down, comments)
- Store relevance signals for future evaluation
- Simulate fine-tuning or reranking based on positive feedback

### 3. Improved Retrieval Quality
- Add reranking models (e.g., ColBERT or cross-encoders)
- Implement confidence thresholds per tool
- Combine multiple tool outputs for complex queries



---

This project provides a strong foundation for exploring **enterprise-grade AI systems**, and with these extensions, it can evolve into a robust, scalable intelligence platform.
