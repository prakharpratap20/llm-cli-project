import os
from dotenv import load_dotenv

from groq import Groq

load_dotenv()


def dispatch(
    prompt: str,
    sysprompt: str = "",
    model: str = "llama3-70b-8192",
) -> str:
    """

    """

    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": sysprompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        model=model,
    )
    response = chat_completion.choices[0].message.content
    return response


def read_markdown_file(file_path: str) -> str:
    with open(file_path, "r") as file:
        content = [line.strip()
                   for line in file if not line.lstrip().startswith("<!--")]
        return "\n".join(content)


if __name__ == "__main__":
    sysprompt = "You are an expert python developer. Your job is to write code, do not explain the code that you produce. Make sure you document each function you return with a docstring."
    prompt = read_markdown_file("ask.md")
    response = dispatch(prompt, sysprompt)
    with open('ask.md', "a") as f:
        f.write("\n"*3 + response)
