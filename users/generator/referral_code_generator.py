import random
import json
import os


class generator():
    def __init__(self):
        self.dir = os.path.dirname(os.path.abspath(__file__))
        self.file = os.path.join(self.dir,"ref_codes.json")
        self.number_char = list(range(0,10))
        self.letter_cap = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        self.letter_low = [letter.lower() for letter in self.letter_cap]
        self.tail = list(range(1000,9999))
        with open(self.file,"r") as file:
            self.codes = json.load(file)

    def generate(self):
        number1_list = [str(random.choice(self.number_char)) for i in range(0,4)]
        letter1_list = [random.choice(self.letter_cap) for i in range(0,2)]
        letter2_list = [random.choice(self.letter_low) for i in range(0,2)]
        tail = str(random.choice(self.tail))
        head = "".join(number1_list)
        body = f"{''.join(letter1_list)}{''.join(letter2_list)}"
        code = f"{head}{body}{tail}"
        if code in self.codes:
            self.generate()
        else:
            self.codes.append(code)
            with open(self.file,"w") as file:
                json.dump(self.codes,file)
            return code

    def clear_db(self):
        with open(self.file,"w") as file:
            json.dump([],file)