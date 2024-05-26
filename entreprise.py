import requests
import pandas as pd
from unidecode import unidecode


def fetch_data():
    url3 = "https://data.paysdelaloire.fr/api/explore/v2.1/catalog/datasets/120027016_base-sirene-v3-ss/exports/json?"

    where = (
        "etatadministratifetablissement = 'Actif' AND ("
        "libellecommuneetablissement = 'DONGES' OR "
        "libellecommuneetablissement = 'FROSSAY' OR "
        "libellecommuneetablissement = 'SAINT-ETIENNE-DE-MONTLUC' OR "
        "libellecommuneetablissement = 'CHOLET' OR "
        "libellecommuneetablissement = 'NANTES' OR "
        "libellecommuneetablissement = 'SAINT-NAZAIRE' OR "
        "libellecommuneetablissement = 'ANGERS' OR "
        "libellecommuneetablissement = 'LAVAL' OR "
        "libellecommuneetablissement = 'LA TARDIERE' OR "
        "libellecommuneetablissement = 'LA ROCHE-SUR-YON' OR "
        "libellecommuneetablissement = 'LE MANS' OR "
        "libellecommuneetablissement = 'REZE' OR "
        "libellecommuneetablissement = 'BOUGUENAIS' OR "
        "libellecommuneetablissement = 'MONTOIR-DE-BRETAGNE')"
    )

    select = 'siret, categorieentreprise, sectionetablissement, libellecommuneetablissement ,geolocetablissement, etatadministratifetablissement'
    limit = 300000

    dfEtp = pd.DataFrame()

    while True:
        # Paramètres de la requête
        params = {
            'select': select,
            'where': where,
            'limit': limit
        }

        response = requests.get(url3, params=params)
        if response.status_code != 200:
            print(f"Erreur: {response.status_code}")
            print(response.text)

        data = response.json()
        if isinstance(data, list):
            df_results = pd.json_normalize(data)
            dfEtp = pd.concat([dfEtp, df_results], ignore_index=True)

        if len(data) < limit:
            break  # Arrêter la boucle si tous les enregistrements ont été récupérés



# Suppression des colonnes 'geolocetablissement', 'geo_shape', et 'geo_point_2d' de dfEtp
    dfEtp = dfEtp.drop(columns=['geolocetablissement'], errors='ignore')

    # Convertir les valeurs de la colonne 'nom_commune' en minuscules et supprimer les accents
    dfEtp['libellecommuneetablissement'] = dfEtp['libellecommuneetablissement'].apply(lambda x: unidecode(x).lower())


    return dfEtp

if __name__ == "__main__":
    df = fetch_data()
    print(df.shape)
    print(df.head())
