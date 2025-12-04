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
