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
    import os
import streamlit as st
from openai import OpenAI
import requests

# ==========================
# ENV KEYS
# ==========================

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
JSON2VIDEO_KEY = os.getenv("JSON2VIDEO_API_KEY")

if not OPENAI_KEY:
    st.error("OPENAI_API_KEY missing. Add it in Streamlit → Secrets.")
    st.stop()

client = OpenAI(api_key=OPENAI_KEY)


# ==========================
# 1. NORMAL AI ASSISTANT
# ==========================

SYSTEM_TEXT = """
You are a helpful, knowledgeable AI assistant.
You answer clearly and logically.
"""

def ask_ai(prompt: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.3,
        messages=[
            {"role":"system", "content": SYSTEM_TEXT},
            {"role":"user",   "content": prompt}
        ]
    )
    return resp.choices[0].message.content.strip()


# ==========================
# 2. JSON2VIDEO GENERATOR
# ==========================

def generate_video(prompt: str) -> bytes:
    if not JSON2VIDEO_KEY:
        raise RuntimeError(
            "JSON2VIDEO_API_KEY missing. "
            "Add it in Streamlit → Secrets."
        )

    url = "https://api.json2video.com/v1/video"

    headers = {
        "Authorization": f"Bearer {JSON2VIDEO_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "script": prompt,
        "aspect_ratio": "16:9",
        "resolution": "720p",
        "voice_over": "en-US",
        "fps": 24
    }

    resp = requests.post(url, json=payload, headers=headers)

    if resp.status_code != 200:
        raise RuntimeError(
            f"API Error: {resp.status_code}\n{resp.text}"
        )

    return resp.content  # raw video bytes


# ==========================
# STREAMLIT UI
# ==========================

def main():
    st.set_page_config(page_title="AI + Video App", page_icon="🤖")

    st.title("AI Assistant + Video Generator 🤖🎬")

    # ----------- AI Assistant ------------
    st.header("🔹 Ask Anything")

    q = st.text_area("Your question:", height=120)
    
    if st.button("Ask AI"):
        if not q.strip():
            st.warning("Type something first.")
        else:
            with st.spinner("Thinking..."):
                try:
                    ans = ask_ai(q)
                    st.markdown("### Answer")
                    st.write(ans)
                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown("---")

    # ----------- JSON2Video ------------
    st.header("🔹 Text → Video Generator (JSON2Video)")

    v_prompt = st.text_area("Enter video prompt / script:")

    if st.button("Generate Video"):
        if not v_prompt.strip():
            st.warning("Type a video prompt first.")
        else:
            with st.spinner("Generating video... (takes time)"):
                try:
                    data = generate_video(v_prompt)
                    fname = "video.mp4"

                    with open(fname, "wb") as f:
                        f.write(data)

                    st.success("Video generated successfully!")
                    st.video(fname)

                except Exception as e:
                    st.error(f"Video generation failed: {e}")


if __name__ == "__main__":
    main()

