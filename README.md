flowchart TD
  subgraph DataSources
    A_pdfs["data/pdfs/ (PDFs)"]
    A_emls["data/emls/ (EMLs)"]
    A_csvs["data/csvs/ (CSV files)"]
  end

  subgraph Ingest
    B1["ingest/parse_unstructured.py"]
    B2["ingest/load_structured.py"]
  end

  subgraph Storage
    C1["data/parsed_docs.jsonl"]
    C2["data/enterprise.duckdb"]
    C3["vector index / embeddings store"]
  end

  subgraph Tools
    D["tools/embeddings.py"]
  end

  subgraph Retrievers
    E1["retrievers/vector.py"]
    E2["retrievers/sql.py"]
  end

  F["agents/router_agent.py"]
  G["ui/app.py"]
  H["scripts/db_viewer.py"]

  A_pdfs --> B1
  A_emls --> B1
  A_csvs --> B2

  B1 --> C1
  B2 --> C2

  C1 --> D
  D --> C3

  C3 --> E1
  C1 --> E1
  C2 --> E2

  E1 --> F
  E2 --> F

  G --> F
  H --> C2