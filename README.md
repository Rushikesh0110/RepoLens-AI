# RepoLens AI

**A local-first AI-powered codebase intelligence platform.**

RepoLens AI aims to help developers understand unfamiliar codebases through repository analysis, code structure extraction, semantic search, AI-powered question answering, and evidence-based bug investigation.

## Vision

Build an intelligent developer assistant that understands how a software repository is structured, how its components interact, and where important functionality is implemented.

## Core Features

### Implemented

- Local repository ingestion and scanning
- File metadata extraction and repository statistics
- File filtering and exclusion rules
- Binary and oversized file detection
- File-access error handling
- Command-line repository scanning
- Python AST-based code structure extraction
- Function and asynchronous function detection
- Class and method identification
- Import, alias, and relative import extraction
- Syntax-error handling during code extraction
- Automated testing with Pytest

### Planned

- Advanced repository analytics and visualization
- Semantic code search
- Retrieval-Augmented Generation (RAG)
- Local LLM integration
- Evidence-based codebase question answering
- AI-assisted bug investigation
- Retrieval and answer evaluation
- Interactive developer interface

## Technology Stack

| Category | Technology |
|---|---|
| Language | Python |
| Code Analysis | Python AST |
| Testing | Pytest |
| Code Quality | Ruff |
| Version Control | Git and GitHub |
| Frontend | Streamlit (planned) |
| Backend API | FastAPI (planned) |
| Local LLM | Ollama + Qwen3 4B (planned) |
| Embeddings | Sentence Transformers (planned) |
| Vector Database | ChromaDB (planned) |
| Storage | SQLite (planned) |

## Development Philosophy

- Local-first development
- Privacy-conscious repository processing
- Modular and maintainable architecture
- Evidence-grounded AI responses
- Measurable evaluation and testing

## Project Status

**Current Phase: Repository Ingestion and Code Structure Extraction**

The repository scanning engine and initial Python AST extraction engine are implemented and tested.

Current validation:

- 16 automated tests passing
- Ruff code-quality checks passing
- Successfully tested against an external Python repository
- File metadata and repository statistics extracted
- Python functions, classes, and imports identified
- Syntax errors handled during code extraction

The project is under active development. Features listed under Planned are not yet implemented.

## Roadmap

1. Repository ingestion and scanning — Completed
2. Python code structure and symbol extraction — Completed
3. Advanced repository analytics and visualization
4. Semantic indexing and search
5. Local LLM integration
6. Retrieval-Augmented Generation
7. Evidence-based question answering
8. AI-assisted bug investigation and evaluation
9. Streamlit-based developer interface

## Future Goal

Build a complete local AI developer assistant capable of understanding, searching, explaining, and investigating real-world software repositories while keeping code and processing under the developer's control.
