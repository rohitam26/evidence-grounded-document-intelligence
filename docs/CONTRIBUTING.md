# Contributing Guidelines

1. Fork and clone the repository.
2. Create a feature branch: `git checkout -b feature/improvement`.
3. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   cd frontend && npm install
   ```
4. Run tests and benchmarks before opening a pull request:
   ```bash
   python -m pytest backend/tests/ -v
   python scripts/run_evaluation.py
   cd frontend && npm run build
   ```
5. Commit changes adhering to Conventional Commits format (`feat:`, `fix:`, `docs:`, `test:`).
