import os
from dotenv import load_dotenv
import toml

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


def create_or_read_proompt_file():
    filename = ".proompt"
    if not os.path.exists(filename):
        data = {
            "model_name": "llama3-70b-8192",
            "system_prompt": "",
            "buffer_name": "ask.md"
        }
        with open(filename, "w") as f:
            toml.dump(data, f)
    with open(filename, "r") as f:
        data = toml.load(f)
    return (data["model_name"],
            data["system_prompt"],
            data["buffer_name"])


if __name__ == "__main__":
    model, sysprompt, filename = create_or_read_proompt_file()
    prompt = read_markdown_file(filename)
    response = dispatch(prompt, sysprompt, model)
    with open(filename, "a") as f:
        f.write("\n"*3 + response)
