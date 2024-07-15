import requests
import re


url = "http://www.pythiacrafting.com/?crafts_sequence="
def get_next_item(sequense):
    rstext = requests.get(url+sequense).text
    if "Potential issue" in rstext:
      print("Potential issue at",len(sequense))
      return "7"
    percentages = re.findall(r'<span class="value">(\d+\.\d+%)</span>', rstext)
    po = {}
    # Print the percentages
    i = 1
    for percentage in percentages:
        po[str(i)] = float(percentage[:-1])
        i+=1
    max_value = max(po.values())
    max_key = max(po, key=po.get)
    return max_key

def get_next_77(sequense, more7=20, max_kraft=1500):
  count = 0
  while count < more7 and len(sequense) < max_kraft:
    next_item = get_next_item(sequense)
    if next_item == "7":
      count += 1
      print("#",count,":",len(sequense)+1)
    sequense += str(next_item)
  return sequense

def get_n_rolls(hero_id):
  response = requests.get("https://eternium.pages.dev/api/v1/users/"+hero_id)
  heroes = response.json()
  return heroes['masterCraftDice']['nRolls']


# Example usage
mmID = 'MMID-5E5BE89B-D785095D-B50404D4-199C45D4B84FE9BAE7B9D38088ED3B66/heroes/'
hero_id = mmID + "HERO-16EC8C75-5785C1E0-9184A5DE-DFD4F66AD7739B5140770C4977F9E281"
n77seq = "23422352324232726242323232452232122432326523223243225243223422322324325223242632243212325232234272323245222342326232254322323242324223272532263242432322215322243232423262532423222353224223422324322362253234223224523422322342123223526232432232342272522342232324235223246232325213242234232272324235224322324226325232324243232223252342273212342225236423232232432252322432324223262325423242232362327"
# prompt: create a simple flask server that return curent nroll, n76 and n77

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
  nroll = get_n_rolls(hero_id)
  n76 = n77seq.find("6",nroll)+1
  n77 = n77seq.find("7",nroll)+1
  return f"nroll: {nroll}, n76: {n76}, n77: {n77}"

if __name__ == "__main__":
  app.run(host="0.0.0.0")
