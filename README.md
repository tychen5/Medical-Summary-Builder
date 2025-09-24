# Medical Summary Builder

Medical Summary Builder is an end-to-end pipeline that ingests disability case files, extracts structured claimant information, and produces a completed medical summary that mirrors the provided template. The system is designed around modular components that combine Retrieval-Augmented Generation (RAG), LangChain tooling, and configurable report writers so attorneys can quickly assemble customized case summaries.

---

## Key Capabilities

- **Automated ingestion** of large medical PDFs into LangChain `Document` objects (`src/medical_summary_builder/data_ingestion/`).
- **Template awareness** by reading DOCX layouts to align generated outputs with attorney-provided formats (`TemplateLoader`).
- **Chunking & indexing** of source documents for hybrid semantic retrieval via Pinecone (`DocumentChunker`, `VectorIndexManager`).
- **LLM-driven extraction** through LangGraph ReAct agents to iteratively retrieve facts and populate summary tables (`agents/`).
- **Flexible reporting** in markdown and DOCX with placeholders for custom table layouts (`ReportWriter`).
- **CLI & API surfaces** for local automation or integration into downstream systems (`cli.py`, `api/app.py`).

---

## Inputs & Outputs

- **Primary inputs**
  - **Source PDF**: `Data/Medical File.pdf`
  - **Template DOCX**: `Data/Medical Summary.docx`
  - **Optional instructions**: User-authored markdown describing custom table layout or extraction emphasis
- **Primary outputs**
  - **Structured JSON**: `MedicalSummary` schema with claimant profile, timeline events, and optional custom tables
  - **Markdown report**: `outputs/reports/medical_summary.md`
  - **DOCX report**: `outputs/reports/medical_summary.docx`

---

## Repository Layout

```
.
├── Data/
│   ├── Medical File.pdf
│   └── Medical Summary.docx
├── outputs/
│   └── .gitkeep
├── prompts/
├── requirements.txt
└── src/
    └── medical_summary_builder/
        ├── __init__.py
        ├── agents/
        ├── api/
        ├── cli.py
        ├── config.py
        ├── data_ingestion/
        ├── llm/
        ├── logging_config.py
        ├── pipelines/
        ├── preprocessing/
        ├── reporting/
        ├── schemas/
        ├── services/
        └── utils/
```

### Module Overview

- **`config.py`**: Centralized configuration via `BaseSettings` (API keys, directories, chunking parameters).
- **`logging_config.py`**: Structured logging setup for console and optional file outputs.
- **`data_ingestion/`**: Loaders and converters for PDFs and DOCX templates (`PDFMedicalLoader`, `TemplateLoader`, `DocumentConverter`).
- **`preprocessing/`**: Chunking, metadata routing, and page relevance ranking stubs ready for LLM integration.
- **`vectorstore/`**: Pinecone index orchestration (`VectorIndexManager`).
- **`llm/`**: Factories that standardize chat models and embedding providers across Nebius/OpenAI.
- **`agents/`**: ReAct-style agent factory configured with LangGraph to drive iterative retrieval.
- **`pipelines/`**: `MedicalSummaryPipeline` wires ingestion, indexing, and downstream extraction steps.
- **`services/`**: High-level façade (`SummaryBuilderService`) that orchestrates pipeline runs and report emission.
- **`reporting/`**: Writers that render markdown and DOCX outputs (`ReportWriter`).
- **`schemas/`**: Pydantic models describing claimant profiles and timeline events.
- **`api/`**: FastAPI application exposing HTTP endpoints for summary creation.
- **`cli.py`**: Typer-based CLI entrypoint for local batch processing.
- **`utils/`**: Shared helpers for IO and prompt management (`PromptLibrary`).

---

## Environment Setup

### Prerequisites

- Python 3.11+
- Access keys for the chosen LLM provider(s) and Pinecone (if vector indexing is required)

### Installation

```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

### Environment Variables (`.env`)

```
NEBIUS_API_KEY=...
OPENAI_API_KEY=...
PINECONE_API_KEY=...
PINECONE_ENVIRONMENT=...
PINECONE_INDEX=medical-summary-index
```

Additional optional settings (see `src/medical_summary_builder/config.py`) include directory overrides and runtime flags such as `ENABLE_TELEMETRY` or `DRY_RUN`.

---

## Pipeline Methodology

1. **Document ingestion** (`PDFMedicalLoader`): Each PDF page is converted to a LangChain `Document` with page number metadata (`page_label` reflecting true PDF pagination per Instruction.md guidance).
2. **Chunking** (`DocumentChunker`): Documents are split into overlapping windows to improve retrieval granularity.
3. **Vector indexing** (`VectorIndexManager`): Chunks are embedded and stored in Pinecone for hybrid retrieval during agent execution.
4. **Template parsing** (`TemplateLoader`): DOCX template paragraphs are normalized into markdown to align output structure.
5. **Extraction agents** (`create_react_agent`): LangGraph ReAct agents orchestrate retrieval and reasoning loops, using vector search tools to populate claimant metadata and event tables.
6. **Custom table support** (`TemplateFiller`): Optional user instructions are parsed to generate bespoke tables beyond the default timeline layout.
7. **Reporting** (`ReportWriter`): Final `MedicalSummary` models are rendered to markdown/DOCX to mirror `Medical Summary.docx` while referencing actual PDF page numbers for the `REF` column.

The architecture keeps each phase isolated so retrieval, extraction, and formatting strategies can be independently improved or swapped for best-of-breed practices.

---

## Usage

### Command Line Interface

```bash
python -m medical_summary_builder.cli build \
  --pdf-path Data/Medical\ File.pdf \
  --template-path Data/Medical\ Summary.docx \
  --custom-instruction-file prompts/custom_table.md
```

- **`--custom-instruction-file`**: Optional markdown describing columns, data definitions, and examples for bespoke tables.
- **`--skip-reports`**: Avoid writing markdown/DOCX outputs if downstream systems consume JSON directly.

### FastAPI Service

```bash
uvicorn medical_summary_builder.api.app:create_app --factory --reload
```

POST `/summaries` with multipart form-data fields `pdf_file`, `template_file`, and optional `custom_instruction` to receive a serialized `MedicalSummary` response. Use `/health` for readiness checks.

---

## Development Notes

- Unit tests can be added under `tests/` (not yet scaffolded) using `pytest`.
- Prompts can be versioned within `prompts/` and loaded via `PromptLibrary` for reproducible agent behavior.
- Intermediate artefacts (logs, converted templates, diagnostics) are written to folders managed through `config.Settings` ensuring consistent output paths.

---

## Roadmap & Enhancements

- **MetadataRouter**: Integrate structured claimant extraction via function calling or JSON schema-constrained prompts.
- **PageRelevanceRanker**: Implement LLM-based scoring to triage relevant pages before detailed extraction.
- **Custom layout builder**: Extend `ReportWriter` to dynamically generate DOCX tables from user-specified schemas (Instruction.md bonus requirement).
- **Evaluation harness**: Add regression tests comparing generated summaries against ground-truth samples.
