-- table schema to store the ingredients and its measurement details per drink
CREATE TABLE IF NOT EXISTS cocktails_ingredients(
    drink_id INTEGER,
    ingredient_name TEXT,
    ingredient_measure TEXT 
);
