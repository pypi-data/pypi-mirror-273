# Import des packages
from lgjsfinance import DataRecover

# Definir la classe et la currency
data = DataRecover("EURUSD=X")

# Récupérer l'historique des prix de la journée
historique_prix = data.get_close_prices_hourly()

# Récupérer les 16 dernières données
print(historique_prix.tail(16))

# Tracer le graphique
data.show_graph(historique_prix)