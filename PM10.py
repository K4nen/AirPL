import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from unidecode import unidecode


def fetch_and_process_pm10_data():
    # URL de base
    url = "https://data.airpl.org/api/v1/mesure/horaire/"

    # Paramètres de base de la requête
    base_params = {
        "code_configuration_de_mesure__code_point_de_prelevement__code_polluant": 24,
        "date_heure_tu__range": "2024-1-1,2024-3-31 23:00:00",
        "export": "json"
    }
    # Limite de résultats par requête
    limit = 1000
    offset = 0

    # DataFrame pour stocker tous les résultats
    dfPM10 = pd.DataFrame()

    while True:
        # Mettre à jour les paramètres avec la limite et l'offset
        params = base_params.copy()
        params.update({
            "limit": limit,
            "offset": offset
        })

        # Récupérer les données
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            df_results = pd.DataFrame(data['results'])  # Adapter selon la structure des données JSON

            # Ajouter les résultats au DataFrame principal
            dfPM10 = pd.concat([dfPM10, df_results], ignore_index=True)

            # Vérifier si le nombre de résultats récupérés est inférieur à la limite
            if len(df_results) < limit:
                break  # Arrêter la boucle si tous les enregistrements ont été récupérés

            # Mettre à jour l'offset pour la prochaine itération
            offset += limit
        else:
            print(f"Erreur {response.status_code}: {response.text}")
            break

    print(f"Total records retrieved: {len(dfPM10)}")

    # Sauvegarder le DataFrame pour utilisation ultérieure
    dfPM10.to_pickle('PM10.pkl')

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

    # Convertir les valeurs de la colonne 'nom_commune' en minuscules et supprimer les accents
    dfPM10['nom_commune'] = dfPM10['nom_commune'].apply(lambda x: unidecode(x).lower())

    # Convertir les colonnes en int64
    for col in colonnes_a_convertir:
        if col in dfPM10.columns:
            dfPM10[col] = dfPM10[col].astype('int64')

    # Afficher les types de colonnes pour vérifier les conversions
    print(dfPM10.dtypes)

    return dfPM10


