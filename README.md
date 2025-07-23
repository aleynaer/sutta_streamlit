# Translation Streamlit App

## Overview
This project is a Streamlit application designed for translating Pali texts into Turkish. It utilizes various resources, including instruction documents, style guides, and a dictionary, to provide accurate translations while maintaining the integrity of the original text.

## Features
- User-friendly interface for translating Pali texts.
- Ability to view and edit instruction texts and style guides.
- Access to a dictionary for Pali terms and their Turkish translations.
- Display of example translations for reference.
- Save and retrieve previously translated texts.

## Project Structure
```
translation-streamlit-app
├── src
│   ├── app.py                  # Main entry point of the Streamlit application
│   ├── utils
│   │   └── translation.py      # Utility functions for handling translations
│   ├── assets
│   │   └── sozluk.json         # Dictionary data for translations
│   └── data
│       ├── 1- Talimat Dosyası.docx  # Instruction text document
│       ├── 2-Cem Şen Çeviri Üslubu Rehberi.docx  # Style guide document
│       ├── ceviri_ornek.txt    # Example translations
│       └── Devadahasutta.txt    # Original Pali text for translation
├── requirements.txt             # Project dependencies
├── README.md                    # Project documentation
└── .streamlit
    └── secrets.toml            # Sensitive information storage
```

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   cd translation-streamlit-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure your API keys and secrets in the `.streamlit/secrets.toml` file.

4. Run the Streamlit application:
   ```
   streamlit run src/app.py
   ```

## Usage Guidelines
- Navigate through the application using the sidebar to access different features.
- Use the translation feature to input Pali text and receive Turkish translations.
- Edit and save instruction texts and style guides as needed.
- Refer to the dictionary for accurate translations of Pali terms.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.