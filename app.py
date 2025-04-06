import pandas as pd
import duckdb
import streamlit as st
import io


# 1er df "beverages"
csv = '''
beverage,price
orange juice,2.5
Expresso,2
Tea,3
'''

beverages = pd.read_csv(io.StringIO(csv))


# 2eme df "food_items"
csv2 = '''
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
'''

food_items = pd.read_csv(io.StringIO(csv2))


# réponse (écrite en tte lettre = string) que l'utilisateur doit donner pour que ça fonctionne :
answer = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

# voici la df de résultat
# la solution c la df de résultat qd on prend la query "answer" et kon la met dans duckdb.sql
solution = duckdb.sql(answer).df()

# on met à dispo de l'utilisateur, un text area pour que l'utilisateur puisse entrer sa requete SQL :
st.header("enter your code")
query = st.text_area(label="votre code SQL ici", key="user_input") # cette query sert à montrer la df de résultat
if query:
    result = duckdb.sql(query).df()
    st.dataframe(result)


tab2, tab3 = st.tabs(["Tables", "Solution"])



# ces tables presentent les tables qu'a l'utilisateur à sa disposition, et on lui montre
# aussi la solution cad la df qui est attendu en sortie

# dans la tab2, on montre à l'utilisateur, le résultat attendu (solution) et les tables ki sont
# à sa disposotion (beverages & food_items)
with tab2:
    st.write("table: beverages")
    st.dataframe(beverages)
    st.write("table: food_items")
    st.dataframe(food_items)
    st.write("expected:")
    st.dataframe(solution)

# et dans une autre table à part (cela permet de cacher le fait d'avoir des tables à part),
# il uy aura la réponse (s'il ne trouve pas il peut cliquer sur la table pour voir la réponse)
with tab3:
    st.write(answer)

