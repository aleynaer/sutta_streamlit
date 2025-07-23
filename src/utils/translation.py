def translate_text(llm, text, system_prompt):
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=text)
    ]
    response = llm.invoke(messages)
    return response.content, response.response_metadata.get("token_usage", {}).get("completion_tokens", 0), response.response_metadata.get("token_usage", {}).get("prompt_tokens", 0)

def save_translation_to_db(translation, db_connection):
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO translations (translated_text) VALUES (?)", (translation,))
    db_connection.commit()

def get_saved_translations(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM translations")
    return cursor.fetchall()