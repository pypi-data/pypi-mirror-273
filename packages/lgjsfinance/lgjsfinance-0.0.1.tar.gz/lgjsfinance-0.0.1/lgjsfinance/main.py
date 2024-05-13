import yfinance as yf
import matplotlib.pyplot as plt
import time as tps
from datetime import datetime, time

class Settings:
    max_cache_age = 60

class DataRecover():
    def __init__(self, entreprise, settings=Settings()):
        self.corp = entreprise
        self.settings = settings
        
        self.ticker = yf.Ticker(entreprise)

    def get_data(self):
        start_of_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return self.ticker.download(start=start_of_day)
        #return self.ticker.history(period="max")
    
    def show_graph(self, data):
        plt.figure(figsize=(10, 6))
        plt.plot(data.index, data['Close'], label='Prix de clôture')
        plt.title('Graphique de clôture')
        plt.xlabel('Date')
        plt.ylabel('Prix de clôture (en $)')
        plt.legend()
        plt.grid(True)
        plt.show()#2714.735107

    def get_close_prices_hourly(self):
        date_a_minuit = datetime.combine(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0), time.min)
        historique_prix = yf.download(self.corp, start=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0), interval='1m')
        return historique_prix


start_time = tps.time()

data = DataRecover("EURUSD=X")

historique_prix = data.get_close_prices_hourly()
print(type(historique_prix.tail(16)))
#print(historique_prix)

"""while True:
    historique_prix = data.get_data()
    print("Prix de cloture : ", historique_prix.iloc[-1]['Close'])
    tps.sleep(30)"""

end_time = tps.time()
duree_requete = end_time - start_time
print("La requête a pris {} secondes.".format(duree_requete))

# Tracer le graphique
#data.show_graph(historique_prix)