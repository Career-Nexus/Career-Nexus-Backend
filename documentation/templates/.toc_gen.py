import re
import sys
import os

with open("Career Nexus Backend Documentation.md","r") as file:
    text = file.read()

content_container = {}

def treat_text(text):
    text = text.lower()
    end = text.replace(" ","_")
    content_container[text] = end
    return end


def anchor(match):
    id = match.group(1)
    treated = treat_text(id)
    return f"# {id}<a name='{treated}'></a>"




pattern = r"^# (.*?)$"

output = re.sub(pattern,anchor,text,flags=re.MULTILINE)

text_toc = []

for key in list(content_container.keys()):
    text = f"[{key}](#{content_container[key]})"
    text_toc.append(text)

output = re.sub(r"{{TOC}}","\n".join(text_toc),output)

with open("output.md","w",encoding="utf-8") as file:
    file.write(output)

print("[LOG]: Completed")

print(os.getcwd())

