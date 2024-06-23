from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
import os
import typer


app = typer.Typer()

def send_question(question: str):
    try:
        load_dotenv()
        key = os.environ["OPENAI_API_KEY"]
        client = OpenAI(api_key=key)
        ans = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}])
        return ans
    
    except KeyError as e:
        print('Please define the environment variable OPENAI_API_KEY in your .env file')
        return None
    
    except OpenAIError as e:
        print(f'Could not connect to get the answer from OpenAI:\n{e}')
        return None    

@app.command()
def question(question: str):
    ans = send_question(question)
    if ans:
        print(ans.choices[0].message.content)
    
@app.command()
def chat():
    inp = input('You can message ChatGPT now. When you finish, type "exit".\n')
    while (inp != 'exit'):
        ans = send_question(inp)
        if not ans:
            break
        print(ans.choices[0].message.content)
        inp = input()

if __name__ == "__main__":
    app()
