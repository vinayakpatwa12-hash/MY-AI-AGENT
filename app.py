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
# 1. AI ASSISTANT FUNCTION
# ==========================

SYSTEM_TEXT = """
You are a helpful assistant.
You answer clearly, logically, step-by-step if needed.
"""

def ask_ai(prompt: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM_TEXT},
            {"role": "user", "content": prompt}
        ],
    )
    return resp.choices[0].message.content.strip()


# ==========================
# 2. JSON2VIDEO FUNCTION
# ==========================

def generate_video(prompt: str) -> str:
    if not JSON2VIDEO_KEY:
        raise RuntimeError("JSON2VIDEO_API_KEY missing. Add in Streamlit Secrets.")

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
        raise RuntimeError(f"Video API Error: {resp.status_code}\n{resp.text}")

    # Save to file
    filename = "generated_video.mp4"
    with open(filename, "wb") as f:
        f.write(resp.content)

    return filename


# ==========================
# 3. APP UI
# ==========================

def main():
    st.set_page_config(page_title="AI + Video App", page_icon="🤖")
    st.title("AI Assistant + Text-to-Video Generator 🤖🎬")

    # ---------------- AI Assistant ----------------
    st.header("💬 Ask Anything")

    user_q = st.text_area("Your question:", height=120, key="ai_box")

    if st.button("Ask AI", key="ai_button"):
        if not user_q.strip():
            st.warning("Type something.")
        else:
            with st.spinner("Thinking..."):
                try:
                    ans = ask_ai(user_q)
                    st.markdown("### Answer")
                    st.write(ans)
                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown("---")

    # ---------------- Video Generator ----------------
    st.header("🎬 Text → Video Generator (JSON2Video)")

    video_prompt = st.text_area(
        "Enter video prompt / script:",
        height=150,
        key="video_box"
    )

    if st.button("Generate Video", key="video_button"):
        if not video_prompt.strip():
            st.warning("Please enter a prompt.")
        else:
            with st.spinner("Generating video (may take 30-120 sec)..."):
                try:
                    video_file = generate_video(video_prompt)
                    st.success("Video generated successfully!")
                    st.video(video_file)
                except Exception as e:
                    st.error(f"Video generation failed: {e}")


if __name__ == "__main__":
    main()
