from tgtg import TgtgClient
import time
import json
import os

ITEM_ID = "REPLACE_WITH_ITEM_ID"  # Run get_item_id.py first to find this
CHECK_INTERVAL = 20  # seconds between polls — don't go lower or TGTG may flag your account
CREDENTIALS_FILE = "tgtg_credentials.json"


def get_client():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE) as f:
            creds = json.load(f)
        return TgtgClient(
            access_token=creds["access_token"],
            refresh_token=creds["refresh_token"],
            user_id=creds["user_id"],
            cookie=creds.get("cookie", "")
        )
    else:
        # First run — TGTG will send a magic link to your email, click it within 60s
        client = TgtgClient(email="your@email.com")
        creds = client.get_credentials()
        with open(CREDENTIALS_FILE, "w") as f:
            json.dump(creds, f)
        print("Credentials saved to tgtg_credentials.json")
        return client


client = get_client()
print(f"Watching for bag (item {ITEM_ID})...")

while True:
    try:
        items = client.get_items(item_ids=[ITEM_ID])
        for item in items:
            available = item["items_available"]
            print(f"[{time.strftime('%H:%M:%S')}] Available: {available}")

            if available > 0:
                print("BAG AVAILABLE — creating order...")
                order = client.create_order(
                    item_id=ITEM_ID,
                    display_name=item["display_name"]
                )
                order_id = order["id"]
                print(f"Order reserved: {order_id}")

                client.pay_order(order_id=order_id)
                print("PAID. Done. Go pick up your bag!")
                exit(0)

    except Exception as e:
        print(f"Error: {e}")
        if "unauthorized" in str(e).lower():
            os.remove(CREDENTIALS_FILE)
            client = get_client()

    time.sleep(CHECK_INTERVAL)
