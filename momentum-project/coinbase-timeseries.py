from coinbase.wallet.client import Client

API_KEY = "dPDPi3BlNGWlWwkh"
API_SECRET = "GfWliBkJtr7cNllIuT0hVRNXGMbjwpPT"

client = Client(API_KEY, API_SECRET)

accounts = client.get_accounts()
client.get_exchange_rates()

print(accounts)