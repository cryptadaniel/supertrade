BI_API_KEY = "xxxxxxxxxxxxx"
BI_API_SECRET = "yyyyyyyyyyyyyyyyyy"
KU_API_KEY = "xxxxxxxxxxxxx"
KU_API_SECRET = "yyyyyyyyyyyyyyyyyy"
KU_API_PASSPHRASE = "zzzzzzzzzzzzzzz"
GA_API_KEY = "xxxxxxxxxxxxx"
GA_API_SECRET = "yyyyyyyyyyyyyyyyyy"


exchange_keys = {
         "kucoin": """{
               "apiKey": config.KU_API_KEY,
               "secret": config.KU_API_SECRET,
               "password": config.KU_API_PASSPHRASE
         }""",
         "gateio": """{
             "apiKey": config.GA_API_KEY,
             "secret": config.GA_API_SECRET
         }""",
         "binance": """{
             "apiKey": config.BI_API_KEY,
             "secret": config.BI_API_SECRET
         }"""
}
