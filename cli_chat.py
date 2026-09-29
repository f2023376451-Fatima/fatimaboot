"""
FatimaBot CLI — simple terminal chat for testing without Streamlit.
Usage: python cli_chat.py
"""

import os
from rag_engine import get_rag


def main():
    print("FatimaBot CLI — type 'quit' to exit\n")
    rag = get_rag()
    history = []

    while True:
        try:
            query = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break
        if not query:
            continue
        if query.lower() in ("quit", "exit", "q"):
            print("Bye.")
            break

        answer, retrieved = rag.generate(
            query=query,
            history=history,
            api_key=os.getenv("GEMINI_API_KEY") or os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY"),
        )
        print(f"\nFatimaBot: {answer}\n")
        history.append({"role": "user", "content": query})
        history.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    main()
