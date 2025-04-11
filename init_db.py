import io
import pandas as pd
import duckdb

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)


# réponse (écrite en tte lettre = string) que l'utilisateur doit donner pour que ça fonctionne :
ANSWER_STR = """
SELECT * FROM beverages
CROSS JOIN food_items
"""


# ------------------------------------------------------------
# EXERCISES LIST
# ------------------------------------------------------------
data = {
    "theme": ["cross_joins", "windows_functions"],
    "exercise_name": ["beverages_and_food", "simple_window"],
    "tables": [["beverages", "food_items"], "simple_window"],
    "last_reviewed": ["1970-01-01", "1970-01-01"]
}
memory_state_df = pd.DataFrame(data)
con.execute("CREATE TABLE IF NOT EXISTS memory_state AS SELECT * FROM memory_state_df")

# ------------------------------------------------------------
# CROSS JOIN EXERCISES
# ------------------------------------------------------------

# 1er df "beverages"
csv = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""

beverages = pd.read_csv(io.StringIO(csv))
con.execute("CREATE TABLE IF NOT EXISTS beverages AS SELECT * FROM beverages")


# 2eme df "food_items"
csv2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""

food_items = pd.read_csv(io.StringIO(csv2))
con.execute("CREATE TABLE IF NOT EXISTS food_items AS SELECT * FROM food_items")