import json
import db
from os import path

with open("data/files.json") as f:
    x = json.load(f)

courses = path.join(path.dirname(path.realpath(__file__)), "courses.json")
with open(courses) as f:
    coursecodes = json.loads(f.read())

pptmimeList = ["application/vnd.ms-powerpoint","application/vnd.openxmlformats-officedocument.presentationml.presentation"]

data = []

for file in x:
    id = file["id"]
    name = file["name"]
    mime = file["mimeType"]
    tag = file["tags"]

    newtag = []

    typicalAncestors = []
    for c in coursecodes:
        for t in tag:
            if c in t:
                typicalAncestors.append(t)
                if "course:" + c not in newtag:
                    newtag.append("course:" + c)

    for t in tag:
        tl = t.lower()
        if "reference book" in tl:
            newtag.append("kind:book")
            typicalAncestors.append(t)
            break
        elif "note" in tl:
            newtag.append("kind:notes")
            typicalAncestors.append(t)
            break
        elif "ppt" in tl:
            newtag.append("kind:lecture-ppt")
            typicalAncestors.append(t)
            break
    
    if mime in pptmimeList and "kind:lecture-ppt" not in newtag:
        newtag.append("kind:lecture-ppt")
    
    for t in tag:
        if t not in typicalAncestors and t:
            newtag.append("other:"+t)

    file = db.File(name = name, link=id, tags=newtag)
    data.append(file)

db.add_files(data)
