import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

class DataRecover():
    def __init__(self, entreprise):
        self.corp = entreprise

    def get_day_data(self, date_string):
        return yf.download(self.corp, start=datetime.strptime(date_string, "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=1), end=datetime.strptime(date_string, "%Y-%m-%d").replace(hour=23, minute=59, second=59, microsecond=59), interval='1m', progress=False)

    def get_data(self):
        start_of_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return yf.download(self.corp, start=start_of_day, progress=False)
    
    def show_graph(self, data):
        plt.figure(figsize=(10, 6))
        plt.plot(data.index, data['Close'], label='Prix de clôture')
        plt.title('Graphique de clôture')
        plt.xlabel('Date')
        plt.ylabel('Prix de clôture (en $)')
        plt.legend()
        plt.grid(True)
        plt.show()

    def get_close_prices_hourly(self):
        historique_prix = yf.download(self.corp, start=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0), interval='1m', progress=False)
        return historique_prix