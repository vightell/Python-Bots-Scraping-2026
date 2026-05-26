import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
TOKEN = "280575628960:zx,y[uhkjhsw4tgdsdtfyhgk,gu,ihy.ufaex]"
current_index = 0
tech_index = 0

def get_day_notes(day):
    with open("NOTES.md", "r", encoding="utf-8") as file:
        content = file.read()

    start = content.find(f"## Day {day}")
    end = content.find(f"## Day {day + 1}")

    if start == -1:
        return "Day not found."

    if end == -1:
        return content[start:]

    return content[start:end]

def get_day_code(day):

    filename = f"code/day{day}.py"

    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()

    except FileNotFoundError:
        return "⚠️ Code file not found."

def get_news():
    global current_index
    
    response = requests.get("https://news.ycombinator.com/")
    soup = BeautifulSoup(response.content, "html.parser")
    titles = soup.select(".titleline > a")
    news = []

    start = current_index
    end = current_index + 5
    current_index += 5

    for item in titles:
        news.append({
            "title": item.get_text(),
            "link": item["href"]
        })
    return news[start:end]        

def get_tech_signals():

    global tech_index

    response = requests.get("https://github.com/trending")

    soup = BeautifulSoup(response.content, "html.parser")

    repos = soup.find_all("article", class_="Box-row")

    signals = []

    start = tech_index
    end = tech_index + 5

    tech_index += 5

    for repo in repos[start:end]:

        title = repo.find("h2").get_text(strip=True)

        link = repo.find("a")["href"]

        full_link = f"https://github.com{link}"

        signals.append({
            "title": title,
            "link": full_link
        })

    return signals

async def techsignals(update: Update, context: ContextTypes.DEFAULT_TYPE):

    signals = get_tech_signals()

    message = "[TECH SIGNALS DETECTED]\n\n"

    for index, signal in enumerate(signals, start=tech_index - len(signals) + 1):

        message += (
            f"Signal {index}:\n"
            f"{signal['title']}\n\n"
            f"Link:\n{signal['link']}\n\n"
        )

    await update.message.reply_text(message)

async def hi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Hi {update.effective_user.first_name}"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    await update.message.reply_text(
    """ ⚔️ Chaos Archive Initialized.

Two paths detected:

🧠 /journey
Explore the evolution logs.

🌐 /abyss
Scan the digital abyss."""
    )

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Recently, blah blah blah..."
    )

async def journey(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        """⚔️ Journey Archive

Available Commands:

🧠 /journey_notes 5
💻 /journey_code 5
⚔️ /journey_both 5

Choose a day number to retrieve your archive.
"""
    )

async def journey_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "Usage: /journey_notes 3"
        )
        return

    day = int(context.args[0])

    notes = get_day_notes(day)

    await update.message.reply_text(notes[:4000])

async def journey_code(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "Usage: /journey_code 5"
        )
        return

    day = int(context.args[0])

    code = get_day_code(day)

    await update.message.reply_text(code[:4000])

async def journey_both(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "Usage: /journey_both 5"
        )
        return

    day = int(context.args[0])

    notes = get_day_notes(day)
    code = get_day_code(day)

    message = (
        f"⚔️ DAY {day} ARCHIVE\n\n"
        f"🧠 NOTES:\n\n{notes}\n\n"
        f"💻 CODE:\n\n{code}"
    )

    await update.message.reply_text(message[:4000])

async def abyss(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
"""  🌐 DIGITAL ABYSS

  Available Scans:

  📰 /hackernews
  Tech surveillance signals.

  📡 /techsignals
  Python, AI, GitHub, tech movement.

  🌀 /chaosfeed
  Weird internet artifacts detected.

  🎲 /randomdiscovery
  Unknown signal from the abyss."""
    )

async def chaos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Shall we summon the Internet Chaos Or Scan the Digital Abyss?"
    )

async def hackernews(update: Update, context: ContextTypes.DEFAULT_TYPE):
    articles = get_news()
    message = "[ABYSS SCAN COMPLETE]\n\n"
    for article in articles:
        message +=(
        f"• {article['title']}\n"
        f"  Link: {article['link']}\n\n"
        )
    if articles:
        await update.message.reply_text(message)
    else:
        await update.message.reply_text("The Digital Abyss is silent... No news found.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("journey_notes", journey_notes))
app.add_handler(CommandHandler("hi", hi))
app.add_handler(CommandHandler("news", news))
app.add_handler(CommandHandler("chaos", chaos))
app.add_handler(CommandHandler("hackernews", hackernews))
app.add_handler(CommandHandler("techsignals", techsignals))
app.add_handler(CommandHandler("journey_code", journey_code))
app.add_handler(CommandHandler("journey_both", journey_both))
app.add_handler(CommandHandler("journey", journey))
app.add_handler(CommandHandler("abyss", abyss))
print("Chaos Scraper is sprinting...")
app.run_polling()