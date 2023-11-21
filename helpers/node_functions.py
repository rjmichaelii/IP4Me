import random
import string

def Node1(input: dict)->dict:
    rand_num = random.randint(0,1000)
    print(f"Recieved Request from {input['SourceNode']} - Generated Random Number")
    input["Message"] = str(rand_num)
    return input

def Node2(input: dict)->dict:
    print(f"Recieved Request from {input['SourceNode']} - Lowercased Message")
    input["Message"] = input["Message"].lower()
    return input

def Node3(input: dict)->dict:
    print(f"Recieved Request from {input['SourceNode']} - Uppercased Message")
    input["Message"] = input["Message"].upper()
    return input

def Node4(input: dict)->dict:
    print(f"Recieved Request from {input['SourceNode']} - Generated Random String")
    input["Message"] = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    return input