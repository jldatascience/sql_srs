# pylint: disable=missing-module-docstring

import io

import duckdb
import pandas as pd
import streamlit as st

# 1er df "beverages"
CSV = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""

beverages = pd.read_csv(io.StringIO(CSV))


# 2eme df "food_items"
CSV2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""

food_items = pd.read_csv(io.StringIO(CSV2))


# réponse (écrite en tte lettre = string) que l'utilisateur doit donner pour que ça fonctionne :
ANSWER_STR = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

# voici la df de résultat
# la solution_df c la df de résultat qd on prend la query "ANSWER_STR" et kon la met dans duckdb.sql
solution_df = duckdb.sql(ANSWER_STR).df()


with st.sidebar:
    option = st.selectbox(
        "What would you like to review?",
        ("Joins", "GroupBy", "Windows Functions"),
        index=None,
        placeholder="Select a theme...",
    )
    st.write("You selected:", option)


# on met à dispo de l'utilisateur, un text area pour que l'utilisateur puisse entrer sa requete SQL :
st.header("enter your code")
query = st.text_area(
    label="votre code SQL ici", key="user_input"
)  # cette query sert à montrer la df de résultat
if query:
    result = duckdb.sql(
        query
    ).df()  # result = c le r+ apres avoir fait la query que l'utilisateur a entré dans la zone de tyexte
    st.dataframe(result)

    # test pour compter le nbr de colonnes :
    #    if len(result.columns) != len(        # len(result.columns) = longueur de result.columns
    #        solution_df.columns                  # on la compare à la longueur de len(solution_df.columns)
    #    ) : # replace with try result = result[solution_df.columns]
    #        st.write("Some columns are missing") # on previent l'utilisateur si result.columns & solution_df.columns n'ont pas la meme longueur

    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
    except KeyError as e:
        st.write("Some columns are missing")

    # test pour compter le nbr de lignes :
    n_lines_difference = (
        result.shape[0] - solution_df.shape[0]
    )  # on créé une variable n_lines_difference pr voir si ya un ecart sur le nbr de ligne entre la df result et la df solution_df
    if n_lines_difference != 0:
        st.write(
            f"result has a {n_lines_difference} lines difference with the solution_df"
        )


tab2, tab3 = st.tabs(["Tables", "Solution"])


# ces tables presentent les tables qu'a l'utilisateur à sa disposition, et on lui montre
# aussi la solution_df cad la df qui est attendu en sortie

# dans la tab2, on montre à l'utilisateur, le résultat attendu (solution_df) et les tables ki sont
# à sa disposotion (beverages & food_items)
with tab2:
    st.write("table: beverages")
    st.dataframe(beverages)
    st.write("table: food_items")
    st.dataframe(food_items)
    st.write("expected:")
    st.dataframe(solution_df)

# et dans une autre table à part (cela permet de cacher le fait d'avoir des tables à part),
# il uy aura la réponse (s'il ne trouve pas il peut cliquer sur la table pour voir la réponse)
with tab3:
    st.write(ANSWER_STR)
