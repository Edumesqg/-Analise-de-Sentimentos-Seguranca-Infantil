import asyncio
from twikit import Client, TooManyRequests, TwitterException
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint
import pandas as pd

MINIMUM_TWEETS = 10
# Adiciona o filtro de idioma na consulta
QUERY = 'Vendo  "Camera canon" lang:pt -filter:replies'
MAX_TWEETS = 20  # Define o número máximo de tweets a serem buscados

# Login credentials
config = ConfigParser()
config.read('config.ini')
username = config['X']['username']
password = config['X']['password']

# async def main():
#     try:
#         # Authenticate
#         client = Client(language='pt-BR')
#         await client.login(auth_info_1=username, auth_info_2=username, password=password)
#         client.save_cookies('cookies.json')
#     except TwitterException as e:
#         print(f"Erro ao tentar fazer login: {e}")
#         return

# Executa a função principal
# asyncio.run(main())

client = Client(language='pt-BR')
client.load_cookies('cookies.json')

# Criando arq. CSV
with open('tweets.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Tweet_count', 'Username', 'Text',
                    'Created At', 'Retweets', 'Favorites'])

# Get tweets


async def get_tweets():
    tweet_count = 0  # Inicializa a variável dentro da função
    try:
        while tweet_count < MAX_TWEETS:
            tweets = await client.search_tweet(QUERY, product='Top', count=MAX_TWEETS - tweet_count)
            if not tweets:
                break  # Interrompe o loop se não houver mais tweets
            for tweet in tweets:
                tweet_count += 1
                tweet_data = [
                    tweet_count, tweet.user.name, tweet.text, tweet.created_at, tweet.retweet_count, tweet.favorite_count
                ]
                print(tweet_data)

                with open('tweets.csv', 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(tweet_data)

                print(f'{datetime.now()} - Got {tweet_count} tweets.')

                # Adiciona um atraso entre 5 e 10 segundos
                await asyncio.sleep(randint(5, 10))

                if tweet_count >= MAX_TWEETS:
                    break  # Interrompe o loop após atingir o número máximo de tweets

        print(f'{datetime.now()} - Done! Got {tweet_count} tweets.')
    except TwitterException as e:
        print(f"Erro ao tentar buscar tweets: {e}")

# Executa a função para obter tweets
asyncio.run(get_tweets())

# Lê o arquivo CSV e exibe em formato de tabela
df = pd.read_csv('tweets.csv')
print(df)
