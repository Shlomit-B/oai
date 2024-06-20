from openai import OpenAI, OpenAIError
import os
import typer


app = typer.Typer()

@app.command()
def question(question: str):
    try:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        ans = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}])
        print(ans.choices[0].message.content)
    except OpenAIError as e:
        print(f'error: {e}')

@app.command()
def chat():
    question = input('Message ChatGPT\n')
    while (question != 'exit'):
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        ans = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}])
        print(ans.choices[0].message.content)
        question = input()

if __name__ == "__main__":
    app()
