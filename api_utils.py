import httpx
import logging
from config import API_VOICE_URL, API_TEXT_URL

def format_api_response(data) -> str:
    if isinstance(data, dict):
        return data.get("answer") or data.get("result") or str(data)
    elif isinstance(data, list):
        if not data:
            return "📭 No data available."
        result = []
        for item in data:
            if isinstance(item, dict):
                name = item.get("النوع") or item.get("name") or item.get("invoiceNo", "")
                qty = item.get("الكمية") or item.get("qty") or ""
                line = f"📦 Type: {name}\n🔢 Quantity: {qty} tons"
                result.append(line)
            else:
                result.append(str(item))
        return "📄 Data:\n\n" + "\n\n".join(result)
    return str(data)

async def ask_voice_api(text: str) -> str:
    try:
        async with httpx.AsyncClient(verify=False, timeout=10) as client:
            response = await client.post(API_VOICE_URL, json={"text": text})
            return format_api_response(response.json())
    except Exception as e:
        logging.exception(f"Voice API error: {e}")
        return f"❌ could not understand the request: {text}"

async def forward_to_external_api(update):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            payload = update.to_dict()
            response = await client.post(API_TEXT_URL, json=payload)
            if response.status_code == 200:
                logging.info("Message successfully sent to external API.")
            else:
                logging.error(f"Failed to send message. Status code: {response.status_code}")
    except Exception as e:
        logging.exception(f"Error sending message to webhook: {e}")
