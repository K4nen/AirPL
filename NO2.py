import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def fetch_and_process_no2_data():
    # URL de base
    url = "https://data.airpl.org/api/v1/mesure/horaire/"

    # Paramètres de base de la requête
    base_params = {
        "code_configuration_de_mesure__code_point_de_prelevement__code_polluant": "03",
        "date_heure_tu__range": "2024-1-1,2024-3-31 23:00:00",
        "code_configuration_de_mesure__code_point_de_prelevement__code_station__code_commune__code_departement__in": "44,49,53,72,85",
        "export": "json"
    }
    # Limite de résultats par requête
    limit = 1000
    offset = 0

    # DataFrame pour stocker tous les résultats
    dfNO2 = pd.DataFrame()

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
            dfNO2 = pd.concat([dfNO2, df_results], ignore_index=True)

            # Vérifier si le nombre de résultats récupérés est inférieur à la limite
            if len(df_results) < limit:
                break  # Arrêter la boucle si tous les enregistrements ont été récupérés

            # Mettre à jour l'offset pour la prochaine itération
            offset += limit
        else:
            print(f"Erreur {response.status_code}: {response.text}")
            break

    print(f"Total records retrieved: {len(dfNO2)}")

    # Sauvegarder le DataFrame pour utilisation ultérieure
    dfNO2.to_pickle('PM10.pkl')

    # Afficher les premières lignes du DataFrame
    print(dfNO2.head())

    # Charger le DataFrame depuis le fichier sauvegardé
    dfNO2 = pd.read_pickle('PM10.pkl')

    # Afficher les types de chaque colonne
    print(dfNO2.dtypes)

    # Supprimer les lignes comportant des valeurs "NaN" dans les colonnes "valeur" et "valeur_originale"
    dfNO2.dropna(subset=['valeur', 'valeur_originale'], inplace=True)

    # Supprimer les lignes comportant des valeurs négatives dans les colonnes "valeur" et "valeur_originale"
    dfNO2 = dfNO2[(dfNO2['valeur'] >= 0) & (dfNO2['valeur_originale'] >= 0)]

    # Vérifier si les colonnes existent dans le DataFrame
    colonnes_a_convertir = ['code_commune', 'departement_code', 'code_polluant']

    # Convertir les colonnes en int64
    for col in colonnes_a_convertir:
        if col in dfNO2.columns:
            dfNO2[col] = dfNO2[col].astype('int64')

    # Afficher les types de colonnes pour vérifier les conversions
    print(dfNO2.dtypes)

    return dfNO2


