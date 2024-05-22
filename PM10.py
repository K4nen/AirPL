import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def fetch_and_process_pm10_data():
    # URL et paramètres de la requête
    url = "https://data.airpl.org/api/v1/mesure/mensuelle/"
    params = {
        "code_configuration_de_mesure__code_point_de_prelevement__code_polluant": 24,
        "date_heure_tu__range": "2021-1-1,2023-12-31",
        "code_configuration_de_mesure__code_point_de_prelevement__code_station__code_commune__code_departement__in": "44,49,53,72,85",
        "export": "json"
    }

    # Récupérer les données
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        dfPM10 = pd.DataFrame(data['results'])  # Adapter selon la structure des données JSON

        # Sauvegarder le DataFrame pour utilisation ultérieure
        dfPM10.to_pickle('PM10.pkl')
    else:
        print(f"Erreur {response.status_code}: {response.text}")
        return None

    # Afficher les premières lignes du DataFrame
    print(dfPM10.head())

    # Charger le DataFrame depuis le fichier sauvegardé
    dfPM10 = pd.read_pickle('PM10.pkl')

    # Afficher les types de chaque colonne
    print(dfPM10.dtypes)

    # Supprimer les lignes comportant des valeurs "NaN" dans les colonnes "valeur" et "valeur_originale"
    dfPM10.dropna(subset=['valeur', 'valeur_originale'], inplace=True)

    # Supprimer les lignes comportant des valeurs négatives dans les colonnes "valeur" et "valeur_originale"
    dfPM10 = dfPM10[(dfPM10['valeur'] >= 0) & (dfPM10['valeur_originale'] >= 0)]

    # Vérifier si les colonnes existent dans le DataFrame
    colonnes_a_convertir = ['code_commune', 'departement_code', 'code_polluant']

    # Convertir les colonnes en int64
    for col in colonnes_a_convertir:
        if col in dfPM10.columns:
            dfPM10[col] = dfPM10[col].astype('int64')

    # Afficher les types de colonnes pour vérifier les conversions
    print(dfPM10.dtypes)

    return dfPM10
