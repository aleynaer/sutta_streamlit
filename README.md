# Translation Streamlit App

## Overview
This project is a Streamlit application designed for translating Pali texts into Turkish. It utilizes various resources, including instruction documents, style guides, and a dictionary, to provide accurate translations while maintaining the integrity of the original text.

**Note:** This is a private development project. Most project files are excluded from the repository via `.gitignore` for security and privacy reasons.

## Features
- User-friendly interface for translating Pali texts.
- Ability to view and edit instruction texts and style guides.
- Access to a dictionary for Pali terms and their Turkish translations.
- Display of example translations for reference.
- Save and retrieve previously translated texts.

## Project Structure
```
sutta_streamlit/
├── src/
│   ├── app.py                  # Main Streamlit application (excluded from repo)
│   ├── utils/
│   │   ├── db.py      # Database utilities (excluded from repo)
│   │   
│   └── data/
│       ├── instructions.db     # Instructions database (excluded from repo)
│       ├── sozluk.json        # Dictionary data (excluded from repo)
│       ├── *.docx files       # Instruction documents (excluded from repo)
│       └── *.txt files        # Text data files (excluded from repo)
├── test.ipynb                  # Development notebook (excluded from repo)
├── requirements.txt            # Project dependencies (excluded from repo)
├── .gitignore                 # Git ignore rules
└── README.md                  # Project documentation
```

**Important:** Most files in this project are excluded from the repository for privacy and security reasons. Only essential documentation and configuration files are tracked.

## Setup Instructions

**Note:** This is a private development repository. The actual project files are not included in the repository for security reasons.

### For Development Environment Setup:
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd sutta_streamlit
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

3. Install dependencies (you'll need to recreate requirements.txt locally):
   ```bash
   pip install streamlit pandas python-docx sqlite3
   ```

4. Create the necessary project structure and files locally:
   - `src/app.py` - Main Streamlit application
   - `src/utils/` - Utility modules
   - `src/data/` - Data files and databases
   - `.streamlit/secrets.toml` - Configuration file

5. Run the application:
   ```bash
   streamlit run src/app.py
   ```

## Usage Guidelines
- Navigate through the application using the sidebar to access different features.
- Use the translation feature to input Pali text and receive Turkish translations.
- Edit and save instruction texts and style guides as needed.
- Refer to the dictionary for accurate translations of Pali terms.

## Security & Privacy
This project contains sensitive translation data and personal documents. Therefore:
- Most project files are excluded from version control via `.gitignore`
- Only essential documentation and configuration files are tracked
- Actual implementation files must be maintained locally

## Development Notes
- The project uses Streamlit for the web interface
- SQLite database for storing instructions and translations
- JSON format for dictionary data
- DOCX files for style guides and instructions