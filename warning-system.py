import discord, json, asyncio
from discord.ext import commands

client = commands.Bot(command_prefix = ".")

with open("logs.json", "r") as f:
    open_file = json.load(f)



@client.command()
@commands.has_permissions(administrator = True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def warn(ctx, member: discord.Member = None, *, reason = None):
    if member is None:
        delete = await ctx.send("**Please mention a member to be warned**")
        await asyncio.sleep(3)
        await delete.delete()
        return

    
    await not_in_logs(member)


    #Dump
    if reason is None:
        open_file[str(member.id)]["reason"].append("**no reason**")
    else:
        open_file[str(member.id)]["reason"].append(reason)


    open_file[str(member.id)]["user_case"] += 1
    with open("logs.json", "w") as f:
        json.dump(open_file, f, indent = 1)
    
    warned = discord.Embed(
        description = f"{member.mention} **has been warned.**",
        color = discord.Color.green()
    )
    warned.add_field(name = "Number of warnings", value = open_file[str(member.id)]["user_case"], inline = False)
    if reason is None:
        warned.add_field(name = "Reason", value = "**no reason**", inline = False)
    else:
        warned.add_field(name = "Reason", value = reason, inline = False)
       
    await ctx.send(embed = warned)

@client.command()
@commands.has_permissions(administrator = True)
async def warnings(ctx, member: discord.Member):
    
    if str(member.id) not in open_file:
        warning_embed = discord.Embed(
            description = "this member does not have any warnings",
            color = discord.Color.dark_blue()
        )
        warning_embed.set_footer(text = f"ID: {member.id}")
        warning_embed.set_author(name = str(member), icon_url = str(member.avatar_url))
        await ctx.send(embed = warning_embed)
        return

    warning_embed2 = discord.Embed(
        description = f"Warnings for {member.mention}",
        color = discord.Color.dark_blue()
    )
    warning_embed2.set_author(name = str(member), icon_url = str(member.avatar_url))
    warning_embed2.set_footer(text = f"ID: {member.id}")
    count = 0
    for cases in open_file[str(member.id)]["reason"]:
        count += 1
        warning_embed2.add_field(name = f"Warning #{count}", value = cases, inline = False)
    await ctx.send(embed = warning_embed2)
    

@warnings.error
async def error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        delete = await ctx.send("You need to mention someone.")
        await asyncio.sleep(4)
        await delete.delete()
    else:
        print(error)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.author.send(f"{ctx.author.mention}, you are missing permissions.")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.author.send(f"{ctx.author.mention}, please wait **5 seconds* before using the command again")
    else:
        print(error)



async def not_in_logs(user):
    if str(user.id) not in open_file:
        open_file[str(user.id)] = {"reason": [], "user_case": 0}
        if "nothing" in open_file:
            del open_file["nothing"]

client.run("Bot Token")