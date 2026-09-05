# pyrefly: ignore [missing-import]
from ollama import chat


# ============================================================
# Configuration
# ============================================================

MODEL_NAME = "qwen3.5:4b"

MAX_OUTPUT_TOKENS = 1500


# ============================================================
# Step 12: Connect to LLM
# ============================================================

def generate_response(prompt):
    """
    Send the augmented prompt to Ollama
    and return the generated response.
    """

    response = chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        think=False,
        options={
            "num_predict": MAX_OUTPUT_TOKENS,
        },
    )

    return response["message"]["content"]


# ============================================================
# Test LLM
# ============================================================

if __name__ == "__main__":

    test_prompt = """
You are a Stardew Valley assistant.

Give a helpful and moderately detailed answer.
Explain the important points clearly and use
bullet points when appropriate.

Answer this question:

What is Stardew Valley?
""".strip()

    print("Sending prompt to LLM...")

    response = generate_response(
        test_prompt
    )

    print("\nLLM Response:")
    print("=" * 60)

    print(response)
