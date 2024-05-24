import requests
import pandas as pd

base_url = "https://data.paysdelaloire.fr/api/explore/v2.1/catalog/datasets/120027016_base-sirene-v3-ss/records"
limit = 100  # Nombre de résultats par page
offset = 0  # Décalage initial
df_entreprise = pd.DataFrame()  # DataFrame pour stocker tous les enregistrements

while True:
    # Construire l'URL avec le paramètre de décalage
    url = f"{base_url}?limit={limit}&offset={offset}"
    print(f"Appel de l'API avec l'URL: {url}")

    # Appeler l'API
    response = requests.get(url)

    # Vérifier si la requête a réussi
    if response.status_code != 200:
        print(f"Erreur lors de l'appel de l'API: {response.status_code}")
        break

    data = response.json()

    # Obtenir les résultats
    results = data.get('results', [])
    if results:
        # Normaliser les résultats JSON en DataFrame
        df_results = pd.json_normalize(results)

        # Sélectionner les colonnes nécessaires
        try:
            df_results = df_results[['siret', 'categorieentreprise', 'sectionetablissement', 'geolocetablissement.lon',
                                     'geolocetablissement.lat', 'etatadministratifetablissement']]
            df_results = df_results[df_results['etatadministratifetablissement'] == 'Actif']

            # Renommer les colonnes pour une meilleure lisibilité
            df_results.columns = ['siret', 'categorieentreprise', 'sectionetablissement', 'longitude', 'latitude',
                                  'etatadministratifetablissement']

            df_entreprise = pd.concat([df_entreprise, df_results], ignore_index=True)
        except KeyError as e:
            print(f"KeyError: {e}")
            print("Colonnes disponibles:", df_results.columns)

    # Vérifier si le nombre d'enregistrements récupérés est inférieur à la limite
    if len(results) < limit:
        print(f"Nombre d'enregistrements récupérés : {len(results)} à l'offset {offset}")
        print("Fin de la pagination.")
        break  # Arrêter la boucle si tous les enregistrements ont été récupérés

    # Mettre à jour le décalage pour l'itération suivante
    offset += limit

print(f"Total des enregistrements récupérés: {len(df_entreprise)}")
print(df_entreprise.head())  # Afficher les premières lignes du DataFrame
