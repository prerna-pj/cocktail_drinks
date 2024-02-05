-- schema to store the drink details
CREATE TABLE IF NOT EXISTS cocktails_details (
    drink_id INTEGER,
    drink_name TEXT,
    drink_alternate_name TEXT,
    drink_tags TEXT,
    drink_category TEXT,
    drink_iba TEXT,
    is_alcoholic TEXT,
    drink_glass TEXT,
    instructions_de TEXT
);
