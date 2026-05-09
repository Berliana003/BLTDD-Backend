import json
import os
from urllib import error, request


def sync_warga_to_firebase(payload):
    database_url = os.environ.get('FIREBASE_DATABASE_URL', '').strip()
    if not database_url:
        return None

    normalized_url = database_url.rstrip('/')
    endpoint = f"{normalized_url}/warga.json"
    body = json.dumps(payload).encode('utf-8')

    req = request.Request(
        endpoint,
        data=body,
        headers={'Content-Type': 'application/json'},
        method='POST',
    )

    try:
        with request.urlopen(req, timeout=15) as response:
            response_body = response.read().decode('utf-8')
            data = json.loads(response_body) if response_body else {}
            return data.get('name')
    except error.URLError as exc:
        raise RuntimeError(f"Gagal sinkron ke Firebase: {exc}") from exc
