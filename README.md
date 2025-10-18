# Discord Channel Scraper
Very simple and lightweight script that scrapes the entirety of a discord channel, given the API key has access to read the message history of said channel.

To setup, simply clone / download the repo. Within a virtual environment, run the following:

```
pip install -r requirements.txt
```

Then, you can either import the function from the script, or replace the values in the function call at the bottom of the script.
It will output the results into a .csv file, deliniated by "|".

### Some flaws
- Currently, the script reads the entire channel history into memory. If you are attempting to scrape a channel with a very large history, this may have some problems
  - An easy solution to this is to write the contents of the response into a file before continuing the loop (I may implement this later)
- The only content, author_id, and mention_everyone is written to the file. If you want other features, you will need to change the loop at the bottom
  - I may add kwargs in the future so that any desired value can be passed without manually changing the code
- If for some reason the code fails (perhaps due to an unexpected response error), all scraping progress is lost
  - Again, only really a problem if you are scraping a large file. I may solve this in the future by handling unexpected responses and logging the last ID so the script can pick up where it left off
