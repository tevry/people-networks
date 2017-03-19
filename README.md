# people-networks
## Short description of the scripts:
1. "create_profile_reading_tracker.py" - creates a csv file to keep track of which articles were already parsed
2. "parse_one_article.py" - extracts the links from monthly revisions of a given article
3. "prr1000.py" - loops over next 1000 articles and calls 'parse_one_article.py' script
4. "loop_parsing.sh" - because of memory leak problem we had to use bash code to call "prr1000.py" 70 times (we have ~70k articles).

Everythin was running on Digital Ocean 20$ instances for ~5 days.
