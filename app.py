# pylint: disable=missing-module-docstring

import io
import os

import duckdb
import pandas as pd
import streamlit as st
from datetime import date, timedelta


# Création du dossier data si nécessaire
if "data" not in os.listdir():
    logging.error(os.listdir())
    logging.error("creating folder data")
    os.mkdir("data")

# Initialisation de la database si nécessaire
if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read()) # dans ce cas, desactiver pylint car ne fonctionne pas avec exec !
    # subprocess.run(["python", "init_db.py"])  MAIS subprocess ne fonctionne pas bien sur streamlit !

# Connexion à DuckDB
con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)


# fonctions
def check_users_solution(user_query: str) -> None:
    """
    Checks that user SQL query is correct by:
    1: checking the columns
    2: checking the values
    :param user_query: a string containing the query inserted by the user
    """
    result = con.execute(user_query).df() # result = c le r+ apres avoir fait la query que l'utilisateur a entré dans la zone de texte
    st.dataframe(result)

    #     # test pour compter le nbr de colonnes :
    #    #    if len(result.columns) != len(        # len(result.columns) = longueur de result.columns
    #     #        solution_df.columns                  # on la compare à la longueur de len(solution_df.columns)
    #    #    ) : # replace with try result = result[solution_df.columns]
    #    #        st.write("Some columns are missing") # on previent l'utilisateur si result.columns & solution_df.columns n'ont pas la meme longueur


    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
        if result.compare(solution_df).shape == (0, 0):
            st.write("Correct !")
            st.balloons()
    except KeyError as e:
        st.write("Some columns are missing")
    # test pour compter le nbr de lignes :
    n_lines_difference = result.shape[0] - solution_df.shape[0] # on créé une variable n_lines_difference pr voir si ya un ecart sur le nbr de ligne entre la df result et la df solution_df
    if n_lines_difference != 0:
        st.write(
            f"result has a {n_lines_difference} lines difference with the solution_df"
        )


# --- INTERFACE ---
with st.sidebar:
    # Liste des thèmes disponibles
    available_themes_df = con.execute("SELECT DISTINCT theme FROM memory_state").df()

    # Interface de sélection du thème
    theme = st.selectbox(
        "What would you like to review?",
        available_themes_df["theme"].unique(),
        index=None,
        placeholder="Select a theme...",
    )

    # Préparation de la requête SQL en fonction du thème
    if theme:
        st.write(f"You selected {theme}")
        select_exercises_query = f"SELECT * FROM memory_state WHERE theme = '{theme}'"
    else:
        select_exercises_query = f"SELECT * FROM memory_state"

    # Récupération de l'exercice correspondant
    exercise = (
        con.execute(select_exercises_query)
        .df()
        .sort_values("last_reviewed")
        .reset_index(drop=True)
    )
    st.write(exercise)

    # Lecture du nom de l'exercice et chargement de la requête SQL attendue
    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql", "r") as f:
        answer = f.read()

    # Exécution de la requête SQL attendue pour obtenir la solution
    # voici la df de résultat
    # la solution_df c la df de résultat qd on prend la query "ANSWER_STR" et kon la met dans duckdb.sql
    # solution_df = con.execute(answer).df() exécute la requête contenue dans answer (qui provient du fichier .sql) via DuckDB, puis récupère le résultat sous forme de DataFrame dans solution_df
    solution_df = con.execute(answer).df()


# on met à dispo de l'utilisateur, un text area pour que l'utilisateur puisse entrer sa requete SQL :
st.header("enter your code")
query = st.text_area(label="votre code SQL ici", key="user_input") # cette query sert à montrer la df de résultat
# ci dessus, on verifie donc si l’utilisateur a rentré uen query ds le text_area


# et si ya une query rentré par l’utilisateur, on fait toutes les manip ci-dessous pr comparer le r+ de la query de
# l’utilisateur avec la solution kil fallait trouver :
if query:
    check_users_solution(query)

# button
for n_days in [2, 7, 21]:
    if st.button(f"Revoir dans {n_days} jours"):
        next_review = date.today() + timedelta(days=n_days)
        con.execute(
            f"UPDATE memory_state SET last_reviewed = '{next_review}' WHERE exercise_name = '{exercise_name}'"
        )
        st.rerun()

if st.button("Reset"):
    con.execute(f"UPDATE memory_state SET last_reviewed = '1970-01-01'")
    st.rerun()


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


con.close()