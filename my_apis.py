import requests 
import json
import html

dad_joke_url = "https://dad-jokes.p.rapidapi.com/random/joke"
yo_momma_joke_url = "https://api.yomomma.info/"
evil_insult_url = "https://evilinsult.com/generate_insult.php"

dad_joke_headers = {
    'x-rapidapi-key': "a8703ff064msh7a09c106cbbb443p1425f2jsn3dddefa8add1",
    'x-rapidapi-host': "dad-jokes.p.rapidapi.com"
    }

def get_dad_joke():
    response = requests.request("GET", dad_joke_url, headers=dad_joke_headers)
    joke_body = json.loads(response.text)['body'][0]
    return html.unescape(joke_body)

def get_yo_momma_joke():
    response = requests.request("GET", yo_momma_joke_url)
    joke_body = json.loads(response.text)['joke']
    return html.unescape(joke_body)

def get_evil_insult():
    response = requests.request("GET", evil_insult_url)
    insult = html.unescape(response.text)
    return insult
    