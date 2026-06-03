import pandas as pd
from app.utils.config import settings

class BitcoinData:
    def __init__(self):
        # läsa CSV-filen
        self.df = pd.read_csv(settings.bitcoin_data_path)
        # vi förklarar till pandas att day kolumn är datum
        self.df['Day'] = pd.to_datetime(self.df['Day'])
        
    def get_stats(self) -> dict:
        # hämta priset och dagen för den allra sista raden i filen
        latest_close = self.df['Close'].iloc[-1]
        latest_day = self.df['Day'].iloc[-1].day
        
        # payday FOMO logik
        if latest_day >= 25 or latest_day <= 2:
            payday_fomo = "Hög (Löningsdags!)"
        else:
            payday_fomo = "Låg (Mitten av månaden, folk har mindre pengar)"
            
        # bollinger bot logik (baserat på sista 20 dagarna)
        recent_20 = self.df.tail(20)
        mean_20 = recent_20['Close'].mean()
        std_20 = recent_20['Close'].std()
        
        # skapa gummibanden
        upper_band = mean_20 + (2 * std_20)
        lower_band = mean_20 - (2 * std_20)
        
        # bot-logiken för köp/sälj signal
        if latest_close >= upper_band:
            bot_signal = "SÄLJ (Priset rör vid övre gummibandet, för dyrt!)"
        elif latest_close <= lower_band:
            bot_signal = "KÖP (Priset är vid nedre gummibandet, rea!)"
        else:
            bot_signal = "AVVAKTA (Priset är i mitten, gör ingenting)"

        # skicka tillbaka resultatet snyggt förpackat
        return {
            "senaste_pris": round(latest_close, 2),
            "payday_fomo": payday_fomo,
            "bollinger_signal": bot_signal
        }

# skapa en färdig element
btc_data = BitcoinData()