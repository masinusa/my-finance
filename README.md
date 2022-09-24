Features:
- List transactions
- Tally total net worth
- compare best prices for something


steps to run quickstart from scratch:
- clone the repo
- copy cookbook.secrets.template.py and fill in plaid secrets. You can get your access tokens by running the get-started from the plaid-quickstart git repo.
- make start-db
- make update



TO-DO reminders:
- Generalize Dockerfile (i.e. CMD /bin/bash and have compose with tty with a passed command in the Makefile)
- Only update certain things when a file was modified
- Check what happens if more than 26 columns and ASCII diverges from excel column names (since column names are in alphabetical order)
- Next big step is having the transactions go to the right mongodb collection

