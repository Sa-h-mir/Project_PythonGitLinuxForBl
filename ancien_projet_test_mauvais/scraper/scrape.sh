# Je récupère la date actuelle au format YYYY-MM-DD
now=$(date '+%Y-%m-%d %H:%M:%S')

# Je récupère la page HTML via un API car je ne peux pas récupérer directement les données via un scrap classique
html=$(curl -s "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")

# DEBUG : Affiche le JSON brut pour test
echo "Réponse API : $html"

# J'extrait le prix en euros via regex Bash
price=$(echo "$html" | grep -oP '"usd":\K[0-9.]+' )

# DEBUG : Affiche le prix extrait
echo "Prix extrait : $price"

# J'enregistre les données dans un CSV
printf "%s,%.2f\n" "$now" "$price" >> ./data/bitcoin_prices.csv


# DEBUG : Affiche le contenu du fichier
echo "Contenu actuel :"
cat ./data/bitcoin_prices.csv
