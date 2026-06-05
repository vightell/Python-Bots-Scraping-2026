import requests
import random
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

load_dotenv()

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise Exception("TOKEN variable is not found")
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
   if day in [22, 23, 24, 25]:
        filename = "code/day22-25.py"

   elif day in [26, 27]:
        filename = "code/day26-27.py"

   elif day in [28, 29, 30]:
        filename = "code/day28-30.py"

   else:
    filename = f"code/day{day}.py"

   try: 
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()

   except FileNotFoundError:
        return None

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

def get_chaos_feed():
    response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
    data = response.json()
    fact= data["text"]
    return fact

chaos_openers = [
    "The abyss",
    "Reality",
    "The intarnet",
    "A rogue signal",
    "The digital void",
    "An unknouwn process",
    "The archive",
    "A forgotten server",
    "The machine",
    "A corruptid timeline",
    ".........-Glitch-"
]

chaos_actions = [
    "has detectead",
    "has revealed",
    "has transmitted",
    "has discovered",
    "has unearthed",
    "has produced",
    "has expoosed",
    "has intercepted",
    "has recounstructed",
    "has awakened",
    "Has WHAT?"
]

chaos_endings = [
    "an impossible fact.",
    "a cursed artifact.",
    "another anomaly.",
    "an unstable signal.",
    "a forbidden observation.",
    "something that should not exist.",
    "a historical glitch.",
    "a statistical nightmare.",
    "a digital hallucination.",
    "an undocumented phenomenon.",
    "........."
]

async def chaosfeed(update: Update, context: ContextTypes.DEFAULT_TYPE):

    fact = get_chaos_feed()
    title = (
        f"{random.choice(chaos_openers)}"
        f" {random.choice(chaos_actions)} "
        f"{random.choice(chaos_endings)}"
    )
    message = (
        "[CHAOS FEED]\n\n"
        f"{title}\n\n"
        f"{fact}"
    )

    await update.message.reply_text(message)

def get_random_discovery():
    headers = { "User-Agent": "Mozilla/5.0" }
    response = requests.get(
        "https://en.wikipedia.org/wiki/Special:Random",
        headers = headers
        )
    final_url = response.url
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.find("h1", id="firstHeading").get_text()
    return {
        "title": title,
        "url": final_url
    }

async def randomdiscovery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    article = get_random_discovery()
    message = (
        "[DISCOVERY TERMINAL]\n\n"
        f"Today's Discovery since before:\n\n"
        f"Title: {article['title']}\n"
        f"Link: {article['url']}"
    )
    await update.message.reply_text(message)


async def hi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Hi {update.effective_user.first_name}"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    await update.message.reply_text(
    """⚔️ Chaos Archive Initialized.

Two paths detected:

🧠 /journey
Explore the evolution logs.

🌐 /abyss
Scan the digital abyss.

────────────────────

📁 JOURNEY ARCHIVE RANGE:
Days 1 → 35
All entries are stored as indexed memory segments.
"""
    )

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Recently, blah blah blah..."
    )

user_state = {}

async def journey(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    user_state[user_id] = {"step": "choose_mode"}

    await update.message.reply_text(
        "⚔️ JOURNEY ARCHIVE\n\n"
        "Select retrieval mode (Archive Range: 1–35)\n\n"
        "1. Notes\n"
        "2. Code\n"
        "3. Both\n\n"
        "Reply with a number baby ;) ."
    )

async def journey_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "Usage: /journey_notes 3"
        )
        return

    day = int(context.args[0])

    notes = get_day_notes(day)

    for i in range(0, len(notes), 3500):
        await update.message.reply_text(notes[i:i + 3500])

async def journey_code(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "Usage: /journey_code 5"
        )
        return

    day = int(context.args[0])
    
    if day in [22, 23, 24, 25]:
     await update.message.reply_text(
        "📁 ARCHIVE NOTE :: STRUCTURE LAYER\n\n"
        "These entries are bound to a single core implementation unit.\n"
        "The system treats Days 22–25 as one structural block in memory mapping."
    )
    elif day in [26, 27]:
     await update.message.reply_text(
        "📁 ARCHIVE NOTE :: RUNTIME CONVERGENCE\n\n"
        "Multiple execution paths detected.\n"
        "Days 26–27 converge into a shared runtime process and are executed from one active code source."
    )
    elif day in [28, 29, 30]:
     await update.message.reply_text(
        "📁 ARCHIVE NOTE :: FINAL COMPRESSION\n\n"
        "Archive stabilization complete.\n"
        "Days 28–30 were compressed into a single finalized implementation unit for consistency and preservation."
    )

    code = get_day_code(day)

    if code is None:

        await update.message.reply_text(
            f"⚔️ DAY {day} CODE ARCHIVE\n\n"
            "[ARCHIVE GAP DETECTED]\n\n"
            "The learning notes survived,\n"
            "but no code archive exists for this day."
        )

        return

    for i in range(0, len(code), 3500):

        chunk = code[i:i + 3500]
            
        await update.message.reply_text(chunk)

async def journey_both(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "Usage: /journey_both 5"
        )
        return

    day = int(context.args[0])

    notes = get_day_notes(day)
    code = get_day_code(day)

    if code is None:

        await update.message.reply_text(
            "💻 CODE:\n\n"
            "⚔️ No code archive exists for this day.\n\n"
            "The journey notes exist, but the code was not preserved."
        )

        return
    else:
        code_text = code

        message = (
        f"⚔️ DAY {day} ARCHIVE\n\n"
        f"🧠 NOTES:\n\n{notes[:1000]}\n\n"
        f"💻 CODE:\n\n{code_text}"
        )
    for i in range(0, len(message), 3500):

        chunk = message[i:i + 3500]

        await update.message.reply_text(chunk)               


async def journey_router(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    text = update.message.text.strip()

    if user_id not in user_state:
        return

    state = user_state[user_id]

    if state["step"] == "choose_mode":

        if text == "1":
            state["mode"] = "notes"
        elif text == "2":
            state["mode"] = "code"
        elif text == "3":
            state["mode"] = "both"
        else:
            await update.message.reply_text("Enter 1, 2 or 3.")
            return

        state["step"] = "choose_day"

        await update.message.reply_text("tell me the day number?")
        return

    if state["step"] == "choose_day":

        if not text.isdigit():
            await update.message.reply_text("Type a valid day number.")
            return

        day = int(text)
        mode = state["mode"]

        notes = get_day_notes(day)
        code = get_day_code(day)

        # cleanup state
        del user_state[user_id]

        if mode == "notes":
            for i in range(0, len(notes), 3500):
                await update.message.reply_text(notes[i:i+3500])

        elif mode == "code":
            if code is None:
                await update.message.reply_text("No code archive found.")
                return

            for i in range(0, len(code), 3500):
                await update.message.reply_text(code[i:i+3500])

        elif mode == "both":
            if code is None:
                await update.message.reply_text("No code archive found.")
                return

            message = (
                f"⚔️ DAY {day} ARCHIVE\n\n"
                f"🧠 NOTES:\n\n{notes[:1000]}\n\n"
                f"💻 CODE:\n\n{code}"
            )

            for i in range(0, len(message), 3500):
                await update.message.reply_text(message[i:i+3500])

async def abyss(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
"""  🌐 DIGITAL ABYSS

  Available Scans:

  📰 /hackernews
  Tech surveillance signals.

  📡 /techsignals
  Live pulse of GitHub's developer ecosystem.

  🌀 /chaosfeed
  Weird internet artifacts detected.

  🎲 /randomdiscovery
  A random fragment from Wikipedia's abyss."""
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
app.add_handler(CommandHandler("chaosfeed", chaosfeed))
app.add_handler(CommandHandler("journey_code", journey_code))
app.add_handler(CommandHandler("journey_both", journey_both))
app.add_handler(CommandHandler("journey", journey))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, journey_router))
app.add_handler(CommandHandler("abyss", abyss))
app.add_handler(CommandHandler("randomdiscovery", randomdiscovery))
print("Chaos Scraper is sprinting...")
app.run_polling()