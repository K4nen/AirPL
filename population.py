import requests
import pandas as pd
from unidecode import unidecode

def fetch_and_process_population_data(base_url, limit=100):
    offset = 0
    dfPopulation = pd.DataFrame()

    while True:
        url = f"{base_url}?limit={limit}&offset={offset}"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Erreur lors de l'appel de l'API: {response.status_code}")
            break

        data = response.json()
        results = data.get('results', [])

        if results:
            df_results = pd.json_normalize(results)
            dfPopulation = pd.concat([dfPopulation, df_results], ignore_index=True)

        if len(results) < limit:
            break

        offset += limit

    print(f"Total records retrieved: {len(dfPopulation)}")

    dfPopulation = dfPopulation.drop(columns=['geo_shape', 'geo_point_2d'], errors='ignore')

    # Convertir les valeurs de la colonne 'nom_commune' en minuscules et supprimer les accents
    dfPopulation['nom_de_la_commune'] = dfPopulation['nom_de_la_commune'].apply(lambda x: unidecode(x).lower())

    colonnes_a_convertir = ['code_departement', 'code_arrondissement', 'code_canton', 'code_commune']
    for col in colonnes_a_convertir:
        if col in dfPopulation.columns:
            dfPopulation[col] = dfPopulation[col].astype('int64')

    print(dfPopulation.head())
    print(dfPopulation.dtypes)

    return dfPopulation

# Utilisation de la fonction
base_url = "https://data.paysdelaloire.fr/api/explore/v2.1/catalog/datasets/12002701600563_population_pays_de_la_loire_2019_communes_epci/records"
dfPopulation = fetch_and_process_population_data(base_url)
