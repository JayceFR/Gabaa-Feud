import requests
import json

def get_json_data(meta_chunk):
    json_data = {}
    json_data.update({"question" : meta_chunk[1]})
    for pointer in range(2, len(meta_chunk)):
        json_data.update({"answer" + str(pointer-1) : meta_chunk[pointer]})
    return json_data

f = open("question.txt", "r")
data = f.read()
f.close()

data = data.split("\n")

meta = []
for chunk in data:
    meta.append(chunk.split("|"))
print(meta)


print(get_json_data(meta[0]))

#base_url = "http://127.0.0.1:5000/"
base_url = "https://gabaafeud.mysticjayce.repl.co/"

for meta_chunk in meta:
    if meta_chunk != []:
        response = requests.post(base_url + "quest/" + meta_chunk[0], json=get_json_data(meta_chunk))
#response = requests.delete(base_url + "quest/1")
#print(response.json())