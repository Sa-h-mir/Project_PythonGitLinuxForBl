#!/bin/bash

# Je mets la date du jour
today=$(date '+%Y-%m-%d')

# Je crée les différents chemins des fichiers
input_file="./data/bitcoin_prices.csv"
output_file="./data/daily_report.csv"

# J'ajoute en-tête si le fichier existe pas
if [ ! -f "$output_file" ]; then
    echo "Date,Open,Close,High,Low" > "$output_file"
fi

# J'extrais les lignes du prix du bitcoin de la journée
lines=$(grep "^$today" "$input_file")

# Je récupère uniquement la colonne "prix"
prices=$(echo "$lines" | cut -d',' -f3)

# Je détermine les différents indicateurs
open=$(echo "$lines" | head -n 1 | cut -d',' -f3)
close=$(echo "$lines" | tail -n 1 | cut -d',' -f3)
high=$(echo "$prices" | sort -nr | head -n 1)
low=$(echo "$prices" | sort -n | head -n 1)

# J'écris ces indicateurs dans le fichier rapport
echo "$today,$open,$close,$high,$low" >> "$output_file"

# Je fais un affichage pour vérifier la cohérence de ce dernier
echo "Rapport $today  Open: $open | Close: $close | High: $high | Low: $low"
