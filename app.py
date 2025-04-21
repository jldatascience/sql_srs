# pylint: disable=missing-module-docstring

import io

import duckdb
import pandas as pd
import streamlit as st



con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

with st.sidebar:
    theme = st.selectbox(
        "What would you like to review?",
        ("cross_joins", "GroupBy", "windows_functions"),
        index=None,
        placeholder="Select a theme...",
    )
    st.write("You selected:", theme)

    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'").df().sort_values(
        "last_reviewed").reset_index()
    st.write(exercise)

    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql", "r") as f:
        answer = f.read()

    # voici la df de résultat
    # la solution_df c la df de résultat qd on prend la query "ANSWER_STR" et kon la met dans duckdb.sql
    # solution_df = con.execute(answer).df() exécute la requête contenue dans answer (qui provient du fichier .sql) via DuckDB, puis récupère le résultat sous forme de DataFrame dans solution_df
    solution_df = con.execute(answer).df()

# on met à dispo de l'utilisateur, un text area pour que l'utilisateur puisse entrer sa requete SQL :
st.header("enter your code")
query = st.text_area(label="votre code SQL ici", key="user_input")  # cette query sert à montrer la df de résultat
if query:
    result = con.execute(
        query).df()  # result = c le r+ apres avoir fait la query que l'utilisateur a entré dans la zone de tyexte
    st.dataframe(result)
    #
    #     # test pour compter le nbr de colonnes :
    #    #    if len(result.columns) != len(        # len(result.columns) = longueur de result.columns
    #     #        solution_df.columns                  # on la compare à la longueur de len(solution_df.columns)
    #    #    ) : # replace with try result = result[solution_df.columns]
    #    #        st.write("Some columns are missing") # on previent l'utilisateur si result.columns & solution_df.columns n'ont pas la meme longueur

    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
    except KeyError as e:
        st.write("Some columns are missing")

    # test pour compter le nbr de lignes :
    n_lines_difference = result.shape[0] - solution_df.shape[
        0]  # on créé une variable n_lines_difference pr voir si ya un ecart sur le nbr de ligne entre la df result et la df solution_df
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
    exercise_tables = exercise.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"table: {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)

# et dans une autre table à part (cela permet de cacher le fait d'avoir des tables à part),
# il uy aura la réponse (s'il ne trouve pas il peut cliquer sur la table pour voir la réponse)
with tab3:
    st.write(answer)