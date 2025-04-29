# QuoteChain ReplyBot

**QuoteChain ReplyBot** is a Python script that automatically replies to the latest tweet by [@QuoteChain_AI](https://twitter.com/QuoteChain_AI) at regular 10-minute intervals using a random message from a local `replies.txt` file.

---

## 🚀 Features

- Automatically replies to new tweets from `@QuoteChain_AI`.
- Selects a random witty response from a customizable `replies.txt` file.
- Syncs with 10-minute block intervals for timely replies.
- Gracefully handles Twitter API rate limits.

---

## 🛠️ Requirements

- Python 3.7 or higher
- A Twitter Developer Account with elevated access
- A Twitter App with the following credentials:
  - API Key
  - API Secret
  - Access Token
  - Access Token Secret
  - Bearer Token

---

## 📦 Installation

1. Clone this repository:

```bash
git clone https://github.com/TheWarley1/QuoteChain-Reply-Bot.git cd QuoteChain-Reply-Bot
```


2. Install dependencies:

```bash
pip install -r requirements.txt
```


3. Create a `.env` file in the root folder and add your Twitter API credentials:

```bash
touch .env
```
```bash
API_KEY=your_api_key
API_SECRET=your_api_secret
ACCESS_TOKEN=your_access_token
ACCESS_SECRET=your_access_token_secret
BEARER_TOKEN=your_bearer_token
```

4. Create a `replies.txt` file with your reply messages (one per line):


---

## 🧪 How to Run

Run the bot with:

```bash
python reply-bot.py
```
Or whatever you saved your script as.


You'll see output like:

```
🚀 Twitter QuoteBot is running...
📅 Synchronized to check shortly after every 10-minute interval
📝 Found latest tweet ID: 1234567890123456789 (won't reply to this one)
⏳ Waiting until 14:10:15 to check for new tweets (123.4 seconds)
```


If rate limited, the bot will pause and automatically retry after the cooldown.

---

## ⏰ How It Works

- On startup, the bot fetches and logs the latest tweet ID (but skips replying).
- Every 10 minutes, it checks for a new tweet.
- If a new tweet is found, it replies using a random message from `replies.txt`.
- If Twitter API rate limits are hit, the bot waits until the reset time and continues.

---

## 🔐 Notes

- Make sure your Twitter Developer account has **write** permissions.
- Avoid over-automating to prevent being flagged by Twitter's systems.

---

## 📄 License

MIT License

---

Made with ❤️ by [@TheWarley1](https://github.com/TheWarley1)

