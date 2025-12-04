import os
import streamlit as st
from openai import OpenAI
import fal_client


# ==========================
# ENV VARIABLES
# ==========================

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
FAL_KEY = os.getenv("FAL_KEY")

if not OPENAI_KEY:
    st.error("OPENAI_API_KEY missing. Set it in Streamlit → Secrets.")
    st.stop()

if not FAL_KEY:
    st.warning("FAL_KEY missing → Video generation won't work.")

# Setup clients
client = OpenAI(api_key=OPENAI_KEY)

if FAL_KEY:
    fal_client.api_key = FAL_KEY


# ==========================
# 1. AI CHAT FUNCTION
# ==========================

SYS_TEXT = """You are a helpful assistant. Answer clearly and logically."""

def ask_ai(prompt: str) -> str:
    try:
        resp = client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=0.2,
            messages=[
                {"role": "system", "content": SYS_TEXT},
                {"role": "user", "content": prompt}
            ],
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"


# ==========================
# 2. FAL.AI VIDEO GENERATION
# ==========================

def generate_video(prompt: str):
    try:
        response = fal_client.submit(
            model="fal-ai/pika/v2/turbo/text-to-video",
            arguments={
                "prompt": prompt,
                "duration": 4,   # seconds
            }
        )

        result = response.get()

        return result.get("video", {}).get("url")

    except Exception as e:
        return None, str(e)


# ==========================
# 3. STREAMLIT UI
# ==========================

def main():

    st.set_page_config(page_title="AI + Pika Video", page_icon="🤖")

    st.title("AI Assistant + Pika Video Generator 🤖🎬")


    # ---------------- CHAT SECTION ----------------

    st.header("💬 Ask Anything")

    user_q = st.text_area("Your question:", key="ai_input")

    if st.button("Ask AI", key="ai_button"):
        if not user_q.strip():
            st.warning("Type something first.")
        else:
            with st.spinner("Thinking..."):
                answer = ask_ai(user_q)
                st.markdown("### Answer:")
                st.write(answer)


    st.markdown("---")


    # ---------------- VIDEO SECTION ----------------

    st.header("🎬 Generate Video using Pika (Fal.ai)")

    if not FAL_KEY:
        st.info("Add FAL_KEY to Streamlit secrets to enable video feature.")
    else:

        video_prompt = st.text_area(
            "Enter a prompt for video:",
            key="video_input",
            height=150
        )

        if st.button("Generate Video", key="video_button"):

            if not video_prompt.strip():
                st.warning("Enter a video prompt.")
            else:
                with st.spinner("Generating video... this may take ~60s"):

                    video_url = None
                    error = None

                    try:
                        video_url = generate_video(video_prompt)
                    except Exception as e:
                        error = str(e)

                    if video_url:
                        st.success("Video generated!")
                        st.video(video_url)
                        st.markdown(f"[Download Video]({video_url})")

                    else:
                        st.error("Failed to generate video.")
                        if error:
                            st.write(error)


if __name__ == "__main__":
    main()
