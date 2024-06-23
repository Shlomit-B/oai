from openai import OpenAI, OpenAIError
from dotenv import dotenv_values, find_dotenv
import os
import typer

CONFIG_FILE = 'env_path.txt'

app = typer.Typer()

def send_question(key: str, question: str):
    if not key:
        print('You must first run env command to ask OpenAI questions.')
        return None
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
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            path = file.read().strip()
            return dotenv_values(path)["OPENAI_API_KEY"]
        
    else:
        print('You must first run env command to be able to ask OpenAI questions.')
        return None


@app.command()
def env(path: str):
    # Check file path and environment variable are valid
    try:
        dotenv_path = find_dotenv(path)

        if not dotenv_path:
            raise Exception
    
        _ = dotenv_values(path)["OPENAI_API_KEY"]

    except KeyError as e:
        print('Please define the environment variable OPENAI_API_KEY in your .env file and try again.')
        
    except Exception as e:
        print('Did not find .env file. Please check the path you enterd.')

    # Save path to text file
    with open(CONFIG_FILE, 'w') as file:
        file.write(path)


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
