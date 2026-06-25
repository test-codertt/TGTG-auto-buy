from tgtg import TgtgClient

# Run this once to find Seoul Bakery's item ID, then paste it into tgtg_autobuy.py
# Make sure the bakery is in your TGTG favourites first (easiest way to find it)

client = TgtgClient(email="your@email.com")
items = client.get_items(favorites_only=True)

for item in items:
    print(item["item"]["item_id"], "—", item["display_name"])
