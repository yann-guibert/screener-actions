import requests
import pandas as pd 
from datetime import datetime
import os 
import time

CLE_API= "CLE_API"

def get_prix_action(symbole): 
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbole}&apikey={CLE_API}"
    reponse = requests.get(url)
    donnees= reponse.json()
    if "Global Quote" in donnees:
        prix = float(donnees["Global Quote"]["05. price"])
        change = float(donnees["Global Quote"]["09. change"])
        change_percent = donnees["Global Quote"]["10. change percent"]
        return prix, change, change_percent
    else:
        return None, None, None

#actions à suivre.
actions= ["AAPL", "TSLA", "NVDA", "AMG"]

resultats=[]
for symbole in actions: 
    prix, change, change_percent = get_prix_action(symbole)
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    resultats.append ({
        "actions": symbole,
        "prix": prix,
        "change": change, 
        "change_percent": change_percent, 
        "date": date,
    })
    time.sleep (1)

df= pd.DataFrame(resultats)
df_baisse= df[df["change"] < -5]
print (df)
print (df_baisse)
if os.path.exists("screener_actions.csv"):
    df.to_csv("screener_actions.csv", mode="a", header=False, index=False)
else:
    df.to_csv("screener_actions.csv", index=False)
print ('Sauvegardé!')
