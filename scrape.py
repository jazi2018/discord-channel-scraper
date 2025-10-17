import requests
import time
from tqdm import tqdm

def scrape_channel(channel:str, message_limit: int = 100, channel_label:str = None, token:str = None) -> None:
    """
    Scrapes all messages from a discord channel provided its id.

    Params:
        channel (str): The desired channel's ID
        message_limit (int): The number of messages retrieved at a time. 100 is the suggested and default value
        channel_label (str): Optional parameter which only affects the name of the output file
        token (str): Discord bot token. Notably, the bot should have access to read previous messages. If no token is passed,
            the function will attempt to find 'DISCORD_TOKEN' in a .env file
    
    Returns:
        void: Outputs all data to a csv file
    
    Raises:
        ValueError: If TOKEN is not present in local .env file
    """
    #get token from environment if not passed
    if not token:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        token = os.getenv("DISCORD_TOKEN")
        if not token:
            raise ValueError("Missing DISCORD_TOKEN in .env")
    
    headers = {
        "Authorization" : f"Bot {token}",
        "Content-Type" : "application/json",
        "User-Agent" : "DiscordChannelScraper (https://github.com/jazi2018/discord-channel-scraper.git, 1.0)"
    }

    pbar = tqdm(desc="scraping", unit="batch")
    #paginate through all messages until messages is None
    all_messages = []
    last_id = None
    while True:
        #construct url
        url = f"https://discord.com/api/v9/channels/{channel}/messages?limit={message_limit}"
        if last_id:
            url += f"&before={last_id}"

        #make api call and verify success
        r = requests.get(url, headers=headers)
        if r.status_code == 429: #rate limit
            limit = r.json()
            print(f"Warning: {limit["message"]} Sleeping for {limit["retry_after"]}")
            time.sleep(limit["retry_after"] + 0.5)
            continue
        elif r.status_code != 200:
            print(f"Request error {r.status_code}: {r.text}")
            break

        messages = r.json()
        if not messages: #we finished!
            break

        #get id of last message
        if len(messages) > 1:
            last_id = messages[-1]['id']

        #add messages to cumulative message list
        all_messages.extend(messages)

        pbar.update(1)
        time.sleep(0.3) #to prevent rate limiting



    with open(f"{channel_label + "-" if channel_label is not None else ""}messages.csv", "w", encoding="utf-8") as f:
        f.write("content|author_id|mention_everyone\n")
        for m in tqdm(all_messages):
            #make sure m does not have embeds or attachments
            #niche case, also check if message type is not 0 (this would be server boosts, polls, etc.)
                #basically everything that isn't a message
            if m["embeds"] or m["attachments"] or m["type"] != 0:
                continue
            #make sure not sent by bot (this is a separate block because if not a bot, the key doesn't appear at all)
            elif m['author'].get("bot"):
                continue
            #otherwise, write message content and author to csv (delineated by |)
            f.write(f"{m["content"]}|{m["author"]["id"]}|{m["mention_everyone"]}\n")

if __name__ == "__main__":
    scrape_channel("1159064215735246921", 100, "doncord-general")