# pyrefly: ignore [missing-import]
from ollama import chat


# ============================================================
# Configuration
# ============================================================

MODEL_NAME = "qwen3.5:4b"


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
    )

    return response["message"]["content"]


# ============================================================
# Test LLM
# ============================================================

if __name__ == "__main__":

    test_prompt = """
You are a Stardew Valley assistant.

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
