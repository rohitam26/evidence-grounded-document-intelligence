# Contributing to Evidence-Grounded Document Intelligence

Thank you for your interest in contributing to this project. We welcome improvements to document parsers, hybrid retrieval models, evidence grounding, agent workflows, and test coverage.

---

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rohitam26/evidence-grounded-document-intelligence.git
   cd evidence-grounded-document-intelligence
   ```

2. **Backend setup:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Or venv\Scripts\activate on Windows
   pip install -r backend/requirements.txt
   ```

3. **Frontend setup:**
   ```bash
   cd frontend
   npm install
   npm run build
   cd ..
   ```

---

## Testing & Quality Requirements

Before submitting a Pull Request, all automated checks must pass:

1. **Pytest Suite:**
   ```bash
   python -m pytest backend/tests/ -v
   ```

2. **Empirical Benchmark Suite:**
   ```bash
   python scripts/run_evaluation.py
   ```

3. **Frontend Build & Typecheck:**
   ```bash
   cd frontend && npm run build
   ```

---

## Branching & Commit Conventions

- Create descriptive feature branches: `feat/component-name`, `fix/issue-description`, or `perf/optimization-name`.
- Use conventional commit messages:
  - `feat(...)`: New feature or capability
  - `fix(...)`: Bug fix
  - `perf(...)`: Performance enhancement
  - `test(...)`: Adding or updating test cases
  - `docs(...)`: Documentation updates
- Ensure PRs are focused on a single logical change.
