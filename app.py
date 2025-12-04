#%%
from openai import OpenAI

# ==========================
# CONFIG (PUT YOUR KEY HERE)
# ==========================

API_KEY = "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"

client = OpenAI(api_key=API_KEY)

# ==========================
# SYSTEM BEHAVIOR
# ==========================

SYSTEM_TEXT = """
You are a helpful, knowledgeable AI assistant.
You can answer any type of question: science, math, coding, history, advice, or explanation.
Always reply clearly and logically.
Give high-quality, accurate information.
"""

# ==========================
# AI FUNCTION
# ==========================

def ask_ai(question: str):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.3,
        messages=[
            {"role": "system", "content": SYSTEM_TEXT},
            {"role": "user", "content": question}
        ],
    )

    return response.choices[0].message.content.strip()


# ==========================
# CLI LOOP
# ==========================

def main():
    print("========================================")
    print("       GENERAL AI AGENT")
    print("   Type 'exit' to quit.")
    print("========================================\n")

    while True:
        q = input("Ask anything: ").strip()

        if q.lower() == "exit":
            print("Goodbye.")
            break

        if not q:
            print("Type something.")
            continue

        try:
            ans = ask_ai(q)
            print("\n--- ANSWER ---")
            print(ans)
            print("--------------\n")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
