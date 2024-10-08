import discord, json, random, threading
from time import sleep

#Command base functions
def userexists(user:str) -> bool:
    """Checks if a user exists."""
    with open("data.json", "r") as f:
        d, b = json.loads(f.read()), False
        for i in d:
            if user == i:
                b = True
                break
        f.close()
        return b
def adduser(user:str) -> None:
    """Adds user to database."""
    with open("data.json", "r") as f:
        d = json.load(f)
        d[user] = {"money": 0, "banked-money":0}
        f.close()
        with open("data.json", "w") as f:
            f.write(json.dumps(d, indent=4))
            f.close()
def usercheck(user:str) -> None:
    """Checks if a user exists and then adds them to the database."""
    if userexists(user):
        pass
    else:
        adduser(user)
        print(f"Sucessfully added {user} to data directory")
def mainloop():
    while True:
        sleep(3600)
        with open("data.json", "r") as f:
            d = json.load(f)
            for i in d.values():
                if i["money"] >  0:
                    i["money"] = round(i.get("money") + i.get("money") * 0.5, 1)
            print("Interest allocated")
            f.close()
        with open("data.json", "w") as f:
            f.write(json.dumps(d, indent=4))
            f.close()
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        threading.Thread(target=mainloop).start()
    async def on_message(self, message):
        if message.author == client.user:
            return
        if message.content.startswith('$changelog'):
            usercheck(message.author.name)
            #command code
            with open("data.json", "r") as f:
                d = json.load(f)
                await message.channel.send(f""">>> # Changelog!\n*10/7/24*\n- Removed $bank-balance now just use $balance\n- Changed all reponse text\n- Buffed Begging, cap is now $25]\n- If you succede in gambling you get 5x\n- Unbanked money will now gain 0.5% every 5 minutes\n- Celebrity beg chance\n- Halfed steal chance making it more likely\n- Removed KMS command\n- Added round command""")
                f.close()
            with open("data.json", "w") as f:
                f.write(json.dumps(d, indent=4))
                f.close()
        if message.content.startswith('$unbank'):
            usercheck(message.author.name)
            #command code
            with open("data.json", "r") as f:
                d = json.load(f)
                p = message.content.split(" ", 1)[1]
                if not str(p).replace("-", "").replace(".","").isdigit():
                    return
                else:
                    p = int(p.split(".")[0])
                if p > d[message.author.name]["banked-money"]:
                    await message.channel.send(f">>> ***{message.author}***\n You don't have enough money!")
                    return
                d[message.author.name]["banked-money"] = d[message.author.name]["banked-money"] - int(p)
                d[message.author.name]["money"] = d[message.author.name]["money"] + int(p)
                await message.channel.send(f""">>> ***{message.author}*** 
successfully unbanked ${p}""")
                f.close()
            with open("data.json", "w") as f:
                f.write(json.dumps(d, indent=4))
                f.close()
            print(f"Sucessfully un-banked {message.author}'s money")
        if message.content.startswith('$bank'):
            usercheck(message.author.name)
            #command code
            with open("data.json", "r") as f:
                d = json.load(f)
                p = message.content.split(" ", 1)[1]
                if not str(p).replace("-", "").replace(".","").isdigit():
                    return
                else:
                    p = int(p.split(".")[0])
                if p > d[message.author.name]["money"]:
                    await message.channel.send(f">>> ***{message.author}***\n You don't have enough money!")
                    return
                d[message.author.name]["money"] = d[message.author.name]["money"] - int(p)
                d[message.author.name]["banked-money"] = d[message.author.name]["banked-money"] + int(p)
                await message.channel.send(f"{message.author} successfully banked ${p}!")
                print(f"Sucessfully banked {message.author}'s money")
                f.close()
            with open("data.json", "w") as f:
                f.write(json.dumps(d, indent=4))
                f.close()
        if message.content.startswith('$help'):
            usercheck(message.author.name)
            #command code
            c = random.randint(1, 25)
            with open("data.json", "r") as f:
                d = json.load(f)
                await message.channel.send(f'>>> # Commands:\n $balance, $beg, $gamble, $give, $steal, $snoop, $bank, $unbank, $round')
                f.close()
            with open("data.json", "w") as f:
                f.write(json.dumps(d, indent=4))
                f.close()
            print(f"Sucessfully added {c} dollar to {message.author}'s data directory")
        if message.content.startswith('$beg'):
            usercheck(message.author.name)
            #command code
            p = None
            if " " in message.content:
                p = message.content.split(" ", 1)[1]
                if not str(p).replace("-", "").replace(".","").isdigit():
                    return
                else:
                    p = int(p.split(".")[0])
                    if p > 15:
                        await message.channel.send(f'>>> ***{message.author}***\n beg max is 15!')
                        return
            celebs = ["Barack Obama", "KSI", "Mr. Beast", "DanTDM", "Logan Paul", "Ava Kris Tyson", "P. Diddy", "Drake", "Kendrick Lamar", "Dr. Disrespect"]
            with open("data.json", "r") as f:
                d = json.load(f)
                if p == None:
                    bc = random.randint(1, 50)
                    if bc == 1:
                        c = random.randint(50, 125)
                        celeb = random.choice(celebs)
                        d[message.author.name]["money"] = d[message.author.name].get("money") + c
                        await message.channel.send(f'>>> ***{message.author}***\n begged and got ${c} from ***{celeb}***!')
                    else:
                        c = random.randint(1, 25)
                        d[message.author.name]["money"] = d[message.author.name].get("money") + c
                        await message.channel.send(f'>>> ***{message.author}***\n begged and got ${c}!')
                else:
                    i = 0
                    while i != p:
                        bc = random.randint(1, 50)
                        if bc == 1:
                            c = random.randint(50, 125)
                            celeb = random.choice(celebs)
                            d[message.author.name]["money"] = d[message.author.name].get("money") + c
                            await message.channel.send(f'>>> ***{message.author}***\n begged and got ${c} from ***{celeb}***!')
                        else:
                            c = random.randint(1, 25)
                            d[message.author.name]["money"] = d[message.author.name].get("money") + c
                            await message.channel.send(f'>>> ***{message.author}***\n begged and got ${c}!')
                        i += 1
                f.close()
            with open("data.json", "w") as f:
                f.write(json.dumps(d, indent=4))
                f.close()
            print(f"Sucessfully added {c} dollar to {message.author}'s data directory")
        if message.content.startswith('$gamble'):
            usercheck(message.author.name)
            #command code
            with open("data.json", "r") as f:
                d = json.load(f)
                c = random.randint(1,2)
                p = message.content.split(" ")
                if len(p) -1 > 1:
                    if not str(p[1]).replace("-", "").replace(".","").isdigit() and not str(p[2]).replace("-", "").replace(".","").isdigit():
                        return
                    else:
                        p[1] = int(p[1])
                        p[2] = int(p[2])
                        if p[2] > 15:
                            await message.channel.send(f'>>> ***{message.author}***\n beg max is 15!')
                            return
                    i = 0
                    while i != p[2]:
                        c = random.randint(1,2)
                        if p[1] > d[message.author.name]["money"]:
                            await message.channel.send(f">>> ***{message.author}***\n You don't have enough money!")
                            return
                        if c == 1:
                            await message.channel.send(f'>>> ***{message.author}***\n gambled and won big ${p[1]*5}!')
                            d[message.author.name]["money"] = d[message.author.name]["money"] + p[1]*5
                        else:
                            await message.channel.send(f'>>> ***{message.author}***\n gambled and loss ${p[1]*2.5}!')
                            d[message.author.name]["money"] = d[message.author.name]["money"]  - p[1]*2.5
                        i += 1
                else:
                    if not str(p[1]).replace("-", "").replace(".","").isdigit():
                        return
                    else:
                        p[1] = int(p[1])
                    if p[1] > d[message.author.name]["money"]:
                        await message.channel.send(f">>> ***{message.author}***\n You don't have enough money!")
                        return
                    if c == 1:
                        await message.channel.send(f'>>> ***{message.author}***\n gambled and won big ${p[1]*5}!')
                        d[message.author.name]["money"] = d[message.author.name]["money"] + p[1]*5
                    else:
                        await message.channel.send(f'>>> ***{message.author}***\n gambled and loss ${p[1]*2.5}!')
                        d[message.author.name]["money"] = d[message.author.name]["money"]  - p[1]*2.5
                f.close()
            with open("data.json", "w") as f:
                f.write(json.dumps(d, indent=4))
                f.close()
            print(f"Sucessfully added 1 dollar to {message.author}'s data directory")
        if message.content.startswith('$give'):
            usercheck(message.author.name)
            #command code
            with open("data.json", "r") as f:
                d = json.load(f)
                p = message.content.split(" ", 2)
                print("Command initiated ", p)
                if not str(p[2]).replace("-", "").replace(".","").isdigit():
                    return
                else:
                    p[2] = int(p[2])
                if p[2] > d[message.author.name]["money"]:
                    await message.channel.send(f">>> ***{message.author}***\n You don't have enough money!")
                    return
                d[message.author.name]["money"] = int(d[message.author.name]["money"]) - p[2]
                d[p[1]]["money"] = int(d[p[1]]["money"]) + int(p[2])
                await message.channel.send(f"{message.author} gave {p[1]} ${p[2]}!")
                f.close()
            with open("data.json", "w") as f:
                f.write(json.dumps(d, indent=4))
                f.close()
        if message.content.startswith("$round"):
            usercheck(message.author.name)
            #command code
            with open("data.json", "r") as f:
                d = json.load(f)
                d[message.author.name]["money"] = round(d[message.author.name]["money"])
                await message.channel.send(f""">>> ***{message.author}***\n Rounded your balance!""")
            with open("data.json", "w") as f:
                f.write(json.dumps(d, indent=4))
                f.close()
            print(f"Sucessfully rounded balance to {message.author}")
        if message.content.startswith('$balance'):
            usercheck(message.author.name)
            #command code
            with open("data.json", "r") as f:
                d = json.load(f)
                await message.channel.send(f""">>> ***{message.author}*** 
You Have ${d[message.author.name]["banked-money"]} in the bank and ${d[message.author.name]["money"]} in your account""")
                f.close()
            with open("data.json", "w") as f:
                f.write(json.dumps(d, indent=4))
                f.close()
            print(f"Sucessfully showed balance to {message.author}")
        if message.content.startswith('$steal'):
            usercheck(message.author.name)
            #command code
            with open("data.json", "r") as f:
                d = json.load(f)
                p = message.content.split(" ", 1)[1]
                c = random.randint(1, 6)
                #make chance to get caught !
                if d[p]["money"] < 0:
                    await message.channel.send(f">>> ***{message.author}***\n tried to steal from {p}, but they're broke!")
                    return
                if c == 1:
                    d[p]["money"] = d[p]["money"] - int(d[p]["money"]/5)
                    d[message.author.name]["money"] = d[message.author.name]["money"] + int(d[p]["money"]/5)
                    await message.channel.send(f">>> ***{message.author}***\n tried to steal from {p}, and suceeded stealing ${int(d[p]["money"]/5)}!")
                else:
                    await message.channel.send(f">>> ***{message.author}***\n tried to steal from {p}, but failed!")
                f.close()
            with open("data.json", "w") as f:
                f.write(json.dumps(d, indent=4))
                f.close()
        if message.content.startswith('$snoop'):
            usercheck(message.author.name)
            #command code
            with open("data.json", "r") as f:
                d = json.load(f)
                p = message.content.split(" ", 1)[1]
                await message.channel.send(f">>> ***{p}***\n has ${d[p]["money"]}")
                f.close()
            with open("data.json", "w") as f:
                f.write(json.dumps(d, indent=4))
                f.close()
            print(f"Sucessfully showed balance to {message.author}")
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
with open("token.txt", "r") as f:
    client.run(f.readline())
    f.close()