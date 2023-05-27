Excuse the Messiness.  This is a personal finance app in the making.


Features Idea list:
- List transactions
- Tally total net worth
- compare best prices for something
- Receipt OCR, NLP, and Information Extraction: https://medium.com/one9-tech/information-extraction-receipt-ocr-scan-deep-learning-1e68ce5a9ae7


steps to run quickstart from scratch:
- clone the repo
- copy cookbook.secrets.template.py and fill in plaid secrets. You can get your access tokens by running the get-started from the plaid-quickstart git repo.
- make start-db
- make update (updates the database)
- make analyze (analyzes the current month's transactions)
- make write (write's current month's transactions to an excel sheet)


TO-DO reminders:
- Generalize Dockerfile (i.e. CMD /bin/bash and have compose with tty with a passed command in the Makefile)
- Only update certain things when a file was modified
- Check what happens if more than 26 columns and ASCII diverges from excel column names (since column names are in alphabetical order)
- Next big step is having the transactions go to the right mongodb collection
- Improve documentation

Notes:
- the explore target simply runs the src/explore script for easily executing code in the container... should maybe just attach to the container to start with or something

DB Schema:

DB - Collection - Document
PlaidDB
  - user_tokens
    - link_token
    - plaid_client_id
    - plaid_secret
  - bank_tokens
    - chase
    - alliant
    - discover
TransactionsDB
  - april_2023
    - ...
