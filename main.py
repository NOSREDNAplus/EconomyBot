import discord, json, random, threading
from time import sleep

def userexists(user:str) -> bool:
    with open("data.json", "r") as f:
        d, b = json.loads(f.read()), False
        for i in d:
            if user == i:
                b = True
                break
        f.close()
        return b
def adduser(user:str) -> None:
    with open("data.json", "r") as f:
        d = json.load(f)
        d[user] = {"money": 0, "banked-money":0}
        f.close()
        with open("data.json", "w") as f:
            f.write(json.dumps(d, indent=4))
            f.close()
def mainloop():
    while True:
        sleep(3600)
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
    async def on_message(self, message):
        if message.author == client.user:
            return
        if message.content.startswith('$changelog'):
            if userexists(message.author.name):
                with open("data.json", "r") as f:
                    d = json.load(f)
                    await message.channel.send(f"""# Changelog!\n10/6/24\n- Added Banking""")
                    f.close()
                with open("data.json", "w") as f:
                    f.write(json.dumps(d, indent=4))
                    f.close()
            else:
                adduser(message.author.name)
                print(f"Sucessfully added {message.author} to data directory")
        if message.content.startswith('$bank-balance'):
            if userexists(message.author.name):
                with open("data.json", "r") as f:
                    d = json.load(f)
                    d[message.author.name]["banked-money"]
                    print(type(message.author))
                    await message.channel.send(f'{message.author} you have ${d[message.author.name]["banked-money"]} in the bank')
                    f.close()
                with open("data.json", "w") as f:
                    f.write(json.dumps(d, indent=4))
                    f.close()
                print(f"Sucessfully showed banked balance to {message.author}")
            else:
                adduser(message.author.name)
                print(f"Sucessfully added {message.author} to data directory")
        if message.content.startswith('$unbank'):
            if userexists(message.author.name):
                with open("data.json", "r") as f:
                    d = json.load(f)
                    p = message.content.split(" ", 1)[1]
                    if not str(p).replace("-", "").replace(".","").isdigit():
                        return
                    else:
                        p = int(p.split(".")[0])
                    if p > d[message.author.name]["banked-money"]:
                        await message.channel.send(f"{message.author} you don't have enough money!")
                        return
                    d[message.author.name]["banked-money"] = d[message.author.name]["banked-money"] - int(p)
                    d[message.author.name]["money"] = d[message.author.name]["money"] + int(p)
                    await message.channel.send(f"{message.author} successfully un-banked ${p}!")
                    print(f"Sucessfully un-banked {message.author}'s money")
                    f.close()
                with open("data.json", "w") as f:
                    f.write(json.dumps(d, indent=4))
                    f.close()
            else:
                adduser(message.author.name)
        if message.content.startswith('$bank'):
            if userexists(message.author.name):
                with open("data.json", "r") as f:
                    d = json.load(f)
                    p = message.content.split(" ", 1)[1]
                    if not str(p).replace("-", "").replace(".","").isdigit():
                        return
                    else:
                        p = int(p.split(".")[0])
                    if p > d[message.author.name]["money"]:
                        await message.channel.send(f"{message.author} you don't have enough money!")
                        return
                    d[message.author.name]["money"] = d[message.author.name]["money"] - int(p)
                    d[message.author.name]["banked-money"] = d[message.author.name]["banked-money"] + int(p)
                    await message.channel.send(f"{message.author} successfully banked ${p}!")
                    print(f"Sucessfully banked {message.author}'s money")
                    f.close()
                with open("data.json", "w") as f:
                    f.write(json.dumps(d, indent=4))
                    f.close()
            else:
                adduser(message.author.name)
        if message.content.startswith('$help'):
            if userexists(message.author.name):
                c = random.randint(1, 5)
                with open("data.json", "r") as f:
                    d = json.load(f)
                    await message.channel.send(f'Commands: $balance, $beg, $gamble, $give, $kms, $steal, $snoop, $bank, $bank-balance, $unbank')
                    f.close()
                with open("data.json", "w") as f:
                    f.write(json.dumps(d, indent=4))
                    f.close()
                print(f"Sucessfully added {c} dollar to {message.author}'s data directory")
            else:
                adduser(message.author.name)
                print(f"Sucessfully added {message.author} to data directory")
        if message.content.startswith('$beg'):
            if userexists(message.author.name):
                c = random.randint(1, 5)
                with open("data.json", "r") as f:
                    d = json.load(f)
                    d[message.author.name]["money"] = d[message.author.name].get("money") + c
                    print(d)
                    f.close()
                with open("data.json", "w") as f:
                    f.write(json.dumps(d, indent=4))
                    f.close()
                print(f"Sucessfully added {c} dollar to {message.author}'s data directory")
                await message.channel.send(f'{message.author} begged and got ${c}!')
            else:
                adduser(message.author.name)
                print(f"Sucessfully added {message.author} to data directory")
        if message.content.startswith('$gamble'):
            if userexists(message.author.name):
                with open("data.json", "r") as f:
                    d = json.load(f)
                    c = random.randint(1,2)
                    p = message.content.split(" ", 1)[1]
                    if not str(p).replace("-", "").replace(".","").isdigit():
                        return
                    else:
                        p = int(p)
                    if p > d[message.author.name]["money"]:
                        await message.channel.send(f"{message.author} you don't have enough money!")
                        return
                    if c == 1:
                        await message.channel.send(f'{message.author} gambled and won big ${p*1.5}!')
                        d[message.author.name]["money"] = d[message.author.name].get("money") + p*1.5
                    else:
                        await message.channel.send(f'{message.author} gambled and loss ${p*2.5}!')
                        d[message.author.name]["money"] = d[message.author.name].get("money") - p*2.5
                    print(d)
                    f.close()
                with open("data.json", "w") as f:
                    f.write(json.dumps(d, indent=4))
                    f.close()
                print(f"Sucessfully added 1 dollar to {message.author}'s data directory")
            else:
                adduser(message.author.name)
                print(f"Sucessfully added {message.author} to data directory")
        if message.content.startswith('$give'):
            if userexists(message.author.name):
                with open("data.json", "r") as f:
                    d = json.load(f)
                    p = message.content.split(" ", 2)
                    print("Command initiated ", p)
                    if not str(p[2]).replace("-", "").replace(".","").isdigit():
                        return
                    else:
                        p[2] = int(p[2])
                    if p[2] > d[message.author.name]["money"]:
                        print("HJelll")
                        await message.channel.send(f"{message.author} you don't have enough money!")
                        return
                    d[message.author.name]["money"] = int(d[message.author.name]["money"]) - p[2]
                    d[p[1]]["money"] = int(d[p[1]]["money"]) + int(p[2])
                    await message.channel.send(f"{message.author} gave {p[1]} ${p[2]}!")
                    f.close()
                with open("data.json", "w") as f:
                    f.write(json.dumps(d, indent=4))
                    f.close()
                #print(f"Sucessfully killed {message.author}")
            else:
                adduser(message.author.name)
                print(f"Sucessfully added {message.author} to data directory")
        if message.content.startswith('$kms'):
            if userexists(message.author.name):
                with open("data.json", "r") as f:
                    d = json.load(f)
                    await message.channel.send(f'{message.author} killed him self :sob:')
                    d[message.author.name]["money"] = 0
                    f.close()
                with open("data.json", "w") as f:
                    f.write(json.dumps(d, indent=4))
                    f.close()
                print(f"Sucessfully killed {message.author}")
            else:
                adduser(message.author.name)
                print(f"Sucessfully added {message.author} to data directory")
        if message.content.startswith('$balance'):
            if userexists(message.author.name):
                with open("data.json", "r") as f:
                    d = json.load(f)
                    d[message.author.name]["money"]
                    print(type(message.author))
                    await message.channel.send(f'{message.author} you have ${d[message.author.name]["money"]}')
                    f.close()
                with open("data.json", "w") as f:
                    f.write(json.dumps(d, indent=4))
                    f.close()
                print(f"Sucessfully showed balance to {message.author}")
            else:
                adduser(message.author.name)
                print(f"Sucessfully added {message.author} to data directory")
            #await message.channel.send(f'Hello, {message.author}!')
        if message.content.startswith('$steal'):
            if userexists(message.author.name):
                with open("data.json", "r") as f:
                    d = json.load(f)
                    p = message.content.split(" ", 1)[1]
                    c = random.randint(1, 12)
                    #d[message.author.name]["money"]
                    if c == 1:
                        d[p]["money"] = d[p]["money"] - int(d[p]["money"]/5)
                        d[message.author.name]["money"] = d[message.author.name]["money"] + int(d[p]["money"]/5)
                        await message.channel.send(f"{message.author} tried to steal from {p}, and suceeded!")
                    else:
                        await message.channel.send(f"{message.author} tried to steal from {p}, but failed!")
                    f.close()
                with open("data.json", "w") as f:
                    f.write(json.dumps(d, indent=4))
                    f.close()
                #print(f"Sucessfully showed balance to {message.author}")
            else:
                adduser(message.author.name)
                print(f"Sucessfully added {message.author} to data directory")
            #await message.channel.send(f'Hello, {message.author}!')
        if message.content.startswith('$snoop'):
            if userexists(message.author.name):
                with open("data.json", "r") as f:
                    d = json.load(f)
                    p = message.content.split(" ", 1)[1]
                    #d[message.author.name]["money"]
                    await message.channel.send(f"{p} has ${d[p]["money"]}")
                    f.close()
                with open("data.json", "w") as f:
                    f.write(json.dumps(d, indent=4))
                    f.close()
                print(f"Sucessfully showed balance to {message.author}")
            else:
                adduser(message.author.name)
                print(f"Sucessfully added {message.author} to data directory")
            #await message.channel.send(f'Hello, {message.author}!')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
with open("token.txt", "r") as f:
    client.run(f.readline())
    f.close()