# PrimeNag

PrimeNag is a curated collection of prime-number algorithms, tests, and visualizations. The Python core exposes a consistent `PrimeAlgorithm` interface, metadata registry, CLI tools, and a React-based webapp for interactive exploration. This README is intentionally lightweight—detailed docs will accompany the upcoming releases.

---

## Getting Started

```bash
# 1. Python environment
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e .

# 2. Run the test suite
pytest

# 3. Export metadata (algorithms.json + sample outputs)
python scripts/export_metadata.py --samples

# 4. Frontend (requires Node ≥22.12 *or* use Docker image)
cd webapp
npm install
npm run dev
```

Need a ready-to-go environment? Build and run the Docker image:

```bash
docker build -t primenag .
docker run -it --rm -p 5173:5173 primenag bash
```

---

## License

MIT © PrimeNag contributors.
