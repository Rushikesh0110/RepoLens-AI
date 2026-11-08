# RepoLens AI

**A local-first AI-powered codebase intelligence platform.**

RepoLens AI aims to help developers understand unfamiliar codebases through repository analysis, semantic code search, AI-powered question answering, and evidence-based bug investigation.

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
- Automated testing with Pytest

### Planned
- Code structure and symbol extraction
- Repository analytics and visualization
- Semantic code search
- Retrieval-Augmented Generation (RAG)
- Evidence-based codebase question answering
- AI-assisted bug investigation
- Retrieval and answer evaluation

## Technology Stack

| Category | Technology |
|---|---|
| Language | Python |
| Frontend | Streamlit (planned) |
| Backend API | FastAPI (planned) |
| Local LLM | Ollama + Qwen3 4B (planned) |
| Code Analysis | Python AST |
| Data Processing | NumPy, Pandas |
| Machine Learning | Scikit-learn |
| Embeddings | Sentence Transformers |
| Vector Database | ChromaDB |
| Storage | SQLite |
| Testing | Pytest |
| Code Quality | Ruff |

## Development Philosophy

- Local-first development
- Privacy-conscious repository processing
- Modular and maintainable architecture
- Evidence-grounded AI responses
- Measurable evaluation and testing

## Project Status

**Current Phase: Repository Ingestion Foundation**

The initial repository scanning engine is implemented and tested.

Current validation:
- 10 automated tests passing
- Ruff code-quality checks passing
- Successfully tested against an external Python repository
- Verified directory and file exclusion behavior

The project is under active development. Features listed under Planned are not yet implemented.

## Roadmap

1. Repository ingestion and scanning
2. Code structure and symbol extraction
3. Repository analytics
4. Semantic indexing and search
5. Local LLM integration
6. Retrieval-Augmented Generation
7. Evidence-based question answering
8. Evaluation and performance improvements
9. Streamlit-based developer interface

## Future Goal

Build a complete local AI developer assistant capable of understanding, searching, explaining, and investigating real-world software repositories while keeping code and processing under the developer's control.
