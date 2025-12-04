import os
import streamlit as st
from openai import OpenAI

SYSTEM_TEXT = """
You are a helpful, knowledgeable AI assistant.
You can answer any type of question clearly and logically.
"""

def get_client():
    """Return (client, error_message)."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None, "OPENAI_API_KEY is not set. Add it in Streamlit -> Secrets."
    try:
        client = OpenAI(api_key=api_key)
        return client, None
    except Exception as e:
        return None, f"Error creating OpenAI client: {e}"

def ask_ai(client, question: str) -> str:
    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.3,
        messages=[
            {"role": "system", "content": SYSTEM_TEXT},
            {"role": "user",  "content": question},
        ],
    )
    return res.choices[0].message.content.strip()

def main():
    st.set_page_config(page_title="AI Assistant", page_icon="🤖")
    st.title("AI Assistant 🤖")
    st.write("Ask anything below.")

    # show something even if key is missing
    client, err = get_client()
    if err:
        st.error(err)
        st.info('In Streamlit Cloud, go to "Manage app" → "Secrets" and set:\n'
                'OPENAI_API_KEY = "your_real_key_here"')
        return

    question = st.text_area("Your question:", height=120)

    if st.button("Ask AI"):
        if not question.strip():
            st.warning("Please type a question first.")
        else:
            with st.spinner("Thinking..."):
                try:
                    answer = ask_ai(client, question)
                    st.markdown("### Answer:")
                    st.markdown(answer)
                except Exception as e:
                    st.error(f"Error from AI: {e}")

if __name__ == "__main__":
    main()
