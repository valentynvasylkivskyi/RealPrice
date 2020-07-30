import tldextract
link = "https://agro-market.net/catalog/item/klen_veernyy_feniks_acer_palmatum_phoenix_konteyner_p9/"

scraper = tldextract.extract(link).domain
print(scraper)
