import os
import streamlit as st
from openai import OpenAI

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    st.error("API key not set. Please set OPENAI_API_KEY in Streamlit secrets.")
    st.stop()

client = OpenAI(api_key=API_KEY)

SYSTEM_TEXT = """
You are a helpful, knowledgeable AI assistant.
You can answer any type of question clearly and logically.
"""

def ask_ai(q):
    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_TEXT},
            {"role": "user", "content": q}
        ],
        temperature=0.3
    )
    return res.choices[0].message.content.strip()

def main():
    st.title("AI Assistant 🤖")

    q = st.text_area("Ask anything:")

    if st.button("Ask"):
        if q.strip():
            st.write(ask_ai(q))
        else:
            st.warning("Type something first!")

if __name__ == "__main__":
    main()
