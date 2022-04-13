import discord
from discord.ext import commands, tasks
import requests
import os
from dotenv import load_dotenv
from solana_functions import create_account, fund_account, get_balance, send_sol

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Define intents (required to DM users)
intents = discord.Intents.default()
intents.members = True

# Create client object
client = commands.Bot(command_prefix = '!', intents=intents)

# Events
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# Commands
@client.command('create')
async def create(ctx):
    sender_username = ctx.message.author
    if not os.path.exists('accounts/' + str(sender_username) + '.txt'):
        try:
            public_key = create_account(sender_username)
            if public_key is not None:
                message = "Solana Account created successfully. "
                message += "Your account public key is {}".format(public_key)
                await ctx.send(message)
            else:
                message = "Failed to create account.n"
                await ctx.send(message)
        except Exception as e:
            print('error:',e)
            await ctx.send('Failed to create account')
            return
    else:
        await ctx.send("You already have an account!")

@client.command('fund')
async def fund(ctx):
    sender_username = ctx.message.author
    incoming_msg = ctx.message.content
    try:
        amount = float(incoming_msg.split(" ")[1])
        if amount <= 2 :
            message = "Requesting {} SOL to your Solana account, please wait !!!".format(amount)
            await ctx.send(message)
            transaction_id = fund_account(sender_username, amount)
            if transaction_id is not None:
                message = "You have successfully requested {} SOL for your Solana account.".format(
                    amount)
                message += "The transaction id is {}".format(transaction_id)
                await ctx.send(message)
            else:
                message = "Failed to fund your Solana account."
                await ctx.send(message)
        else:
            message = "The maximum amount allowed is 2 SOL."
            await ctx.send(message)
    except Exception as e:
        print('error:',e)
        await ctx.send('Failed to fund account.')
        return

@client.command('balance')
async def balance(ctx):
    sender_username = ctx.message.author
    try:
        data = get_balance(sender_username)
        if data is not None:
            public_key = data['publicKey']
            balance = data['balance']
            message = "Your Solana account {} balance is {} SOL".format(
                public_key, balance)
            await ctx.send(message)
        else:
            message = "Failed to retrieve balance"
            await ctx.send(message)
    except Exception as e:
        print('error:',e)
        await ctx.send('Failed to check account balance')
        return

@client.command('send')
async def send(ctx):
    sender_username = ctx.message.author
    incoming_msg = ctx.message.content
    try:
        split_msg = incoming_msg.split(" ")
        amount = float(split_msg[1])
        receiver = split_msg[2]
        message = "Sending {} SOL to {}, please wait !!!".format(
            amount, receiver)
        await ctx.send(message)
        transaction_id = send_sol(sender_username, amount, receiver)
        if transaction_id is not None:
            message = "You have successfully sent {} SOL to {} n".format(
                amount, receiver)
            message += "The transaction id is {}".format(transaction_id)
            await ctx.send(message)
        else:
            message = "Failed to send SOL"
            await ctx.send(message)
    except Exception as e:
        print('error:',e)
        await ctx.send('Failed to send SOL')
        return


client.run(BOT_TOKEN)
