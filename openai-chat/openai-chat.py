from openai import OpenAI, OpenAIError
from dotenv import dotenv_values, find_dotenv
import os
import typer

app = typer.Typer()


def send_question(key: str, question: str):
    try:
        client = OpenAI(api_key=key)
        ans = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}])
        return ans
    
    except OpenAIError as e:
        print(f'Could not connect to get the answer from OpenAI:\n{e}')
        return None
    

def get_api_key():
    try:
        if not os.path.isfile('.env'):
            raise Exception
        
        key = dotenv_values()["OPENAI_API_KEY"]

    except KeyError:
        print('Please define the environment variable OPENAI_API_KEY in your .env file and try again.')
        return None
    
    except Exception:
        print('Did not find .env file.')
        return None
    
    return key


@app.command()
def question(question: str):
    key = get_api_key()
    if key:
        ans = send_question(key, question)
        if ans:
            print(ans.choices[0].message.content)
    

@app.command()
def chat():
    key = get_api_key()
    if key:
        inp = input('You can message ChatGPT now. When you finish, type "exit".\n')
        while (inp != 'exit'):
            ans = send_question(key, inp)
            if not ans:
                break
            print(ans.choices[0].message.content)
            inp = input()

if __name__ == "__main__":
    app()
