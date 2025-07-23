import sqlite3
import os
import json
import docx
import streamlit as st

data_path = st.secrets["data_path"]


def init_db():
    db_path = os.path.join(data_path, "instructions.db")  # Veritabanı özel dizinde
    #db_path = "src/data/instructions.db"
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Create instructions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS instructions
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         title TEXT NOT NULL,
         content TEXT NOT NULL,
         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    ''')

    # Initialize instructions if empty
    c.execute("SELECT COUNT(*) FROM instructions")
    if c.fetchone()[0] == 0:
        try:
            # Read default instruction from DOCX
            doc_path = os.path.join(data_path, "1- Talimat Dosyası.docx")
            doc = docx.Document(doc_path)
            talimat = '\n'.join([para.text for para in doc.paragraphs])
            c.execute("INSERT INTO instructions (title, content) VALUES (?, ?)", 
                     ("Default Instructions", talimat))
        except Exception as e:
            print(f"Error loading instructions: {str(e)}")
    

    # Create style guides table
    c.execute('''
        CREATE TABLE IF NOT EXISTS style_guides
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         title TEXT NOT NULL,
         content TEXT NOT NULL,
         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    ''')

    # Initialize style guide if empty
    c.execute("SELECT COUNT(*) FROM style_guides")
    if c.fetchone()[0] == 0:
        try:
            # Read default style guide from DOCX
            doc_path = os.path.join(data_path, "2-Cem Şen Çeviri Üslubu Rehberi.docx")
            doc = docx.Document(doc_path)
            uslup = '\n'.join([para.text for para in doc.paragraphs])
            c.execute("INSERT INTO style_guides (title, content) VALUES (?, ?)", 
                     ("Default Style Guide", uslup))
        except Exception as e:
            print(f"Error loading style guide: {str(e)}")

    # Create dictionary table
    c.execute('''
        CREATE TABLE IF NOT EXISTS dictionary
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         pali TEXT NOT NULL,
         turkish TEXT NOT NULL,
         notes TEXT,
         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    ''')
    
    # Initialize dictionary from JSON if table is empty
    c.execute("SELECT COUNT(*) FROM dictionary")
    if c.fetchone()[0] == 0:
        try:
            json_path = os.path.join(data_path, "sozluk.json")
            with open(json_path, "r", encoding="utf-8") as f:
                dictionary_data = json.load(f)
                entries = []
                
                # Handle both list and dictionary formats
                if isinstance(dictionary_data, list):
                    # If data is a list of entries
                    for item in dictionary_data:
                        if isinstance(item, dict):
                            pali = item.get('pali', '')
                            turkish = item.get('turkish_translation', '')
                            notes = item.get('explanation', '')
                            if pali and turkish:
                                entries.append((pali, turkish, notes))
                else:
                    # If data is a dictionary
                    for pali_term, translations in dictionary_data.items():
                        if isinstance(translations, dict):
                            turkish = translations.get('turkish_translation', '')
                            notes = translations.get('explanation', '')
                            entries.append((pali_term, turkish, notes))
                        else:
                            # Handle simple key-value pairs
                            entries.append((pali_term, str(translations), ''))
                
                # Insert all entries in a single transaction
                if entries:
                    c.executemany(
                        "INSERT INTO dictionary (pali, turkish, notes) VALUES (?, ?, ?)", 
                        entries
                    )
                    print(f"Added {len(entries)} dictionary entries")
                
        except Exception as e:
            print(f"Error loading dictionary: {str(e)}")
            raise
    
    # Create example translations table
    c.execute('''
        CREATE TABLE IF NOT EXISTS example_translations
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         title TEXT NOT NULL,
         original_text TEXT NOT NULL,
         translated_text TEXT NOT NULL,
         is_selected BOOLEAN DEFAULT FALSE,
         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    ''')

    # Initialize example translations if empty
    c.execute("SELECT COUNT(*) FROM example_translations")
    if c.fetchone()[0] == 0:
        try:
            # Read example translations from ceviri_ornek.txt
            txt_path = os.path.join(data_path, "ceviri_ornek.txt")
            with open(txt_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                entries = []
                
                # Each entry is assumed to be in the format: title|original_text|translated_text
                for line in lines:
                    parts = line.strip().split('|')
                    if len(parts) == 3:
                        title, original_text, translated_text = parts
                        entries.append((title, original_text, translated_text))
                
                # Insert all entries in a single transaction
                if entries:
                    c.executemany(
                        "INSERT INTO example_translations (title, original_text, translated_text) VALUES (?, ?, ?)", 
                        entries
                    )
                    print(f"Added {len(entries)} example translations")
        except Exception as e:
            print(f"Error loading example translations: {str(e)}")

    # Create user translations table
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_translations
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         title TEXT NOT NULL,
         original_text TEXT NOT NULL,
         translated_text TEXT NOT NULL,
         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    ''')
    
    conn.commit()
    conn.close()

# Get all instructions from the database
def get_all_instructions():
    conn = sqlite3.connect("src/data/instructions.db")
    c = conn.cursor()
    c.execute("SELECT id, title, content FROM instructions")
    instructions = c.execute("SELECT * FROM instructions").fetchall()
    conn.close()
    return instructions

# Save and update instructions
def save_instruction(title, content):
    conn = sqlite3.connect("src/data/instructions.db")
    c = conn.cursor()
    c.execute("INSERT INTO instructions (title, content) VALUES (?, ?)", (title, content))
    conn.commit()
    conn.close()

def update_instruction(id, title, content):
    conn = sqlite3.connect("src/data/instructions.db")
    c = conn.cursor()
    c.execute("UPDATE instructions SET title = ?, content = ? WHERE id = ?", (title, content, id))
    conn.commit()
    conn.close()

# Get all style guides from the database
def get_all_style_guides():
    conn = sqlite3.connect("src/data/instructions.db")
    c = conn.cursor()
    style_guides = c.execute("SELECT * FROM style_guides").fetchall()
    conn.close()
    return style_guides

# Save and update style guides
def save_style_guide(title, content):
    conn = sqlite3.connect("src/data/instructions.db")
    c = conn.cursor()
    c.execute("INSERT INTO style_guides (title, content) VALUES (?, ?)", (title, content))
    conn.commit()
    conn.close()

def update_style_guide(id, title, content):
    conn = sqlite3.connect("src/data/instructions.db")
    c = conn.cursor()
    c.execute("UPDATE style_guides SET title = ?, content = ? WHERE id = ?", (title, content, id))
    conn.commit()
    conn.close()

# Get all dictionary entries
def get_dictionary():
    """Get all dictionary entries for display"""
    conn = sqlite3.connect("src/data/instructions.db")
    c = conn.cursor()
    dictionary = c.execute("""
        SELECT id, pali, turkish, notes 
        FROM dictionary 
        ORDER BY pali
    """).fetchall()
    conn.close()
    return dictionary

# Add, update, and delete dictionary entries
def add_dictionary_entry(pali, turkish, notes=""):
    conn = sqlite3.connect("src/data/instructions.db")
    c = conn.cursor()
    c.execute("INSERT INTO dictionary (pali, turkish, notes) VALUES (?, ?, ?)", 
             (pali, turkish, notes))
    conn.commit()
    conn.close()

def update_dictionary_entry(id, pali, turkish, notes):
    conn = sqlite3.connect("src/data/instructions.db")
    c = conn.cursor()
    c.execute("UPDATE dictionary SET pali = ?, turkish = ?, notes = ? WHERE id = ?", 
             (pali, turkish, notes, id))
    conn.commit()
    conn.close()

def delete_dictionary_entry(id):
    conn = sqlite3.connect("src/data/instructions.db")
    c = conn.cursor()
    c.execute("DELETE FROM dictionary WHERE id = ?", (id,))
    conn.commit()
    conn.close()

# Get dictionary as a dictionary object
def get_dictionary_as_dict():
    """Get dictionary as a Python dict for translation use"""
    conn = sqlite3.connect("src/data/instructions.db")
    c = conn.cursor()
    rows = c.execute("SELECT pali, turkish, notes FROM dictionary").fetchall()
    conn.close()
    
    return {row[0]: {
        "turkish_translation": row[1],
        "explanation": row[2] if row[2] else ""
    } for row in rows}

# Get all example translations
def get_all_examples():
    conn = sqlite3.connect("src/data/instructions.db")
    c = conn.cursor()
    examples = c.execute("SELECT * FROM example_translations").fetchall()
    conn.close()
    return examples

# Save, update, delete, and select example translations
def save_example(title, original_text, translated_text):
    conn = sqlite3.connect("src/data/instructions.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO example_translations (title, original_text, translated_text) 
        VALUES (?, ?, ?)""", (title, original_text, translated_text))
    conn.commit()
    conn.close()

def update_example(id, title, original_text, translated_text):
    conn = sqlite3.connect("src/data/instructions.db")
    c = conn.cursor()
    c.execute("""
        UPDATE example_translations 
        SET title = ?, original_text = ?, translated_text = ? 
        WHERE id = ?""", (title, original_text, translated_text, id))
    conn.commit()
    conn.close()

def delete_example(id):
    conn = sqlite3.connect("src/data/instructions.db")
    c = conn.cursor()
    c.execute("DELETE FROM example_translations WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def update_example_selection(id, is_selected):
    conn = sqlite3.connect("src/data/instructions.db")
    c = conn.cursor()
    c.execute("UPDATE example_translations SET is_selected = ? WHERE id = ?", (is_selected, id))
    conn.commit()
    conn.close()

def get_selected_examples():
    conn = sqlite3.connect("src/data/instructions.db")
    c = conn.cursor()
    examples = c.execute("SELECT * FROM example_translations WHERE is_selected = TRUE").fetchall()
    conn.close()
    return examples

# Save user translations
def save_user_translation(title, original_text, translated_text):
    conn = sqlite3.connect("src/data/instructions.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO user_translations (title, original_text, translated_text) 
        VALUES (?, ?, ?)""", (title, original_text, translated_text))
    conn.commit()
    conn.close()

# Get user translations
def get_user_translations():
    conn = sqlite3.connect("src/data/instructions.db")
    c = conn.cursor()
    translations = c.execute("SELECT * FROM user_translations ORDER BY created_at DESC").fetchall()
    conn.close()
    return translations