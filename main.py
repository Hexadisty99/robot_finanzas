import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import time
import re

# URL a scrapear
url = 'https://finviz.com/news.ashx?v=3'
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
website = urlopen(req).read()
html = BeautifulSoup(website, 'html.parser')

# Inicializamos el analizador de sentimiento de NLTK
analyzer = SentimentIntensityAnalyzer()

# Función de análisis del sentimiento usando NLTK
def analyze_sentiment(text):
    sentiment_scores = analyzer.polarity_scores(text)
    compound_score = sentiment_scores["compound"]
    return compound_score

# Función para obtener el DataFrame de noticias
def get_news():
    try:
        # Buscamos la tabla usando sus clases
        table = html.find('table', attrs={'class': 'styled-table-new is-rounded table-fixed'})
        if table is None:
            print("No se encontró la tabla de noticias.")
            return None

        rows = table.find_all('tr')
        data = []

        for row in rows:
            # Extraer la fecha de la primera celda
            date_cell = row.find('td', class_='news_date-cell')
            date_text = date_cell.get_text(strip=True) if date_cell else None

            # Extraer la celda que contiene la noticia y los tickers
            news_cell = row.find('td', class_='news_link-cell')
            if news_cell:
                # Suponemos que el titular de la noticia es el texto del primer enlace
                news_link = news_cell.find('a', href=True)
                news_headline = news_link.get_text(strip=True) if news_link else ''

                # Buscar todos los enlaces que contengan el ticker: 'quote.ashx?t='
                ticker_links = news_cell.find_all('a', href=lambda href: href and 'quote.ashx?t=' in href)
                tickers_list = []
                for t_link in ticker_links:
                    href = t_link.get('href')
                    # Extraemos lo que sigue a 't=' con una expresión regular
                    match = re.search(r't=([^&]+)', href)
                    if match:
                        tickers_list.append(match.group(1))
            else:
                news_headline = ''
                tickers_list = []

            for ticker in tickers_list:
                data.append({
                    'Date': date_text,
                    'News Headline': news_headline,
                    'Ticker': ticker
                })

        # Creamos el DataFrame y establecemos la columna 'Date' como índice
        df = pd.DataFrame(data)
        df.set_index('Date', inplace=True)
        return df

    except Exception as e:
        print("Se produjo un error:", e)
        return None

while True:
    news_df = get_news()

    if news_df is not None:
        # Listas para almacenar la fecha, el sentimiento y los tickers
        dates = []
        sentiment_values = []
        tickers = []

        # Iteramos sobre el DataFrame; el índice 'date' contiene la fecha de cada noticia
        for date, row in news_df.iterrows():
            headline = row['News Headline']
            ticker = row['Ticker']
            sentiment = analyze_sentiment(headline)

            dates.append(date)
            sentiment_values.append(sentiment)
            tickers.append(ticker)

        # Creamos el DataFrame con las columnas "Date", "Sentiment" y "Ticker"
        sentiment_df = pd.DataFrame({
            'Date': dates,
            'Sentiment': sentiment_values,
            'Ticker': tickers
        })

        # Filtro
        filtered_sentiment_df = sentiment_df[(sentiment_df['Sentiment'] < -0.5) | (sentiment_df['Sentiment'] > 0.5)]

        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print("\n")
            # print(sentiment_df)
            print(filtered_sentiment_df)
            time.sleep(30)

    else:
        print("No se pudo obtener el DataFrame de noticias.")

    website = urlopen(req).read()
    html = BeautifulSoup(website, 'html.parser')


