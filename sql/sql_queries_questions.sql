-- Sql Queries few question for the cocktail_drinks database

-- 1. Which alcoholic drinks can be mixed with lemon and whiskey?
SELECT DISTINCT det.drink_name
FROM cocktails_details det
INNER JOIN cocktails_ingredients ing1 ON det.drink_id = ing1.drink_id
INNER JOIN cocktails_ingredients ing2 ON det.drink_id = ing2.drink_id 
WHERE det.is_alcoholic IS True
    AND LOWER(ing1.ingredient_name) = "lemon" 
    AND LOWER(ing2.ingredient_name) = "whiskey";

-- 2. Which drink(s) can be mixed with just 15 g of Sambuca?
-- Assumption: The column ingredient_measure contains exact value and unit for measurement for lookup,
-- if not, then have to calculate the conversion from one unit to another
SELECT DISTINCT det.drink_name
FROM cocktails_details det
INNER JOIN cocktails_ingredients ing
ON det.drink_id = ing.drink_id
WHERE LOWER(ingredient_name) = "sambuca" AND ingredient_measure = "15 g";

-- 3. Which drink has the most ingredients? 
SELECT det.drink_name, COUNT(ing.ingredient_name) AS ingredient_count
FROM cocktails_details det
INNER JOIN cocktails_ingredients ing
ON det.drink_id = ing.drink_id
GROUP BY det.drink_name
ORDER BY ingredient_count DESC
LIMIT 1;
