# Cocktail Drinks
This project downloads all the drinks from the api: `https://www.thecocktaildb.com/api.php`
and stores it in a sqlite database with its ingredients details.

## Create and activate a virtual environment (recommended but optional)
For windows:
1. Set up a virtual environment
`python -m venv venv`
2. Activate the virtual environment
`venv\Scripts\activate`

## How to run this python solution
1. When running for the first time, please install the required packages in the requirements.txt file using pip
```
pip install -r requirements.txt
```

2. Run the python script
```
python coacktail_drinks.py
```

## Tables structure for the cocktail_drinks problem statement
### 1. cocktails_details
This table contains the details of the drinks like its unique id, name, category, instructions(German) and any other relevany details.
Primary key: drink_id

### 2. cocktails_ingredients
This table contains the ingredients and its measument used in the drinks for each drink in the cocktails_details table.
Foreign key: drink_id

## How you use the sqlite database
1. Download any DB browser App for SQLite
2. Open the database file `cocktail_drinks.db` in the above app
3. Query any run your sql. For sample queries, please use the one from `./sql/sql_queries_questions.sql`
