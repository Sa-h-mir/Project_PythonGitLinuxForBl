#!/bin/bash

# Je sépare la date et l'heure pour mettre chacun dans deux cases distinctes du csv
date=$(date '+%Y-%m-%d')
time=$(date '+%H:%M:%S')

# Je récupère le lien html où se trouve l'indice boursier du bitcoin
html=$(curl -s "https://coinmarketcap.com/currencies/bitcoin/")

# J'extrait de manière brut la valeur de ce dernier
raw_price=$(echo "$html" | grep -Eo '\$[0-9,]+\.[0-9]+' | head -n 1)

# Je nettoie la valeur pour enlever le $ et la virgule
price=$(echo "$raw_price" | tr -d '$,')

# Je fais un affichage pour debug
echo "Prix extrait : $price"

# Je sauvegarde les données dans le CSV (data/bitcoin_prices.csv)
echo "$date,$time,$price" >> ./data/bitcoin_prices.csv

