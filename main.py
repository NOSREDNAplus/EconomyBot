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
        d[user] = {"money": 0, "level": 0, "banked-money":0, "nickname": None,"products":{}, "products-owned":{}}
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
def getusernickname(user:str) -> str:
    a = None
    with open("data.json", "r") as f:
        d = json.load(f)
        for i in d.items():
            if i[0] == user:
                a = i[1]["nickname"]
    return a
def checkproductowned(user:str, item:str) -> None:
    x = (False, 0)
    with open("data.json", "r") as f:
        d = json.load(f)
        try:
            d[user]["products-owned"][item]
            x = (True, d[user]["products-owned"][item]["q"])
        except Exception as e:
            print(f"Encountered Error: {e}")
    return x
    
def getproduct(name:str) -> tuple:
    with open("data.json", "r") as f:
        d = json.load(f)
        p = None
        for i in d.items():
            u = i[0]
            for t in i[1]["products"].items():
                if t[0] == name:
                    p = (u, t[0], t[1])
                    break
        f.close()
    with open("data.json", "w") as f:
        f.write(json.dumps(d, indent=4))
        f.close()
    return p
def getproductquantity(name:str) -> int:
    with open("data.json", "r") as f:
        d = json.load(f)
        n = 0
        for i in d.items():
            for t in i[1]["products-owned"].items():
                if t[0] == name:
                    n += t[1]["q"]
        f.close()
    return n
def getnetworth(user:str) -> int:
    with open("data.json", "r") as f:
        d = json.load(f)
        p = 0
        for t in d[user]["products-owned"].items():
            print(t)
            p += t[1]["$"] * t[1]["q"]
        f.close()
    with open("data.json", "w") as f:
        f.write(json.dumps(d, indent=4))
        f.close()
    return p
def mainloop():
    while True:
        sleep(3600)
        with open("data.json", "r") as f:
            d = json.load(f)
            for i in d.values():
                if i["banked-money"] >  0:
                    i["banked-money"] = round(i.get("banked-money") + i.get("banked-money") * 0.5, 1)
            print("Interest allocated")
            f.close()
        with open("data.json", "w") as f:
            f.write(json.dumps(d, indent=4))
            f.close()
class MyClient(discord.Client):
    fiu = False
    def filebuffer(self):
        if self.fiu:
            pass
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        threading.Thread(target=mainloop).start()
    async def on_message(self, message):
        global interestrate
        if message.author == client.user:
            return
        if message.content.startswith('$changelog'):
            usercheck(message.author.name)
            #command code
            with open("data.json", "r") as f:
                d = json.load(f)
                await message.channel.send(f""">>> ### Changelog!\n# Shop! Shop! Shop! (Part 1.5)\n*10/18/24*\n- Added $nickname(beta) command""")
                f.close()
            with open("data.json", "w") as f:
                f.write(json.dumps(d, indent=4))
                f.close()
        if message.content.startswith("$buy"):
            usercheck(message.author.name)
            p = message.content.split(" ",2)
            #commmand code
            with open("data.json", "r") as f:
                d = json.load(f)
                if "-" in str(p[2]) or not str(p[2]).replace("-", "").replace(".","").isdigit():
                    return
                else:
                    p[2] = int(p[2].split(".")[0])
                if getproduct(p[1]) != None:
                    prod = getproduct(p[1])
                    i = 0
                    while i != p[2]:
                        if d[message.author.name]["money"] >= prod[2]["$"]:
                            d[message.author.name]["money"] -= prod[2]["$"]
                            #print(prod)
                            #print(getproductquantity(prod[1]), prod[2]["q"])
                            if getproductquantity(prod[1]) == prod[2]["q"]:
                                await message.channel.send(f">>> ***{message.author}***\n No more {prod[1]}(s) to be bought!")
                                return
                            d[prod[0]]["money"] += prod[2]["$"]
                            creat = False
                            for g in d[message.author.name]["products-owned"].keys():
                                #print(g, p[1])
                                if g == p[1]:
                                    creat = True
                                    break
                            if not creat:
                                d[message.author.name]["products-owned"][prod[1]] = {"$": prod[2]["$"], "q": 1}
                            else:
                                d[message.author.name]["products-owned"][prod[1]]["q"] += 1
                            await message.channel.send(f">>> ***{message.author}***\n Bought {p[1]}!")
                        else:
                            await message.channel.send(f">>> ***{message.author}***\n You don't have enough money!")
                            return
                        i += 1
                else:
                    await message.channel.send(f">>> ***{message.author}***\n Product doesn't exist!")
                    return
                f.close()
            with open("data.json", "w") as f:
                f.write(json.dumps(d, indent=4))
                f.close()
        if message.content.startswith('$ranks'):
            usercheck(message.author.name)
            #command code
            with open("data.json", "r") as f:
                d = json.load(f)
                l = []
                for i in d.items():
                    if i[1]["nickname"] != None:
                        l.append((f""""{i[1]["nickname"]}" - {i[0]}""", i[1]['money']+i[1]['banked-money']))
                    else:
                        l.append((i[0], i[1]['money']+i[1]['banked-money']))
                if len(l)-1 < 4:
                    r = 5 - (len(l)-1)
                    itr = 0
                    while r != itr:
                        l.append(("None", 0))
                        itr += 1
                t = sorted(l, key = lambda x: x[1], reverse = True) # I caved :(
                await message.channel.send(f">>> ***Rankings***\n- {t[0][0]} ${t[0][1]}\n- {t[1][0]} ${t[1][1]}\n- {t[2][0]} ${t[2][1]}\n- {t[3][0]} ${t[3][1]}\n- {t[4][0]} ${t[4][1]}")  
            with open("data.json", "w") as f:
                f.write(json.dumps(d, indent=4))
                f.close()
            print(f"Sucessfully showed {message.author} ranks")
        if message.content.startswith('$unbank'):
            usercheck(message.author.name)
            #command code
            with open("data.json", "r") as f:
                d = json.load(f)
                p = message.content.split(" ", 1)[1]
                if "-" in str(p) or not str(p).replace("-", "").replace(".","").isdigit():
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
                if "-" in str(p[2]) or not str(p[2]).replace("-", "").replace(".","").isdigit():
                    return
                else:
                    p = int(p.split(".")[0])
                if p > d[message.author.name]["money"]:
                    await message.channel.send(f">>> ***{message.author}***\n You don't have enough money!")
                    return
                d[message.author.name]["money"] = d[message.author.name]["money"] - int(p)
                d[message.author.name]["banked-money"] = d[message.author.name]["banked-money"] + int(p)
                await message.channel.send(f">>> ***{message.author}***\n Successfully banked ${p}!")
                print(f"Sucessfully banked {message.author}'s money")
                f.close()
            with open("data.json", "w") as f:
                f.write(json.dumps(d, indent=4))
                f.close()
        if message.content.startswith('$nickname'):
            if message.content.startswith("$"):
                usercheck(message.author.name)
                #commmand code
                p = message.content.split(" ",1)[1]
                with open("data.json", "r") as f:
                    d = json.load(f)
                    if p.lower() != "none":
                        for i in d.items():
                            if i[1]["nickname"] == p:
                                await message.channel.send(f">>> ***{message.author}***\n Nickname already in use!")
                                return
                        d[message.author.name]["nickname"] = p
                        await message.channel.send(f">>> ***{message.author}***\n Successfully set nickname!")
                    else:
                        d[message.author.name]["nickname"] = None
                        await message.channel.send(f">>> ***{message.author}***\n Successfully removed nickname!")
                    f.close()
                with open("data.json", "w") as f:
                    f.write(json.dumps(d, indent=4))
                    f.close()
        if message.content.startswith('$stats'):
            usercheck(message.author.name)
            #command code
            with open("data.json", "r") as f:
                d = json.load(f)
                await message.channel.send(f">>> **Stats***\nInterest Rate: {MyClient.interestrate}")
                print(f"Showed stats to {message.author.name}")
                f.close()
            with open("data.json", "w") as f:
                f.write(json.dumps(d, indent=4))
                f.close()
        if message.content.startswith('$profile'):
            usercheck(message.author.name)
            #command code
            with open("data.json", "r") as f:
                d = json.load(f)
                p = None
                if " " in message.content:
                    p = message.content.split(" ", 1)[1]
                if p != None:
                    if userexists(p):
                        l = []
                        for i in d.items():
                            l.append(i[1]['banked-money']+i[1]["money"])
                        t = sorted(l, reverse = True)
                        print(t)
                        if getusernickname(p) == None:
                            await message.channel.send(f""">>> ***{p}***\nWealth - Acccount: {int(float(d[p]["money"]))} Banked: {int(float(d[p]["banked-money"]))} Total: {int(float(d[p]["money"]+d[p]["banked-money"]))}\nRank: {t.index(d[p]["money"]+d[p]["banked-money"])+1}\nNet Worth: ${int(float(getnetworth(p)))}""")
                        else:
                            await message.channel.send(f""">>> ***"{getusernickname(p)}"*** - ***{p}***\nWealth - Acccount: {d[p]["money"]} Banked: {d[p]["banked-money"]} Total: {d[p]["money"]+d[p]["banked-money"]}\nRank: {t.index(d[p]["money"]+d[p]["banked-money"])+1}\nNet Worth: ${getnetworth(p)}""")
                    else:
                        await message.channel.send(f">>> ***{message.author.name}***\nUser doesn't exist!")
                        return
                else:
                    l = []
                    for i in d.items():
                        l.append(i[1]['banked-money']+i[1]["money"])
                    t = sorted(l,  reverse = True)
                    print(t)
                    if getusernickname(message.author.name) == None:
                        await message.channel.send(f""">>> ***{message.author.name}***\nWealth - Account: {d[message.author.name]["money"]} Banked: {d[message.author.name]["banked-money"]} Total: {d[message.author.name]["money"]+d[message.author.name]["banked-money"]}\nRank: {t.index(d[message.author.name]["money"]+d[message.author.name]["banked-money"])+1}\nNet Worth: ${getnetworth(message.author.name)}""")
                    else:
                        await message.channel.send(f""">>> ***"{getusernickname(message.author.name)}"*** - ***{message.author.name}***\nWealth - Account: {d[message.author.name]["money"]} Banked: {d[message.author.name]["banked-money"]} Total: {d[message.author.name]["money"]+d[message.author.name]["banked-money"]}\nRank: {t.index(d[message.author.name]["money"]+d[message.author.name]["banked-money"])+1}\nNet Worth: ${getnetworth(message.author.name)}""")
                print(f"Showed profile to {message.author.name}")
                f.close()
            with open("data.json", "w") as f:
                f.write(json.dumps(d, indent=4))
                f.close()
        if message.content.startswith('$?'):
            usercheck(message.author.name)
            #command code
            c = random.randint(1, 25)
            with open("data.json", "r") as f:
                d = json.load(f)
                await message.channel.send(f'>>> # Commands:\n- $beg [optional: times done]\n- $profile [optional: user]\n- $ranks [optional: user]\n- $gamble [money bet] [optional: times done]\n- $give [user] [amount]\n- $steal [user]\n- $bank [amount]\n- $unbank [amount]\n- $sell [name] [price] [quantity]\n- $buy [name] [quantity]\n- $shop [optional: username]\n- $trade [person] [item/rights] [item name] [amount: only with item]\n- $round\n- $nickname [name or "none" to remove]')
                f.close()
            with open("data.json", "w") as f:
                f.write(json.dumps(d, indent=4))
                f.close()
            print(f"Sucessfully added {c} dollar to {message.author}'s data directory")
        if message.content.startswith("$products"):
            usercheck(message.author.name)
            #commmand code
            with open("data.json", "r") as f:
                d = json.load(f)
                f.close()
            with open("data.json", "w") as f:
                f.write(json.dumps(d, indent=4))
                f.close()
        if message.content.startswith("$sell"):
            usercheck(message.author.name)
            #commmand code
            with open("data.json", "r") as f:
                d = json.load(f)
                p = message.content.split(" ")
                if "-" in str(p[2]) or not str(p[2]).replace("-", "").replace(".","").isdigit():
                    return
                elif "-" in str(p[3]) or not str(p[3]).replace("-", "").replace(".","").isdigit():
                    return
                else:
                    print(p[2], p[3])
                    p[2] = int(p[2])
                    p[3] = int(p[3])
                if p[2] * p[3] + (p[2] * p[3] * 0.5) > d[message.author.name]["money"]:
                    await message.channel.send(f">>> You don't have enough money to produce this item!\n\nMoney to Product = quantity * cost * 0.2 = {p[2] * p[3] + (p[2] * p[3] * 0.5)}")
                    return
                elif getproduct(p[1]) != None:
                    await message.channel.send(f">>> Product with the same name already exists!")
                    return
                else:
                    d[message.author.name]["products"][p[1]] = {"$": p[2], "q": p[3]}
                    d[message.author.name]["money"] -= p[2] * p[3] + (p[2] * p[3] * 0.5)
                    await message.channel.send(f">>> Successfully selling product, {p[1]}, price of production: {p[2] * p[3] + (p[2] * p[3] * 0.5)}")
                f.close()
            with open("data.json", "w") as f:
                f.write(json.dumps(d, indent=4))
                f.close()
        if message.content.startswith("$restock"):
            #$restock set Apple 20
            #$restock add Apple 15  
            pass
        if message.content.startswith("$shop"):
            if message.content.startswith("$"):
                usercheck(message.author.name)
                #commmand code
                with open("data.json", "r") as f:
                    d = json.load(f)
                    c = None
                    if " " in message.content:
                        c = message.content.split(" ", 1)[1]
                    if c != None:
                        p = []
                        for t in d[c]["products"].items():
                            p.append(f'{t[0]} ${t[1]["$"]} Avaliable Products: {t[1]["q"] - getproductquantity(t[0])}')
                        if getusernickname(c) == None:
                            await message.channel.send(f""">>> ***{c}'s Shop***\n- {'\n- '.join(p)}""")
                        else:
                            await message.channel.send(f""">>> ***{getusernickname(c)}'s Shop***\n- {'\n- '.join(p)}""")
                    else:
                        p = []
                        for i in d.items():
                            for t in i[1]["products"].items():
                                p.append(f'{t[0]} ${t[1]["$"]} Avaliable Products: {t[1]["q"] - getproductquantity(t[0])} Created By: {i[0]}')
                        await message.channel.send(f""">>> ***Shop***\n- {'\n- '.join(p)}""")
                    f.close()
                with open("data.json", "w") as f:
                    f.write(json.dumps(d, indent=4))
                    f.close()
        if message.content.startswith("$inventory"):
            usercheck(message.author.name)
            #commmand code
            with open("data.json", "r") as f:
                d = json.load(f)
                i = []
                p = None
                if " " in message.content:
                    p = message.content.split(" ", 1)[1]
                if p != None:
                    for k in d[p]["products-owned"].items():
                        i.append(f"{k[0]} x{k[1]["q"]}")
                    await message.channel.send(f""">>> ***{p}'s Inventory***\n{', '.join(i)}""")
                else:
                    for k in d[message.author.name]["products-owned"].items():
                        i.append(f"{k[0]} x{k[1]["q"]}")
                    await message.channel.send(f""">>> ***{message.author}'s Inventory***\n{', '.join(i)}""")
                f.close()
            with open("data.json", "w") as f:
                f.write(json.dumps(d, indent=4))
                f.close()
        if message.content.startswith('$slots'):
            usercheck(message.author.name)
            #command code
            p = None
            if " " in message.content:
                p = message.content.split(" ", 1)[1]
                if "-" in str(p) or not str(p).replace("-", "").replace(".","").isdigit():
                    return
                else:
                    p = int(p.split(".")[0])
                    if p > 15:
                        await message.channel.send(f'>>> ***{message.author}***\n beg max is 15!')
                        return
            with open("data.json", "r") as f:
                d = json.load(f)
                if p == None:
                    c = random.randint(1, 50)
                    if d[message.author.name]["money"] >= 5:
                        d[message.author.name]["money"] = d[message.author.name].get("money") - 5
                        if c == 1:
                            d[message.author.name]["money"] = d[message.author.name].get("money") + 25000
                            await message.channel.send(f'>>> ***{message.author}***\n rolled and got $25000 from ***The Slots***!')
                        else: 
                            await message.channel.send(f'>>> ***{message.author}***\n rolled and got nothing from ***The Slots***!')
                    else:
                        await message.channel.send(f">>> ***{message.author}***\n You don't have enough money!")
                        return
                else:
                    i = 0
                    while i != p:
                        c = random.randint(1, 100)
                        if d[message.author.name]["money"] >= 5:
                            d[message.author.name]["money"] = d[message.author.name].get("money") - 5
                            if c == 1:
                                d[message.author.name]["money"] = d[message.author.name].get("money") + 25000
                                await message.channel.send(f'>>> ***{message.author}***\n rolled and got $25000 from ***The Slots***!\nRoll: {i+1}/{p}')
                            else: 
                                await message.channel.send(f'>>> ***{message.author}***\n rolled and got nothing from ***The Slots***!\nRoll: {i+1}/{p}')
                        else:
                            await message.channel.send(f">>> ***{message.author}***\n You don't have enough money!")
                            return
                        i += 1
                f.close()
            with open("data.json", "w") as f:
                f.write(json.dumps(d, indent=4))
                f.close()
            print(f"Sucessfully added {c} dollar to {message.author}'s data directory")
        if message.content.startswith("$trade"):
            usercheck(message.author.name)
            #commmand code
            #$trade [person] [item/rights] [item name] [amount: only with item]
            p = None
            if " " in message.content:
                p = message.content.split(" ")
            else:
                print(f"damn this {message.author} stinks")
                return
            with open("data.json", "r") as f:
                d = json.load(f)
                if userexists(p[1]):
                    pass
                else:
                    await message.channel.send(f">>> ***{message.author}***\n {p[1]} doesn't exist!")
                    return
                #Checks if user owns rights to product if in rights mode
                if p[2] == "rights" and getproduct(p[3])[0].strip() != message.author.name:
                    await message.channel.send(f">>> ***{message.author}***\n {getproduct(p[3])[0]} has the rights to this product!")
                    return
                #Checks if user owns product if in item mode
                elif p[2] == "item" and checkproductowned(message.author.name, p[3])[0] == False:
                    await message.channel.send(f">>> ***{message.author}***\n {message.author.name} You don't own this product!")
                    return
                #item mode
                if p[2] == "rights":
                    d[p[1]]["products"][p[3]] = d[message.author.name]["products"][p[3]]
                    del d[message.author.name]["products"][p[3]]
                    await message.channel.send(f">>> ***{message.author}***\n you succssfully gave the rights of {p[3]} to {p[1]}!")
                if p[2] == "item":
                    if "-" in str(p[4]) or not str(p[4]).replace("-", "").replace(".","").isdigit():
                        return
                    else:
                        p[4] = int(p[4].split(".")[0])
                        print(p[4], checkproductowned(message.author.name, p[3])[1])
                        if p[4] > checkproductowned(message.author.name, p[3])[1]:
                            await message.channel.send(f">>> ***{message.author}***\n you don't have enough {p[3]}(s)!")
                            return
                    #Checks whether user has enough products to give
                    if d[message.author.name]["products-owned"][p[3]]["q"] - p[4] < 0:
                        await message.channel.send(f">>> ***{message.author}***\n you don't have enough {p[3]}(s)!")
                        return
                    else:
                        if d[message.author.name]["products-owned"][p[3]]["q"] - p[4] == 0:
                            del d[message.author.name]["products-owned"][p[3]]
                        else:
                            d[message.author.name]["products-owned"][p[3]]["q"] -= p[4]
                        if not p[3] in d[p[1]]["products-owned"].keys():
                            d[p[1]]["products-owned"][p[3]] = {"$":getproduct(p[3])[2], "q":0}
                        d[p[1]]["products-owned"][p[3]]["q"] += p[4]
                        await message.channel.send(f">>> ***{message.author}***\n you successfully gave {p[1]} {p[4]} {p[3]}(s)!")
                f.close()
            with open("data.json", "w") as f:
                f.write(json.dumps(d, indent=4))
                f.close()
        if message.content.startswith('$beg'):
            usercheck(message.author.name)
            #command code
            p = None
            if " " in message.content:
                p = message.content.split(" ", 1)[1]
                if "-" in str(p) or not str(p).replace("-", "").replace(".","").isdigit():
                    return
                else:
                    p = int(p.split(".")[0])
                    if p > 15:
                        await message.channel.send(f'>>> ***{message.author}***\n beg max is 15!')
                        return
            celebs = ["Barack Obama", "KSI", "Mr. Beast", "DanTDM", "Logan Paul", "Ava Kris Tyson", "P. Diddy", "Drake", "Kendrick Lamar", "Dr. Disrespect"]
            if p == None:
                with open("data.json", "r") as f:
                    d = json.load(f)
                    bc = random.randint(1, 50)
                    if bc == 1:
                        c = random.randint(50, 125)
                        celeb = random.choice(celebs)
                        d[message.author.name]["money"] += c
                        await message.channel.send(f'>>> ***{message.author}***\n begged and got ${c} from ***{celeb}***!')
                    else:
                        c = random.randint(1, 25)
                        d[message.author.name]["money"] = d[message.author.name].get("money") + c
                        await message.channel.send(f'>>> ***{message.author}***\n begged and got ${c}!')
                    f.close()
                with open("data.json", "w") as f:
                    print(f"Sucessfully added {c} dollar to {message.author}'s data directory")
                    f.write(json.dumps(d, indent=4))
                    f.close()
            else:
                i = 0
                while i != p:
                    with open("data.json", "r") as f:
                        d = json.load(f)
                        bc = random.randint(1, 50)
                        if bc == 1:
                            c = random.randint(50, 125)
                            celeb = random.choice(celebs)
                            d[message.author.name]["money"] += c
                            await message.channel.send(f'>>> ***{message.author}***\n begged and got ${c} from ***{celeb}***!\nRoll: {i+1}/{p}')
                        else:
                            c = random.randint(1, 25)
                            d[message.author.name]["money"] = d[message.author.name].get("money") + c
                            await message.channel.send(f'>>> ***{message.author}***\n begged and got ${c}\nRoll: {i+1}/{p}!')
                        f.close()
                    with open("data.json", "w") as f:
                        print(f"Sucessfully added {c} dollar to {message.author}'s data directory")
                        f.write(json.dumps(d, indent=4))
                        f.close()
                    i += 1
        if message.content.startswith('$gamble'):
            usercheck(message.author.name)
            #command code
            c = random.randint(1,2)
            p = message.content.split(" ")
            if len(p) -1 > 1:
                if "-" in str(p[1]) or not str(p[1]).replace("-", "").replace(".","").isdigit():
                    return
                elif "-" in str(p[2]) or not str(p[2]).replace("-", "").replace(".","").isdigit():
                    return
                else:
                    p[1] = int(p[1])
                    p[2] = int(p[2])
                    if p[2] > 15:
                        await message.channel.send(f'>>> ***{message.author}***\n gamble max is 15!')
                        return
                i = 0
                while i != p[2]:
                    with open("data.json", "r") as f:
                        d = json.load(f)
                        c = random.randint(1,2)
                        if p[1] >= d[message.author.name]["money"]:
                            await message.channel.send(f">>> ***{message.author}***\n You don't have enough money!")
                            return
                        if c == 1:
                            await message.channel.send(f'>>> ***{message.author}***\n gambled and won big ${p[1]*5}!\nRoll: {i+1}/{p[2]}')
                            d[message.author.name]["money"] = d[message.author.name]["money"] + p[1]*2.5
                        else:
                            await message.channel.send(f'>>> ***{message.author}***\n gambled and loss ${p[1]*2.5}!\nRoll: {i+1}/{p[2]}')
                            d[message.author.name]["money"] = d[message.author.name]["money"]  - p[1]*0.9
                        f.close()
                    with open("data.json", "w") as f:
                        f.write(json.dumps(d, indent=4))
                        f.close()
                    i += 1
            else:
                if "-" in str(p[1]) or not str(p[1]).replace("-", "").replace(".","").isdigit():
                    return
                else:
                    p[1] = int(p[1])
                with open("data.json", "r") as f:
                    d = json.load(f)
                    c = random.randint(1,2)
                    if p[1] >= d[message.author.name]["money"]:
                        await message.channel.send(f">>> ***{message.author}***\n You don't have enough money!")
                        return
                    if c == 1:
                        await message.channel.send(f'>>> ***{message.author}***\n gambled and won big ${p[1]*5}!')
                        d[message.author.name]["money"] = d[message.author.name]["money"] + p[1]*2.5
                    else:
                        await message.channel.send(f'>>> ***{message.author}***\n gambled and loss ${p[1]*2.5}!')
                        d[message.author.name]["money"] = d[message.author.name]["money"]  - p[1]*0.9
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
                if "-" in str(p[2]) or not str(p[2]).replace("-", "").replace(".","").isdigit():
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
        if message.content.startswith('$steal'):
            usercheck(message.author.name)
            #command code
            with open("data.json", "r") as f:
                d = json.load(f)
                p = message.content.split(" ", 1)[1]
                c = random.randint(1, 6)
                #make chance to get caught !
                if d[p]["money"] <= 0:
                    await message.channel.send(f">>> ***{message.author}***\n tried to steal from {p}, but they're broke!")
                    return
                if c == 1:
                    d[p]["money"] = d[p]["money"] - int(d[p]["money"]/5)
                    d[message.author.name]["money"] = d[message.author.name]["money"] + int(d[p]["money"]/1.5)
                    await message.channel.send(f""">>> ***{message.author}***\n tried to steal from {p}, and suceeded stealing ${int(d[p]["money"]/5)}!""")
                else:
                    d[message.author.name]["money"] -= 50
                    await message.channel.send(f">>> ***{message.author}***\n tried to steal from {p}, but you got caught lose $50!")
                f.close()
            with open("data.json", "w") as f:
                f.write(json.dumps(d, indent=4))
                f.close()
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
with open("token.txt", "r") as f:
    client.run(f.readline())
    f.close()
