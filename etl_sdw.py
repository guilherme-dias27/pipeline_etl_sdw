import pandas as pd
import requests
import openai
from pathlib import Path
from dotenv import load_dotenv, dotenv_values

dotenv_path = (Path(__file__).parent).joinpath(".env")
load_dotenv(dotenv_path)
envvar = dotenv_values(dotenv_path)

openai.api_key = envvar["OPENAI_AUTH"]
    

def getUser(id: int) -> dict:
    url = f"https://sdw-2023-prd.up.railway.app/users/{id}"
    response = requests.get(url, timeout=5)
    
    return response.json() if response.status_code == 200 else None


def generateNews(client: dict) -> str:
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system", 
                "content": "Você é um especialista em marketing no Brasil"
            },
            {
                "role": "user", 
                "content": f"Crie uma mensagem para {client['name']} para convencê-lo a invstir. Seja sucinto e persuasivo."
            }
        ]
    )

    response = completion.choices[0].content.strip("\"")
    
    return response


def updateClient(client: dict) -> bool:
    url = f"https://sdw-2023-prd.up.railway.app/users/{client['id']}"
    payload = client
    
    response = requests.put(url, json=payload, timeout=5)
    
    True if response.status_code == 200 else False



df = pd.read_csv("SDW2023.csv")
ids = df["ClientID"].tolist()

for id in ids:
    client = getUser(id)
    
    client["news"].append(
        {
            "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
            "description": generateNews(client)
        }
    )
    
    success = updateClient(client)
    
    print(f"Client {client['name']} updated? -> {success}")