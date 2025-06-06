import json
import re
import requests
from lxml import html



class googlemaps:
    def __init__(self, url: str):
        self.url = url
        if "google.com/maps/" not in url:
            return 0, []

        self.session = requests.Session()
        self.session.headers.update({
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'dnt': '1',
            'downlink': '10',
            'priority': 'u=0, i',
            'rtt': '200',
            'sec-ch-prefers-color-scheme': 'dark',
            'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version-list': '"Chromium";v="136.0.7103.93", "Google Chrome";v="136.0.7103.93", "Not.A/Brand";v="99.0.0.0"',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        })
        self.locations = []

    def consent_page(self, response):
        tree = html.fromstring(response.text)
        form = tree.xpath("//form")[0]
        action = form.get("action")
        method = form.get("method")
        inputs = form.xpath(".//input")
        data = {input.get("name"): input.get("value") for input in inputs}
        response = self.session.request(method, action, data=data)
        return response
    
    def scrape(self):
        response = self.session.get(self.url)
        if "consent.google" in response.url:
            response = self.consent_page(response)
        pattern = r'window\.APP_INITIALIZATION_STATE\s*=\s*\[(.*?)\];'
        match = re.search(pattern, response.text)
        if not match:
            print(response.status_code)
            print("No Items found")
            return 0,[]
            
        state_str = match.group(1)
        state = json.loads(f"[{state_str}]")
        events_arr = state[3][2].replace(")]}'\n", "")
        all_events = json.loads(events_arr)
        
        for event in all_events[64]:
            if isinstance(event[1], list):
                self.locations.append(self.fetch_event_data(event[1]))
        return len(self.locations), self.locations
        
    def fetch_event_data(self, event):
        return {
            "name": event[11],
            "address": event[18] or event[39],
            "attributes": ', '.join(attr[0] for attr in event[76]),
            "place_id": event[89],
            "rating": self.safe_get(event, 4, 7),
            "reviews_count": self.safe_get(event, 4, 8),
            "phone": self.safe_get(event, 178, 0, 0) if isinstance(event[178], list) else None,
            "url": self.safe_get(event, 7, 0) if isinstance(event[7], list) else None
        }

    def safe_get(self, event, *indexes):
        for index in indexes:
            if isinstance(event, list) and index < len(event):
                event = event[index]
            else:
                return None
        return event