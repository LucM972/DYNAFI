import streamlit as st
import pandas as pd
import plotly.express as px

# Lecture des fichiers Excel (ils doivent être dans le même dossier que app.py sur GitHub)
df1 = pd.read_excel("LAMENTIN_1.xlsx", sheet_name=0, header=None)
df2 = pd.read_excel("LAMENTIN_2.xlsx", sheet_name=0, header=None)

# Nettoyage du fichier des ratios (df2)
df2 = df2.dropna(how='all')
df2 = df2[df2[1].str.match(r'^R\d+', na=False)]

# Attribution des colonnes (ajusté pour 2020 à 2023 + 1 colonne commentaire)
df2.columns = ["Code", "Libellé", "2019", "2020", "2021", "2022", "2023", "Commentaire"]

# Conversion des années en numérique
for year in ["2020", "2021", "2022", "2023"]:
    df2[year] = pd.to_numeric(df2[year], errors="coerce")

# Filtrage des ratios clés
ratios_clefs = {
    "R1": "Recettes réelles de fonctionnement",
    "R2": "Dépenses réelles de fonctionnement",
    "R8": "Épargne de gestion",
    "R9E": "Trésorerie"
}
df_ratios = df2[df2["Libellé"].isin(ratios_clefs.keys())].copy()
df_ratios["Libellé complet"] = df_ratios["Libellé"].map(ratios_clefs)
df_ratios = df_ratios[["Libellé complet", "2020", "2021", "2022", "2023"]]

# Titre
st.set_page_config(page_title="Analyse financière - Lamentin", layout="wide")
st.title("Analyse Financière Automatisée")
st.subheader("Commune : Lamentin (Martinique)")

# Tableau
st.markdown("### Ratios clés (2020 à 2023)")
st.dataframe(df_ratios.style.format(thousands=" "))

# Graphique
st.markdown("### Évolution des ratios")
df_melt = df_ratios.melt(id_vars="Libellé complet", var_name="Année", value_name="Montant")
fig = px.line(df_melt, x="Année", y="Montant", color="Libellé complet", markers=True)
st.plotly_chart(fig, use_container_width=True)

# Analyse textuelle IA (statique pour la démo)
st.markdown("### Analyse automatique")
st.markdown("""
La commune du Lamentin montre une évolution positive de ses recettes de fonctionnement sur la période 2020-2023, 
avec une stabilité de l’épargne de gestion et une trésorerie globalement maîtrisée. 
Les dépenses suivent une courbe plus douce, traduisant un bon contrôle budgétaire.
""")
