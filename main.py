import os
import unicodedata
from dotenv import load_dotenv

import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.service import DEFAULT_EXECUTABLE_PATH

from keep_alive import keep_alive


#.envファイルをロードして環境変数へ反映
load_dotenv()
TOKEN = os.getenv( 'DISCORD_BOT_TOKEN' )

# Intentsを指定
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=None, intents=intents)

# Seleniumの設定
CHROME_DRIVER_PATH = DEFAULT_EXECUTABLE_PATH  # Chromeドライバのパス
chrome_service = ChromeService(executable_path=CHROME_DRIVER_PATH)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--window-size=1440,780')
chrome_options.add_argument('--headless')  # ヘッドレスモードでの実行
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content
    print(f"メッセージ内容: {content}")  # メッセージの内容をプリントする
    if ';' not in content:
        print( "not ;" )
        return

    print( "start" )
    # URLと要素の指定
    url = f'https://www.vcrdb.net/builder?c={content}'  # スクリーンショットを取得したいURLを指定してください
    element_selector = 'builderImage'  # スクリーンショットを取得したい要素のセレクタを指定してください

    # Seleniumを使ってURLにアクセスし、スクリーンショットを取得
    driver.get(url)
    element = driver.find_element( By.ID, element_selector )
    screenshot_path = 'screenshot.png'  # スクリーンショットの保存先を指定してください
    element.screenshot(screenshot_path)

    # Discordのチャットにスクリーンショットを送信
    with open(screenshot_path, 'rb') as f:
        screenshot = discord.File(f)
        await message.channel.send(file=screenshot)

    print( "finish" )

keep_alive()
bot.run(TOKEN)
