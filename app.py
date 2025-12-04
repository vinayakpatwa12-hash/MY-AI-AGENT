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

client = OpenAI(api_key=OPENAI_KEY)

if FAL_KEY:
    fal_client.api_key = FAL_KEY


# ==========================
# AI CHAT
# ==========================

SYS_TEXT = "You are a helpful, smart assistant. Answer clearly and logically."

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
# FAL.AI VIDEO GENERATION
# ==========================

def generate_video(prompt: str):
    if not FAL_KEY:
        return None, "FAL_KEY missing."

    try:
        # Submit job (CORRECT API CALL)
        response = fal_client.submit(
            "fal-ai/pika/v2/turbo/text-to-video",
            {
                "prompt": prompt,
                "duration": 4,
            }
        )

        # Wait for job completion
        result = response.get()

        if not result:
            return None, "Empty response from API."

        video_data = result.get("video")

        if not video_data:
            return None, "API returned no video field."

        video_url = video_data.get("url")

        if not video_url:
            return None, "API returned no video URL."

        return video_url, None

    except Exception as e:
        return None, str(e)


# ==========================
# STREAMLIT UI
# ==========================

def main():

    st.set_page_config(page_title="AI + Video", page_icon="🤖")
    st.title("AI Assistant + Pika Video Generator 🤖🎬")


    # ------- CHAT SECTION -------
    st.header("💬 Ask Anything")

    user_q = st.text_area("Your question:", key="ai_input", height=120)

    if st.button("Ask AI", key="btn_ai"):
        if not user_q.strip():
            st.warning("Type something first.")
        else:
            with st.spinner("Thinking..."):
                answer = ask_ai(user_q)
                st.markdown("### Answer:")
                st.write(answer)


    st.markdown("---")


    # ------- VIDEO SECTION -------
    st.header("🎬 Generate Video using Pika (Fal.ai)")

    if not FAL_KEY:
        st.info("Add FAL_KEY in Secrets to enable video generator.")
        return

    video_prompt = st.text_area(
        "Enter a prompt for video:", key="video_input", height=150
    )

    if st.button("Generate Video", key="btn_video"):

        if not video_prompt.strip():
            st.warning("Enter a video prompt.")
            return

        with st.spinner("Generating video... (30-120 sec)"):

            video_url, error = generate_video(video_prompt)

            if video_url and not error:
                st.success("Video generated!")

                try:
                    st.video(video_url)
                except:
                    st.warning("Video generated, but cannot embed. Open manually:")

                st.markdown(f"[Open / Download Video]({video_url})")

            else:
                st.error("Video generation failed.")
                if error:
                    st.write("Error details:")
                    st.write(error)


if __name__ == "__main__":
    main()
