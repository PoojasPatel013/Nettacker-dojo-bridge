# Nettacker-DefectDojo Bridge Prototype

A working prototype that bridges **OWASP Nettacker** scan results with **DefectDojo** for automated vulnerability management.

## 🚀 Features
- Parses JSON output from Nettacker.
- Automates finding ingestion into DefectDojo via API v2.
- Handles finding deduplication (handled by DefectDojo).
- Includes professional documentation and verification steps.

## 🛠️ Quick Start

### 1. Installation
```bash
pip install requests mkdocs mkdocs-material python-dotenv
```

### 2. Usage
```bash
# Run the bridge script
python bridge.py --file nettacker_results.json --engagement 1
```

### 3. Documentation
This project includes a full walkthrough site.
```bash
mkdocs serve
```
Then open `http://127.0.0.1:8000` to view the guide.

## 📂 Project Structure
- `bridge.py`: The core script pushing data to DefectDojo.
- `nettacker_results.json`: Sample vulnerability data for testing.
- `docs/`: Source for the documentation site.
- `mkdocs.yml`: Configuration for the walkthrough site.

## ⚠️ Configuration
Create a `.env` file in the root directory:
```env
DOJO_URL=http://localhost:8080/api/v2
DOJO_API_KEY=your_api_key_here
```
This keeps your credentials secure and out of the source code.
