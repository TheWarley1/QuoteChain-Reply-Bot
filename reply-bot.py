import time
import tweepy
import random
import json
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import requests  # For catching generic timeout exceptions

load_dotenv()

# === Twitter API Credentials ===
client = tweepy.Client(
    bearer_token=os.getenv("BEARER_TOKEN"),
    consumer_key=os.getenv("API_KEY"),
    consumer_secret=os.getenv("API_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_SECRET"),
    wait_on_rate_limit=True  # Let tweepy handle rate limiting automatically
)

# === QuoteChain Twitter Info ===
quote_ai_username = "QuoteChain_AI"
STATE_FILE = "bot_state.json"

def load_state():
    """Load the bot's state from file"""
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        return {"last_replied_tweet": None, "last_check_time": None}
    except Exception as e:
        print(f"❌ Error loading state: {e}")
        return {"last_replied_tweet": None, "last_check_time": None}

def save_state(state):
    """Save the bot's state to file"""
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(state, f)
    except Exception as e:
        print(f"❌ Error saving state: {e}")

def get_latest_quote_ai_tweet():
    try:
        user = client.get_user(username=quote_ai_username)
        if user is None or user.data is None:
            print(f"⚠️ Could not find user: {quote_ai_username}")
            return None
        
        user_id = user.data.id
        tweets = client.get_users_tweets(id=user_id, max_results=5)
        if tweets is None or tweets.data is None or len(tweets.data) == 0:
            print("⚠️ No tweets found for user.")
            return None
        
        return tweets.data[0].id
    except tweepy.TooManyRequests as e:
        print(f"⚠️ Rate limited! Tweepy will handle the waiting.")
        return None
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
        print(f"⚠️ Connection error: {e}. Will retry later.")
        time.sleep(60)  # Wait a bit before retrying
        return None
    except Exception as e:
        print(f"❌ Error fetching latest tweet: {type(e).__name__} - {str(e)}")
        return None

def get_random_reply():
    try:
        with open("replies.txt", "r", encoding="utf-8") as f:
            replies = [line.strip() for line in f if line.strip()]
            if not replies:
                raise ValueError("Replies file is empty!")
            return random.choice(replies)
    except Exception as e:
        print(f"❌ Error reading replies file: {e}")
        return "🔥 Another banger from the QuoteChain oracle."

def reply_to_tweet(tweet_id, message):
    try:
        response = client.create_tweet(in_reply_to_tweet_id=tweet_id, text=message)
        print(f"✅ Replied to Tweet ID {tweet_id}: {message}")
        return response
    except Exception as e:
        print(f"❌ Failed to reply: {e}")
        return None

def calculate_next_tweet_time():
    """Calculate the next 10-minute interval."""
    now = datetime.now()
    minutes = (now.minute // 10 + 1) * 10
    next_time = now.replace(minute=0, second=15, microsecond=0) + timedelta(minutes=minutes)
    if next_time < now:
        next_time += timedelta(minutes=10)
    return next_time

def main():
    print("🚀 Twitter QuoteBot is running...")
    print("📅 Synchronized to check shortly after every 10-minute interval")
    
    # Load previous state
    state = load_state()
    last_replied_tweet = state["last_replied_tweet"]
    
    if last_replied_tweet:
        print(f"📝 Loaded previous tweet ID: {last_replied_tweet}")
    else:
        # Initial fetch - don't reply yet
        try:
            last_replied_tweet = get_latest_quote_ai_tweet()
            if last_replied_tweet:
                print(f"📝 Found latest tweet ID: {last_replied_tweet} (won't reply to this one)")
                # Update state
                state["last_replied_tweet"] = last_replied_tweet
                save_state(state)
        except Exception as e:
            print(f"💥 Error during initial tweet check: {e}")

    consecutive_errors = 0
    max_consecutive_errors = 5
    
    while True:
        try:
            next_tweet_time = calculate_next_tweet_time()
            now = datetime.now()

            if next_tweet_time > now:
                wait_seconds = (next_tweet_time - now).total_seconds()
                print(f"⏳ Waiting until {next_tweet_time.strftime('%H:%M:%S')} to check for new tweets ({wait_seconds:.1f} seconds)")
                time.sleep(wait_seconds)

            # Optional: wait a little bit more so the tweet is surely posted
            time.sleep(30)

            latest_tweet_id = get_latest_quote_ai_tweet()
            if latest_tweet_id and latest_tweet_id != last_replied_tweet:
                reply_text = get_random_reply()
                reply_result = reply_to_tweet(latest_tweet_id, reply_text)
                
                if reply_result:
                    last_replied_tweet = latest_tweet_id
                    # Update state after successful reply
                    state["last_replied_tweet"] = last_replied_tweet
                    state["last_check_time"] = datetime.now().isoformat()
                    save_state(state)
                    consecutive_errors = 0  # Reset error counter after success
            else:
                print("⏳ No new tweet or already replied to the latest one.")
            
        except Exception as e:
            print(f"💥 Error in main loop: {e}")
            consecutive_errors += 1
            
            # If too many errors in a row, take a longer break
            if consecutive_errors >= max_consecutive_errors:
                cooldown = 15 * 60  # 15 minutes
                print(f"⚠️ Too many consecutive errors. Taking a {cooldown/60} minute break...")
                time.sleep(cooldown)
                consecutive_errors = 0
            else:
                time.sleep(60)

if __name__ == "__main__":
    main()