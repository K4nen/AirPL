import requests
import pandas as pd

def fetch_and_process_no2_data():
    # Récupérer les données
    url = "https://data.airpl.org/api/v1/mesure/mensuelle/"
    params = {
        "code_configuration_de_mesure__code_point_de_prelevement__code_polluant": "03",
        "date_heure_tu__range": "2021-1-1,2023-12-31",
        "code_configuration_de_mesure__code_point_de_prelevement__code_station__code_commune__code_departement__in": "44,49,53,72,85",
        "export": "json"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        dfNO2 = pd.DataFrame(data['results'])  # Adapter selon la structure des données JSON

        # Sauvegarder le DataFrame pour utilisation ultérieure
        dfNO2.to_pickle('NO2.pkl')
    else:
        print(f"Erreur {response.status_code}: {response.text}")
        return None

    # Charger le DataFrame depuis le fichier sauvegardé
    dfNO2 = pd.read_pickle('NO2.pkl')

    # Afficher les types de chaque colonne
    print(dfNO2.dtypes)

    # Assurez-vous que dfNO2 est bien chargé et nettoyé
    # Supprimer les lignes comportant des valeurs "NaN" dans les colonnes "valeur" et "valeur_originale"
    dfNO2.dropna(subset=['valeur', 'valeur_originale'], inplace=True)

    # Supprimer les lignes comportant des valeurs négatives dans les colonnes "valeur" et "valeur_originale"
    dfNO2 = dfNO2[(dfNO2['valeur'] >= 0) & (dfNO2['valeur_originale'] >= 0)]

    # Afficher les premières lignes du DataFrame pour vérifier le nettoyage
    print(dfNO2.head())

    # Vérifier si les colonnes existent dans le DataFrame
    colonnes_a_convertir = ['code_commune', 'departement_code', 'code_polluant']

    # Convertir les colonnes en int64
    for col in colonnes_a_convertir:
        if col in dfNO2.columns:
            dfNO2[col] = dfNO2[col].astype('int64')

    # Afficher les types de colonnes pour vérifier les conversions
    print(dfNO2.dtypes)

    return dfNO2
