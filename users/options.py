import json
import os

def get_choices():
    dirname = os.path.dirname(os.path.abspath(__file__))
    choice_base = f"{dirname}/resources/valid_options.json"

    with open(choice_base,"r") as file:
        choices = json.load(file)

    categories = list(choices.keys())
    container = {}

    for key in categories:
        values = choices[key]
        container_upper = []
        for item in values:
            group = (item,item)
            container_upper.append(group)
        tuple_container = tuple(container_upper)
        container[key] = tuple_container

    return container


