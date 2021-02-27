import discord
import asyncio
import random
import json
from os import getcwd, path
from discord.ext import commands
from mods import XP as DRAWXP
from mods import Rates as RATE
from mods import ProvsCon as PC

cwd = getcwd()
intents = discord.Intents().all()
bot = commands.Bot(command_prefix="+",intents=intents,help_command=None)
#bot info
version = "< MOOD 0.1 >"

#to do list
droprate = [1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,3,3,3,3,4,4,4]
damage = {"Clay":[5,15],"Bronze":[50,100],"Silver":[300,900],"Iron":[1000,2000],"Gold":[5000,10000]}

@bot.event
async def on_ready():
    #await bot.guilds[0].text_channels[2].send("The Bot is now Online!")
    print('online')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=". Just watching"))

@bot.command(pass_context=True,aliases=['h'])
@commands.guild_only()
async def help(ctx):
    with open(path.join("server\\help.txt"),"r") as h:
        text = h.read()
        h.close()
    embed = discord.Embed(title="Help Page",description="Help Page for MOOD bot!",colour=ctx.author.roles[-1].color)
    embed.add_field(name="Commands",value=text)
    embed.set_footer(text=version)
    await ctx.send(embed=embed)

@bot.command(pass_context=True,aliases=['v'])
@commands.guild_only()
async def verify(ctx):
    user = ctx.author
    ID = user.id
    emoji = bot.get_emoji(773273771606933535)
    if emoji == None:
        emoji = ":crossed_swords:"
    embed = discord.Embed(title=f"{emoji} Make and Account! {emoji}",description="Follow the instructions below!",colour=user.roles[-1].color)
    embed.set_footer(text=version)
    embed.add_field(name="Instructions:",value=":one:Type in the code given below\n\n20udwa\n\n:two:Have fun on the MOOD server!")
    await user.send(embed=embed)
    def check(m):
        return  m.author == user
    v = await bot.wait_for('message',check=check,timeout=15)
    if v.content != "20udwa":
        embed = discord.Embed(title="Wrong answer",description="Retry the verification process!",color=user.roles[-1].color)
        embed.set_footer(text=version)
        await user.send(embed=embed)
        return
    #add user info to json
    with open(path.join(cwd, "server\\user_stats.json"),"r") as stats:
        data = json.load(stats)
        try:
            data[str(ID)]
        except:
            data[str(ID)] = {"level":1,"rank":"Clay","XP":0,"MAXHP":100,
                            "HP":100,"DMG":3,"MAXXP":100,"description":"An aspiring adventurer!",
                            "money":0,"armor":0,"using":{"head":"None","chest":"None","pants":"None",
                            "boots":"None","weapon":"None"}}
        stats.close()
    with open(path.join(cwd, "server\\user_stats.json"),"w") as stats:
        json.dump(data, stats, indent=2, sort_keys=True)
        stats.close()
    #send completion
    embed = discord.Embed(title=f"{emoji} Verification Complete! {emoji}", description="You can return to the server!", colour=user.roles[-1].color)
    embed.set_footer(text=version)
    await user.send(embed=embed)

@bot.command(pass_context=True,aliases=["stat","s"])
@commands.guild_only()
#@commands.cooldown(3,60,commands.BucketType.user)
async def status(ctx, member: discord.Member=None):
    if member == None:
        member = ctx.author
    user = member
    ID = user.id
    emoji = bot.get_emoji(773273771606933535)
    if emoji == None:
        emoji = ":smile:"
    status = str(user.status).upper()
    name = str(user).split("#")[0]
    with open(path.join(cwd, "server\\user_stats.json"),"r") as stats:
        data = json.load(stats)
        LVL = "`"+str(data[str(ID)]["level"])+"`"
        RANK = "`"+str(data[str(ID)]["rank"])+"`"
        XP = "`"+str(data[str(ID)]["XP"])+"`"
        DES = data[str(ID)]["description"]
        HP = data[str(ID)]["HP"]
        stats.close()

    embed = discord.Embed(title=f"{emoji} Status of {name}! {emoji}",description=f"STATUS: {status}",colour=user.roles[-1].color)
    embed.add_field(name="DESCRIPTION:",value=str(DES),inline=False)
    embed.add_field(name="User Level:",value=str(LVL),inline=True)
    embed.add_field(name="Health:",value=f"`{HP}`:heart:")
    embed.set_footer(text=version)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="RANK",value=str(RANK),inline=True)
    #SET THE XP AMOUNT TO AN IMAGE!!!
    n = DRAWXP.Load_XP(data[str(ID)]["MAXXP"],data[str(ID)]["XP"])
    n.save_img()
    f = discord.File(path.join(cwd, "images\\temp.png"),filename="img.png")
    embed.set_image(url=f"attachment://img.png")
    embed.add_field(name="XP",value=str(XP),inline=False)
    await ctx.send(file=f,embed=embed)
    f.close()
    n.close()

@status.error
async def status_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="Don't spam this command!", description="Please wait {:.0f}s before using this command!".format(error.retry_after),colour=discord.Colour.dark_gray())
        embed.set_footer(text=version)
        await ctx.send(embed=embed)
    print(error)

@bot.command(pass_context=True,aliases=['pro','p'])
@commands.guild_only()
#@commands.cooldown(3,60,commands.BucketType.user)
async def profile(ctx):
    user = ctx.author
    with open(path.join(cwd, "server\\user_stats.json"),"r") as stats:
        data = json.load(stats)
        name = str(user).split("#")[0]
        health = data[str(user.id)]["HP"]
        maxhealth = data[str(user.id)]["MAXHP"]
        damage = data[str(user.id)]["DMG"]
        maxXP = data[str(user.id)]["MAXXP"]
        XP = data[str(user.id)]["XP"]
        rank = data[str(user.id)]["rank"]
        money = data[str(user.id)]["money"]
        level = data[str(user.id)]["level"]
        description = data[str(user.id)]["description"]
        armor = data[str(user.id)]["armor"]
        using = data[str(user.id)]["using"]
        head = using["head"]
        chest = using["chest"]
        pants = using["pants"]
        boots = using["boots"]
        weapon = using["weapon"]
        stats.close()
    emblem = bot.get_emoji(809464420827660300)
    embed=discord.Embed(title=f"The profile of {name}",description=f"{description}",colour=user.roles[-1].color)
    embed.set_footer(text=version)
    embed.set_author(name=f"{name}",icon_url=user.avatar_url)
    embed.add_field(name=f"{name}'s RANK:",value=f"{rank}",inline=False)
    embed.add_field(name=f"{name}:",value=description,inline=False)
    healthpercent = health / maxhealth
    healthpercent *= 100
    embed.add_field(name="HP:",value=f"{int(health)}:heart: ({healthpercent:.2f}%)",inline=True)
    xppercent = XP / maxXP
    xppercent *= 100
    embed.add_field(name="XP:",value=f"{XP}{emblem} ({xppercent:.2f}%)",inline=True)
    embed.add_field(name=f"{name}'s wallet:",value=f"{money}",inline=True)
    nextLevel = maxXP - XP
    armoremoji = bot.get_emoji(807287558450970634)
    statistics = [f"MaxHP - {maxhealth:.2f}:heart:",f"XP until next level - {nextLevel:.2f}{emblem}",f"Damage - {damage:.2f}:crossed_swords:",f"Armor - {armor}{armoremoji}"]
    embed.add_field(name=f"{name}'s Stats:",value="\n".join(statistics),inline=False)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="{}".format("-" * 30),value="{}".format("-"*30),inline=False)
    equippedItems = [f"Helmet   - {head}",f"Chestplate - {chest}",f"Pants   - {pants}",f"Boots  - {boots}",f"Weapon - {str(weapon).upper()}"]
    embed.add_field(name="Currently Equipped:",value="\n".join(equippedItems),inline=False)
    await ctx.send(embed=embed)

@profile.error
async def profile_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed=discord.Embed(title="This command is on cooldown!",description="Wait {:.0f}s before using this command again!".format(error.retry_after),colour=discord.Colour.dark_gray())
        embed.set_footer(text=version)
        await ctx.send(embed=embed)
    else:
        print(error)

@bot.command(pass_context=True,aliases=['des','setdes','set description'])
@commands.guild_only()
@commands.cooldown(2,60,commands.BucketType.user)
async def description(ctx, *description):
    user = ctx.author
    ID = user.id
    #check length of description
    if len(description) < 1:
        embed = discord.Embed(title="There is nothing to set your description to.",description="Please enter something to set your description as.",colour=discord.Colour.dark_gray())
        embed.set_footer(text=version)
        await ctx.send(embed=embed)
        return
    #get info
    with open(path.join(cwd, "server\\user_stats.json"),"r") as stats:
        data = json.load(stats)
        if str(ctx.author.id) not in list(data.keys()):
            embed = discord.Embed(title="You do not have an account!",description="Please use the `/account` command to make your account!",colour=discord.Colour.dark_gray())
            embed.set_footer(text=version)
            await ctx.send(embed=embed)
            stats.close()
            return
        user_data = data[str(ID)]
        user_data["description"] = " ".join(description)
        stats.close()
    with open(path.join(cwd, "server\\user_stats.json"), "w") as stats:
        json.dump(data, stats, indent=2, sort_keys=True)
        stats.close()
    
    embed = discord.Embed(title="Description has been set!",description="You can check your description with the `/status` command!",colour=user.roles[-1].color)
    embed.set_footer(text=version)
    await ctx.send(embed=embed)

@description.error
async def description_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="Please wait before using this command again!", description="Please wait {:.0f}s before using this command!".format(error.retry_after),colour=discord.Colour.dark_gray())
        embed.set_footer(text=version)
        await ctx.send(embed=embed)

@bot.command(pass_context=True,aliases=[])
@commands.guild_only()
#@commands.cooldown(1,30,commands.BucketType.user)
async def hunt(ctx):
    user = ctx.author
    ID = user.id
    #get monster type
    with open(path.join(cwd, "server\\user_stats.json"),"r") as stats:
        sdata = json.load(stats)
        if str(ID) not in list(sdata.keys()):
            embed = discord.Embed(title="You do not have an account!",description="Please use the `/account` command to make your account!",colour=discord.Colour.dark_gray())
            embed.set_footer(text=version)
            await ctx.send(embed=embed)
            stats.close()
            return
        sdata[str(ID)]
        rank = sdata[str(ID)]["rank"]
        REDUCE = sdata[str(ID)]["DMG"]
        armor = sdata[str(ID)]["armor"]
        stats.close()
    with open(path.join(cwd, "server\\monsters.json"),"r") as mobs:
        data = json.load(mobs)
        mob = list(data[str(rank)].keys())
        mob = random.choice(mob)
        temp = list(data[str(rank)][str(mob)].keys())
        temp.remove("type")
        drop = random.choice(temp)
        amount = random.choice(droprate)
        mobs.close()
    #user damage and stuff
    r = damage[str(rank)]
    DMG = random.randint(r[0],r[1])
    DMG = DMG - REDUCE - armor
    if DMG < 0:
        DMG = 0
    sdata[str(ID)]["HP"] -= DMG
    HP = sdata[str(ID)]["HP"]
    if sdata[str(ID)]["HP"] <= 0:
        dead = True
        sdata[str(ID)]["HP"] = 1
        if sdata[str(ID)]["level"] == 1:
            pass
        else:
            sdata[str(ID)]["level"] -= 1
            x = int(sdata[str(ID)]["MAXXP"]) * (1.2**-int(sdata[str(ID)]["level"])) * 100
            sdata[str(ID)]["MAXXP"] = x
    else:
        dead = False
            #reduce health
        #add xp
        rate = RATE.convert(str(rank))
        XP = random.randint(rate * 5, rate * 20)
        MAXXP = sdata[str(ID)]["MAXXP"]
        total_XP = sdata[str(ID)]["XP"] + XP
        if total_XP >= MAXXP:
            sdata[str(ID)]["XP"] = int(total_XP - MAXXP)
            sdata[str(ID)]["MAXXP"] = int(MAXXP * 1.2)
            sdata[str(ID)]["level"] += 1
            sdata[str(ID)]["MAXHP"] *= 1.2
            sdata[str(ID)]["HP"] = int(HP * 1.03)
        else:
            sdata[str(ID)]["XP"] = int(total_XP)
        #money
        earned = random.randint(rate*10, rate*20)
        sdata[str(ID)]["money"] += int(earned)
    
    #write onto json
    with open(path.join(cwd, "server\\user_stats.json"),"w") as stats:
        json.dump(sdata, stats, indent=2, sort_keys=True)
        stats.close()
    name = str(user).split("#")[0]
    embed = discord.Embed(title=f"{name} went Hunting!",description=f"Rank: {rank}",colour=user.roles[-1].color)
    embed.set_footer(text=version)
    embed.set_thumbnail(url=user.avatar_url)
    embed.set_author(name="STATS")
    if dead:
        embed.add_field(name="RESULTS",value=f"`{name}` fought a `{mob}` but died in the process. They managed to be saved by a nearby adventurer.")
    else:
        embed.add_field(name="RESULTS",value=f"`{name}` fought a `{mob}` and managed to get `{amount}` `{drop}`.\nThey took `{DMG}` damage and have `{HP}` health.")
    #add items to inventory
    with open(path.join(cwd, "server\\user_inv.json"),"r") as inv:
        invs = json.load(inv)
        try:
            invs[str(ID)]
        except:
            invs[str(ID)] = {}
        if str(drop) not in list(invs[str(ID)].keys()):
            invs[str(ID)][str(drop)] = int(amount)
        else:
            invs[str(ID)][str(drop)] += int(amount)
        inv.close()
    with open(path.join(cwd, "server\\user_inv.json"),"w") as inv:
        json.dump(invs, inv, indent=2, sort_keys=True)
        inv.close()
    await ctx.send(embed=embed)

@hunt.error
async def hunt_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="You bloodthirsty adventurer, chillax!", description="Please wait {:.0f}s before using this command!".format(error.retry_after),colour=discord.Colour.dark_gray())
        embed.set_footer(text=version)
        await ctx.send(embed=embed)
    else:
        print("HUNT FAILED< SOMETHING WENT WRONG!!!")
        print(error)

@bot.command(pass_context=True,aliases=['store'])
@commands.guild_only()
@commands.cooldown(3,30,commands.BucketType.user)
async def shop(ctx, page: int=1):
    s = 7 * (page - 1)
    limit = 7 * page
    with open(path.join(cwd, "server\\shop_items.json"),"r") as shop:
        data = json.load(shop)
        items = list(data.keys())
        shop.close()
    output = []
    for x in range(s, limit):
        try:
            i = items[x]
        except:
            break
        c = data[str(i)]["cost"]
        e = data[str(i)]["emoji"]
        e = bot.get_emoji(int(e))
        s = f"{e}`{i}`  -  `{c}`"
        output.append(s)
    output = "\n".join(output)
    embed = discord.Embed(title="Welcome to the Shop!",description=f"Here are the items for page {page}",colour=ctx.author.roles[-1].color)
    embed.set_footer(text=version)
    embed.add_field(name="ITEMS",value=str(output))
    embed.set_thumbnail(url=ctx.guild.icon_url)
    await ctx.send(embed=embed)

@shop.error
async def shop_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="Command on Cooldown!", description="Please wait {:.0f}s before using this command!".format(error.retry_after),colour=discord.Colour.dark_gray())
        embed.set_footer(text=version)
        await ctx.send(embed=embed)
    else:
        print(error)

@bot.command(pass_context=True,aliases=['purchase','b'])
@commands.guild_only()
@commands.cooldown(2,30,commands.BucketType.user)
async def buy(ctx, item: str=None, amount: int=1):
    if item == None:
        embed = discord.Embed(title="No item!",description="You did not specify an item you want to buy!")
        embed.set_footer(text=version)
        await ctx.send(embed=embed)
        return
    with open(path.join(cwd, "server\\shop_items.json"),"r") as shop:
        data = json.load(shop)
        items = list(data.keys())
        if str(item) not in items:
            embed = discord.Embed(title="That is not an Item!",description="The item you specified does not exist or has a spelling error!\nPlease check!")
            embed.set_footer(text=version)
            await ctx.send(embed=embed)
            shop.close()
            return
        else:
            cost = int(data[str(item)]["cost"]) * amount
            emoji = bot.get_emoji(int(data[str(item)]["emoji"]))
        shop.close()
    user = ctx.author
    ID = user.id
    with open(path.join(cwd, "server\\user_stats.json"),"r") as users:
        data = json.load(users)
        if str(ctx.author.id) not in list(data.keys()):
            embed = discord.Embed(title="You do not have an account!",description="Please use the `/account` command to make your account!")
            embed.set_footer(text=version)
            await ctx.send(embed=embed)
            users.close()
            return
        user_money = data[str(ID)]["money"]
        if int(user_money) < cost:
            embed = discord.Embed(title="Try not to scam shops too much!",description="You do not have enough money!")
            embed.set_footer(text=version)
            await ctx.send(embed=embed)
            return
        else:
            data[str(ID)]["money"] -= cost
        users.close()
    with open(path.join(cwd, "server\\user_stats.json"),"w") as users:
        json.dump(data, users, indent=2, sort_keys=True)
        users.close()
    with open(path.join(cwd, "server\\user_inv.json"),"r") as invs:
        data = json.load(invs)
        INV = data[str(ID)]
        if str(item) in list(INV.keys()):
            data[str(ID)][str(item)] += int(amount)
        else:
            data[str(ID)][str(item)] = int(amount)
        invs.close()
    with open(path.join(cwd, "server\\user_inv.json"),"w") as invs:
        json.dump(data, invs, indent=2, sort_keys=True)
        invs.close()
    s = "{} bought {} {} for ${}".format(str(user).split("#")[0],amount,emoji,cost)
    embed = discord.Embed(title="Purchase Successful!",description="_ _",colour=user.roles[-1].color)
    embed.set_footer(text=version)
    embed.set_author(name=str(user).split("#")[0])
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.add_field(name="content",value=s)
    await ctx.send(embed=embed)

@buy.error
async def buy_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="Command is on Cooldown!",description="Please wait {:.0f}s before using this command!".format(error.retry_after))
        embed.set_footer(text=version)
        await ctx.send(embed=embed)
    
    print(error)  

@bot.command(pass_context=True)
@commands.guild_only()
async def heal(ctx, power="", amount=1):
    user = ctx.author
    with open(path.join(cwd, "server\\user_inv.json"),"r") as invs:
        idata = json.load(invs)
        u = idata[str(user.id)]
        potion = "health_potion"
        if power == "_":
            pass
        elif len(power) != 0:
            potion = power + "_" + potion
        if potion not in u:
            embed = discord.Embed(title="You do not have any Potions!",description="No potions therefore no healing!",colour=ctx.author.roles[-1].color)
            embed.set_footer(text=version)
            await ctx.send(embed=embed)
            invs.close()
            return
        elif u[potion] <= 0:
            embed = discord.Embed(title="You do not have any Potions!",description="No potions therefore no healing!",colour=ctx.author.roles[-1].color)
            embed.set_footer(text=version)
            await ctx.send(embed=embed)
            invs.close()
            return
        elif u[potion] < amount:
            embed = discord.Embed(title="You do not have enough Potions!",description="Pick Less, therefore no healing!",colour=ctx.author.roles[-1].color)
            embed.set_footer(text=version)
            await ctx.send(embed=embed)
            invs.close()
            return
        else:
            u[potion] -= amount
        invs.close()
    with open(path.join(cwd, "server\\shop_items.json"),"r") as items:
        data = json.load(items)
        recover = data[potion]["recover"]
        emoji = bot.get_emoji(int(data[potion]["emoji"]))
        items.close()
    with open(path.join(cwd, "server\\user_stats.json"),"r") as stats:
        s = json.load(stats)
        hp = s[str(user.id)]["HP"]
        maxhp = s[str(user.id)]["MAXHP"]
        stats.close()
    #random chance to heal triple
    if random.randint(0,20) == 2:
        hp = int(hp) + int(recover * 3 * amount)
    else:
        hp = int(hp) + int(recover * amount)
    if hp > int(maxhp):
        hp = int(maxhp)
    s[str(user.id)]["HP"] = hp
    with open(path.join(cwd, "server\\user_stats.json"),"w") as stats:
        json.dump(s, stats, indent=2, sort_keys=True)
        stats.close()
    with open(path.join(cwd, "server\\user_inv.json"),"w") as invs:
        json.dump(idata, invs, indent=2, sort_keys=True)
        invs.close()
    embed = discord.Embed(title="You Healed!",description=f"You used {amount} {emoji}.",colour=user.roles[-1].color)
    embed.set_footer(text=version)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="Results:",value=f"You successfully healed {recover * amount} HP. Any extra HP that goes beyond your current max HP will not be put into effect.\nYou used {amount} {emoji}.")
    await ctx.send(embed=embed)

@bot.command(pass_context=True,aliases=['i','inv'])
@commands.guild_only()
async def inventory(ctx, page: int=1):
    user = ctx.author
    s = 10 * (page - 1)
    limit = 10 * page
    with open(path.join("server\\user_inv.json"),"r") as invs:
        allinv = json.load(invs)
        userinv = allinv[str(user.id)]
        invs.close()
    #get all items
    with open(path.join("server\\item_emojis.json"),"r") as emotes:
        data = json.load(emotes)
        emotes.close()
    items = list(userinv.keys())
    message = []
    try:
        for i in range(s, limit):
            try:
                e = bot.get_emoji(data[str(items[i])])
            except:
                e = "[]"
            s = str(e) + "`" + str(items[i]) + "` - `" + str(userinv[str(items[i])]) + "`"
            if int(userinv[str(items[i])]) <= 0:
                userinv.pop(str(items[i]))
                with open(path.join(cwd, "server\\user_inv.json"),"w") as isv:
                    json.dump(allinv, isv, sort_keys=True)
                    isv.close()
                continue
            message.append(s)
    except:
        pass
    message = "\n".join(message)
    member = str(user).split("#")[0]
    embed=discord.Embed(title="User Inventory",description=f"The inventory of {member}",colour=user.roles[-1].color)
    embed.set_footer(text=version)
    embed.add_field(name=f"Page {page}",value=message)
    embed.set_thumbnail(url=user.avatar_url)
    await ctx.send(embed=embed)

@bot.command()
@commands.guild_only()
async def test(ctx):
    emoji = bot.get_emoji(808735716535697408)
    embed=discord.Embed(title='u gay',description="big gae")
    embed.add_field(name='scam',value=f"{emoji}")
    await ctx.send(embed=embed)

@bot.command(pass_context=True,aliases=['u','utilize'])
@commands.guild_only()
async def use(ctx, item):
    pass

@bot.command(pass_context=True,aliases=['wear'])
@commands.guild_only()
async def equip(ctx, item):
    #get item, if not equippable, say it isnt
    #check if already wearing piece, if so, remove and swap, otherwise, just put on
    user = ctx.author
    #get the item type
    #chekc if user has item
    with open(path.join(cwd, "server\\shop_items.json"),"r") as items:
        data = json.load(items)
        if item not in data:
            embed = discord.Embed(title="That item does not exist!",description="Please enter a real item?",colour=user.roles[-1].color)
            embed.set_footer(text=version)
            await ctx.send(embed=embed)
            items.close()
            return
        else:
            if not data[str(item)]["type"] == "equipable":
                embed = discord.Embed(title="This item is not equipable!",description="Please pick an equipable item!",colour=user.roles[-1].color)
                embed.set_footer(text=version)
                await ctx.send(embed=embed)
                items.close()
                return
        items.close()
    with open(path.join(cwd, "server\\user_inv.json"),"r") as inv:
        idata = json.load(inv)
        if item in idata[str(user.id)]:
            del(idata[str(user.id)][str(item)])
        else:
            embed=discord.Embed(title="You Do not Posses this Item!",description="Please buy the item from shop or monster drops!",colour=user.roles[-1].color)
            embed.set_footer(text=version)
            await ctx.send(embed=embed)
            inv.close()
            return
        inv.close()
    if "armor" in data[str(item)]:
        part = data[str(item)]["part"]
    elif "damage" in data[str(item)]:
        part = "weapon"
    with open(path.join(cwd, "server\\user_stats.json"),"r") as stats:
        sdata = json.load(stats)
        if sdata[str(user.id)]["using"][str(part)] != "None":
            embed = discord.Embed(title="This slot is taken!",description="An item is already occupying this spot. Please use the `/unequip` command to unequip it!",colour=user.roles[-1].color)
            embed.set_footer(text=version)
            await ctx.send(embed=embed)
            stats.close()
            return
        old_item = sdata[str(user.id)]["using"][str(part)]
        sdata[str(user.id)]["using"][str(part)] = str(item)
        new_item = str(item)
        if part in ['chest','head','pants','boots']:
            sdata[str(user.id)]["armor"] += data[str(item)]["armor"]
        elif part == "weapon":
            sdata[str(user.id)]["DMG"] += data[str(item)]["damage"]
        toughness = sdata[str(user.id)]["armor"]
        stats.close()
    with open(path.join(cwd, "server\\user_stats.json"),"w") as stats:
        json.dump(sdata, stats, indent=2, sort_keys=True)
        stats.close()
    with open(path.join(cwd, "server\\user_inv.json"),"w") as inv:
        json.dump(idata, inv, indent=2, sort_keys=True)
        inv.close()
    
    if old_item == "None":
        old_item = "no item"
    emoji = bot.get_emoji(807287558450970634)
    embed = discord.Embed(title=f"You swapped your {old_item} for a {new_item}!",description=f"You now have {toughness}{emoji} toughness!",colour=user.roles[-1].color)
    embed.set_footer(text=version)
    await ctx.send(embed=embed)

@bot.command(pass_context=True,aliases=['take_off','uequip'])
@commands.guild_only()
async def unequip(ctx, piece):
    user = ctx.author
    with open(path.join(cwd, "server\\user_stats.json"),"r") as stats:
        sdata = json.load(stats)
        stats.close()
    if str(piece) not in ['head','chest','pants','boots','weapon']:
        embed=discord.Embed(title="That is not a valid piece!",description="The pieces are the head, chestplate, pants, boots, and weapon!",colour=user.roles[-1].color)
        embed.set_footer(text=version)
        await ctx.send(embed=embed)
        return
    if sdata[str(user.id)]["using"][str(piece)] == "None":
        embed=discord.Embed(title=f"Nothing was equipped on your {piece}!",description="Use the `equip` command to equip an item!",colour=user.roles[-1].color)
        embed.set_footer(text=version)
        await ctx.send(embed=embed)
        return
    #change piece data
    item = sdata[str(user.id)]["using"][str(piece)]
    sdata[str(user.id)]["using"][str(piece)] = "None"
    with open(path.join(cwd, "server\\shop_items.json"),"r") as items:
        data = json.load(items)
        if "armor" in data[str(item)]:
            effect = "armor"
        elif "damage" in data[str(item)]:
            effect = "damage"
        amount = data[str(item)][str(effect)]
        items.close()
    if str(effect) == "armor":
        sdata[str(user.id)]["armor"] -= int(amount)
        if int(sdata[str(user.id)]["armor"]) < 0:
            sdata[str(user.id)]["armor"] = 0
    elif str(effect) == "damage":
        sdata[str(user.id)]["DMG"] -= int(amount)
        if int(sdata[str(user.id)]["DMG"]) < 0:
            sdata[str(user.id)]["DMG"] = 0
    with open(path.join(cwd, "server\\user_stats.json"),"w") as stats:
        json.dump(sdata, stats, indent=2, sort_keys=True)
        stats.close()
    with open(path.join(cwd, "server\\user_inv.json"),"r") as inv:
        idata = json.load(inv)
        if str(item) not in idata[str(user.id)]:
            idata[str(user.id)][str(item)] = 1
        else:
            idata[str(user.id)][str(item)] += 1
        inv.close()
    with open(path.join(cwd, "server\\user_inv.json"),"w") as inv:
        json.dump(idata, inv, indent=2, sort_keys=True)
        inv.close()
    embed=discord.Embed(title=f"You unequipped your {piece} piece!",description=f"You unequipped your {item}!",colour=user.roles[-1].color)
    embed.set_footer(text=version)
    await ctx.send(embed=embed)

@bot.command(pass_context=True,aliases=['adv'])
@commands.guild_only()
@commands.cooldown(1, 30, commands.BucketType.user)
async def adventure(ctx):
    user = ctx.author
    ID = user.id
    #get monster type
    with open(path.join(cwd, "server\\user_stats.json"),"r") as stats:
        sdata = json.load(stats)
        if str(ID) not in list(sdata.keys()):
            embed = discord.Embed(title="You do not have an account!",description="Please use the `/account` command to make your account!",colour=discord.Colour.dark_gray())
            embed.set_footer(text=version)
            await ctx.send(embed=embed)
            stats.close()
            return
        sdata[str(ID)]
        rank = sdata[str(ID)]["rank"]
        REDUCE = sdata[str(ID)]["DMG"]
        armor = sdata[str(ID)]["armor"]
        element = sdata[str(ID)]["using"]["weapon"]
        with open(path.join(cwd, "server\\shop_items.json"),"r") as i:
            element = json.load(i)[str(element)]["element"]
            i.close()
        stats.close()
    with open(path.join(cwd, "server\\monsters.json"),"r") as mobs:
        data = json.load(mobs)
        mob = list(data[str(rank)].keys())
        mob = random.choice(mob)
        temp = list(data[str(rank)][str(mob)].keys())
        temp.remove("type")
        drop = random.choice(temp)
        amount = random.choice(droprate)
        m_type = data[str(rank)][str(mob)]["type"]
        mobs.close()
    #user damage and stuff
    r = damage[str(rank)]
    DMG = random.randint(r[0]*7,r[1]*10)
    if PC.isBad(element, m_type):
        REDUCE /= 2
    else:
        DMG *= 2
    DMG = DMG - REDUCE - armor
    if DMG < 0:
        DMG = 0
    sdata[str(ID)]["HP"] -= DMG
    HP = sdata[str(ID)]["HP"]
    if sdata[str(ID)]["HP"] <= 0:
        dead = True
        sdata[str(ID)]["HP"] = 1
        if sdata[str(ID)]["level"] == 1:
            pass
        else:
            sdata[str(ID)]["level"] -= 1
            x = int(sdata[str(ID)]["MAXXP"]) * (1.2**-int(sdata[str(ID)]["level"])) * 100
            sdata[str(ID)]["MAXXP"] = x
    else:
        dead = False
            #reduce health
        #add xp
        rate = RATE.convert(str(rank))
        XP = random.randint(rate * 20, rate * 30)
        MAXXP = sdata[str(ID)]["MAXXP"]
        total_XP = sdata[str(ID)]["XP"] + XP
        if total_XP >= MAXXP:
            sdata[str(ID)]["XP"] = int(total_XP - MAXXP)
            sdata[str(ID)]["MAXXP"] = int(MAXXP * 1.5)
            sdata[str(ID)]["level"] += 1
            sdata[str(ID)]["MAXHP"] *= 1.2
            sdata[str(ID)]["HP"] = int(HP * 1.03)
        else:
            sdata[str(ID)]["XP"] = int(total_XP)
        #money
        earned = random.randint(rate*40, rate*60)
        sdata[str(ID)]["money"] += int(earned)
    
    #write onto json
    with open(path.join(cwd, "server\\user_stats.json"),"w") as stats:
        json.dump(sdata, stats, indent=2, sort_keys=True)
        stats.close()
    name = str(user).split("#")[0]
    embed = discord.Embed(title=f"{name} went Hunting!",description=f"Rank: {rank}",colour=user.roles[-1].color)
    embed.set_footer(text=version)
    embed.set_thumbnail(url=user.avatar_url)
    embed.set_author(name="STATS")
    if dead:
        embed.add_field(name="RESULTS",value=f"`{name}` fought a `{mob}` but died in the process. They managed to be saved by a nearby adventurer.")
    else:
        embed.add_field(name="RESULTS",value=f"`{name}` fought a `{mob}` and managed to get `{amount}` `{drop}`.\nThey took `{DMG}` damage and have `{HP}` health.")
    #add items to inventory
    with open(path.join(cwd, "server\\user_inv.json"),"r") as inv:
        invs = json.load(inv)
        try:
            invs[str(ID)]
        except:
            invs[str(ID)] = {}
        if str(drop) not in list(invs[str(ID)].keys()):
            invs[str(ID)][str(drop)] = int(amount)
        else:
            invs[str(ID)][str(drop)] += int(amount)
        inv.close()
    with open(path.join(cwd, "server\\user_inv.json"),"w") as inv:
        json.dump(invs, inv, indent=2, sort_keys=True)
        inv.close()
    await ctx.send(embed=embed)

@adventure.error
async def adventure_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="Cooldown!",description="You need to wait {:.0f}s to use this command again".format(error.retry_after),colour=discord.Colour.dark_gray())
        embed.set_footer(text=version)
        await ctx.send(embed=embed)

@bot.command(pass_context=True)
@commands.guild_only()
async def promote(ctx):
    with open(path.join(cwd, "server\\user_stats.json"),"r") as stats:
        udata = json.load(stats)
        u_stats = udata[str(ctx.author.id)]
        u_lvl = u_stats["level"]
        u_money = u_stats["money"]
        u_rank = RATE.convert(u_stats["rank"])
        stats.close()
    e = bot.get_emoji(809464420827660300)
    if not u_lvl >= u_rank * 15:
        embed = discord.Embed(title=f"{e}You do not meet the requirements for a promotion{e}",description=f"You need to be at least level {u_rank * 15}")
        embed.set_footer(text=version)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        return
    elif not u_money >= u_rank*500:
        embed = discord.Embed(title=f"{e}You do not meet the requirements for a promotion{e}",description=f"You need {u_rank * 500} money")
        embed.set_footer(text=version)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        return
    u_stats["money"] -= u_rank*500
    u_stats["rank"] = RATE.getRank(u_rank+1)
    with open(path.join(cwd, "server\\user_stats.json"),"w") as stats:
        json.dump(udata, stats, sort_keys=True)
        stats.close()
    embed=discord.Embed(title=f"{e} You have been promoted {e}",description=f"You are now {RATE.getRank(u_rank+1)} rank!",colour=ctx.author.roles[-1].color)
    embed.set_footer(text=version)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@bot.command(pass_context=True,aliases=['yeet'])
@commands.guild_only()
async def sell(ctx, item, amount=1):
    with open(path.join(cwd, "server\\user_inv.json"),"r") as invs:
        allinv = json.load(invs)
        if item not in allinv[str(ctx.author.id)]:
            embed=discord.Embed(title="Item Error!",description="You either do not have that item or do you spelled something wrong!")
            embed.set_footer(text=version)
            await ctx.send(embed=embed)
            invs.close()
            return
        item_amount = allinv[str(ctx.author.id)][str(item)]
        invs.close()
    with open(path.join(cwd, "server\\monsters.json"),"r") as mobs:
        allmobs = json.load(mobs)
        worth = 0
        for rank in allmobs:
            for mob in allmobs[str(rank)]:
                if str(item) in allmobs[str(rank)][str(mob)]:
                    worth = int(allmobs[str(rank)][str(mob)][str(item)])
        if worth == 0:
            embed=discord.Embed(title="This item does not exist or cannot be sold",description="Please sell something else")
            embed.set_footer(text=version)
            await ctx.send(embed=embed)
            return
        mobs.close()
    temp = False
    if item_amount < amount:
        amount = item_amount
        temp = True
    embed=discord.Embed(title="Trading with the Market",description="Here are your terms...",colour=ctx.author.roles[-1].color)
    embed.set_footer(text=version)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    if temp:
        embed.add_field(name="You are missing some items",value=f"Since you are missing items, you will be giving us less D:\nThe new terms are {amount} {item}")
    embed.add_field(name="The TERMS",value=f"You are selling {amount} {item} for {amount * worth} money.")
    embed.add_field(name="Accept the Terms?",value="Type in [y] or [n] to accept or decline the trade")
    await ctx.send(embed=embed)
    def check(m):
        return m.author == ctx.author and m.content in ['y','n']
    answer = await bot.wait_for('message',check=check,timeout=10)
    if answer.content == 'y':
        #do the stuff which adds money and takes away the items
        earned = amount * worth
        allinv[str(ctx.author.id)][str(item)] -= amount
        with open(path.join(cwd, "server\\user_inv.json"),"w") as newinvs:
            json.dump(allinv, newinvs, sort_keys=True)
            newinvs.close()
        with open(path.join(cwd, "server\\user_stats.json"),"r") as stats:
            allstats = json.load(stats)
            allstats[str(ctx.author.id)]["money"] += earned
            stats.close()
        with open(path.join(cwd, "server\\user_stats.json"),"w") as newstats:
            json.dump(allstats, newstats, sort_keys=True)
            newstats.close()
        embed=discord.Embed(title="Trade Successful",description="It was a pleasure doing business with you!",colour=ctx.author.roles[-1].color)
        embed.set_footer(text=version)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name="Trade Info",value=f"You traded {amount} {item} for {earned} money!")
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="Trade has been cancelled",description="No Trade D:",colour=ctx.author.roles[-1].color)
        embed.set_footer(text=version)
        await ctx.send(embed=embed)

bot.run('ODA2NTY3MjI0NTgzOTEzNDg0.YBrUQw.gfbsXp8TAA3bVdpDpiLmP_EEUO8')
