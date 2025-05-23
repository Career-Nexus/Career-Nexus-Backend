import sys
import os
import re

cwd = os.getcwd()
dir_items = os.listdir(cwd)

toc_identifier = '{{TOC}}'

if "input.md" not in dir_items:
    documentation_name = input("Enter Name of Documentation:\n")
    heading = f"# {documentation_name}\n\n\n## Index<a name='toc'></a>\n\n{toc_identifier}"
    with open(os.path.join(cwd,"input.md"),"w",encoding="utf-8") as file:
        file.write(heading)

with open(os.path.join(cwd,"input.md"),"r") as file:
    doc_content = file.read()

def request(description,multiple=False):
    if multiple == False:
        command = input(description)
        if command.lower() == "n":
            return ''
        else:
            return command
    else:
        output_container = []
        command = input(description)
        while command.lower() != "n":
            command = input(description)
            output_container.append(command)
        return output_container

def format_payload():
    container = []
    key = input("Item name:\n")
    if key.lower() != "n":
        while key.lower() != "n":
            container.append(key)
            key = input("Item name:\n")
        head_text = "{\n"
        for i in container:
            head_text = f"{head_text}\n{i}:*****\n"
        terminate = "}"
        return f"{head_text}\n{terminate}\n"
    else:
        return "\n"




print("---------HEAD PARAMETERS----------------")
title = request("Title of API:\n")
description = request("API description:\n")
endpoint = request("Endpoint:\n")
method = request("Request Method:\n")
print("----------PAYLOAD---------------")
payload = format_payload()



print("---------BODY PARAMETERS----------------")
success_status_code = request("Status Code(successful):\n")

print("Success Body:")
success_body = sys.stdin.read()

failure_status_code = request("Status Code(Failure):\n")
print("Failure Body:")
failure_body = sys.stdin.read()

def md(type,string):
    allowed_types = ["Title","Description","Endpoint","Method","Success_sc","Success_b","Failure_sc","Failure_b","Payload"]
    if type not in allowed_types:
        return "Failed"
    else:
        if len(string) > 0:
            if type.capitalize() == "Title":
                output = f"# {string}\n\n"
            elif type.capitalize() == "Description":
                output = f"{string}\n\n"
            elif type.capitalize() == "Endpoint":
                output = f"**Endpoint:**`{string}`\n\n"
            elif type.capitalize() == "Method":
                output = f"**Method:** `{string}`\n\n"
            elif type.capitalize() == "Success_sc":
                output = f"## Response body\n\n**status code:{string}**\n\n"
            elif type.capitalize() == "Success_b":
                output = f"``` json\n{string}```\n\n"
            elif type.capitalize() == "Failure_sc":
                output = f"## Failure\n\n**status code:{string}**\n\n"
            elif type.capitalize() == "Payload":
                output = f"## Payload\n\n``` json\n{string}\n```\n"
            else:
                output = f"```{string}```\n\n"
            return f"{output}"
        else:
            return ""

exit_container = []
title = md("Title",title)
exit_container.append(title)

description = md("Description",description)
exit_container.append(description)



endpoint = md("Endpoint",endpoint)
exit_container.append(endpoint)



method = md("Method",method)
exit_container.append(method)



payload = md("Payload",payload)
exit_container.append(payload)


success_status_code = md("Success_sc",success_status_code)
exit_container.append(success_status_code)


success_body = md("Success_b",success_body)
exit_container.append(success_body)


failure_status_code = md("Failure_sc",failure_status_code)
exit_container.append(failure_status_code)


failure_body = md("Failure_b",failure_body)
exit_container.append(failure_body)
exit_container.append(f"[Table of contents](#toc)")



#print("=========================================================")
#print("".join(exit_container))

#print("=========================================================")

#Creating table of contents
updated_docs = f"{doc_content}\n\n\n{''.join(exit_container)}"

with open(os.path.join(cwd,"input.md"),"w",encoding="utf-8") as file:
    file.write(updated_docs)

text = updated_docs

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
    text_toc.append(f"\n{text}")

output = re.sub(r"{{TOC}}","".join(text_toc),output)

with open(os.path.join(cwd,"output.md"),"w",encoding="utf-8") as file:
    file.write(output)

print("[LOG]: Completed")


