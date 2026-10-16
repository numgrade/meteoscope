# Données d'exemple

`stations.csv` : observations horaires (fictives, inspirées des formats de
données publiques Météo-France) de trois stations, le 1er janvier 2024.

| Colonne | Unité | Description |
|---|---|---|
| station | — | identifiant de la station |
| date | ISO 8601 | horodatage de la mesure |
| temperature_c | °C | température sous abri |
| humidite_pct | % | humidité relative |
| pression_hpa | hPa | pression au niveau de la station |
| vent_ms | m/s | vitesse du vent moyenne |
| pluie_mm | mm | précipitations de l'heure |

Pièges volontairement inclus : cellules vides, code d'erreur `-999.9`,
doublons exacts, valeur aberrante (capteur défaillant).