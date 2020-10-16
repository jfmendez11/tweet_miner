import os
from dotenv import load_dotenv
from twitter_miner import TwittterMiner
import pprint
from pymongo import MongoClient

screen_names = [
  "Uniandes",
  "agaviriau",
  "DEUniandes",
  "inguniandes",
  "facisouniandes",
  "UniandesDerecho",
  "MediUniandes",
  "CPolUniandes",
  "EconomiaUniandes",
  "CiderUniandes",
  "EdCoUniandes",
  "AdmonUniandes",
  "GobiernoUAndes",
  "Ceper_Uniandes",
  "CulturaUniandes",
  "CienciasUAndes",
  "CEFAUniandes",
  "GDIPUniandes",
  "_CONSEFE",
  "IEEEUniandes",
  "CEGOBUniandes",
  "CeuDerecho",
  "ceuniandino",
  "pzalamea",
  "uniandesbiblio",
  "cerosetenta",
  "EdcoUniandes",
  "rettberg_a",
  "ljhernandezf",
  "philipp_hessel",
  "DanielMejiaL",
  "Felipe_Acosta1",
  "Rev_Ingenieria",
  "ConectaTE_U",
  "BecadosUniandes",
  "diegosierrab",
  "Adcamach",
  "lucerovgo",
  "CrawfordAJ",
  "Parra_Leonardo",
  "SantiagoVargasN",
  "PosgradosUAndes",
  "Mafe_Rosales_R",
  "NatRamBus",
  "AntrUniandes",
  "oscarunivio",
  "juandacontreras",
  "CTPUniandes",
  "UniandesCEIM",
  "admision_uandes",
  "gipuniandes",
  "sandraborda",
  "DeportesUniande",
  "MariUniandes",
  "CamilaFarfanL",
  "CamiloMontes",
  "fabiosanchez_to",
  "JmChenou",
  "amoterocleves",
  "FelipeMontesJ",
  "SEHernandezR",
  "mlcepedah",
  "catmuno",
  "GarzonGuerrero",
  "JavierPinedaD",
  "TrainaVJuli",
  "mortiz217",
  "juansgalan"
]

def main():
  load_dotenv()
  twitter_keys = {
    "consumer_key": os.getenv("TWITTER_API_KEY"),
    "consumer_secret": os.getenv("TWITTER_API_SECRET_KEY"),
    "access_token": os.getenv("TWITTER_ACCESS_TOKEN"),
    "access_token_secret": os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
  }

  miner = TwittterMiner(keys_dict=twitter_keys, result_limit=20)
  data = miner.mine_user_tweets(user="agaviriau", max_pages=10)
  pprint.pprint(data)
  