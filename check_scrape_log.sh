#!/bin/bash

echo " Cron lancé à $(date)" >> /home/ubuntu/debug_cron.log

CSV="/home/ubuntu/data/bitcoin_prices.csv"

if [ ! -f "$CSV" ]; then
    echo " Fichier bitcoin_prices.csv introuvable."
    exit 1
fi

# Dernière ligne du fichier
LAST_LINE=$(tail -n 1 "$CSV")

# Extraire date et heure
LAST_DATE=$(echo "$LAST_LINE" | cut -d',' -f1)
LAST_TIME=$(echo "$LAST_LINE" | cut -d',' -f2)

# Format datetime complet
LAST_DATETIME="$LAST_DATE $LAST_TIME"

# Convertir en timestamp UNIX
LAST_TS=$(date -d "$LAST_DATETIME" +%s)
NOW_TS=$(date +%s)

# Différence en secondes
DIFF_SEC=$((NOW_TS - LAST_TS))

if [ "$DIFF_SEC" -le 300 ]; then
    echo " Dernière mise à jour il y a $DIFF_SEC secondes : OK"
else
    # Lancer scrape.sh
    bash "$SCRAPER"
    echo " Alerte : dernière mise à jour il y a $DIFF_SEC secondes "
fi
