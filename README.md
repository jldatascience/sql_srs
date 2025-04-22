🧠 SQL Training App avec SRS (Spaced Repetition System)

Sujet & objectif :
J’ai créé une application déployée sur Streamlit Cloud permettant à un utilisateur de s'entraîner à des exercices SQL en utilisant le principe du SRS (Spaced Repetition System), afin de favoriser la mémorisation à long terme.


SRS – Révision espacée intelligente :
Après chaque exercice, l’utilisateur peut choisir de revoir l’exercice dans :
      ⏳ 2 jours (rappel rapide)
      📆 7 jours (consolidation)
      🧠 21 jours (mémorisation longue durée)

Cela met à jour dynamiquement la table memory_state pour adapter l'ordre d'apparition des exercices.


👉 Application en ligne : https://sql--srs.streamlit.app/

👉 Repo GitHub : https://github.com/jldatascience/sql_srs


🚀 Fonctionnalités principales :
      Interface web interactive avec Streamlit
      Moteur SQL embarqué avec DuckDB
      Vérification automatique des requêtes : colonnes, valeurs, structure
      Système de répétition espacée (SRS) : 2, 7 ou 21 jours
      Visualisation des résultats et corrections en temps réel
      Accès aux tables et réponses des exercices à tout moment


🗂️ Structure du projet :
      sql_srs/
      │
      ├── app.py               # Application principale Streamlit
      ├── init_db.py           # Script d'initialisation de la base DuckDB
      ├── data/                # Contient la base exercises_sql_tables.duckdb
      ├── answers/             # Fichiers SQL avec les réponses attendues
      ├── requirements.txt     # Dépendances Python
      └── README.md            # Ce fichier


▶️ Lancer l’application en local :
      git clone https://github.com/jldatascience/sql_srs.git
      cd sql_srs
      pip install -r requirements.txt
      streamlit run app.py


🛠️ Technologies utilisées :
      Python 3.10+
      Streamlit
      DuckDB
      Pandas
