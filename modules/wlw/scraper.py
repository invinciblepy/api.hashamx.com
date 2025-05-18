import time
from urllib import parse
import user_agent
import random
from .wrapper import fetch_url


class wlw:
    def __init__(self, url=None):
        self.base_url = "https://www.wlw.de/de/suche"
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'priority': 'u=1, i',
            'referer': 'https://www.wlw.de/de/suche?q=solar+installer',
            'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
            # 'cookie': 'language=de; vwo_user_id=b5f2d679-0e56-4ed5-b18d-66ad742334c8; CookieConsent={stamp:%27C5nEX6YmtIJ6Xjjs1qsB5qd3RdMhZQisEEkGQmzxrwN6SsWprUGyxw==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1747552033323%2Cregion:%27pk%27}; existing_session=True; _ga=GA1.1.1599060059.1747552035; FPID=FPID2.2.Qr0IyxMIPzzUooBmEPoJ6h4appX7BcFsKV6QNg8IAak%3D.1747552035; _gcl_au=1.1.1794322139.1747552035; FPAU=1.2.818812130.1747552036; _fbp=fb.1.1747552035510.1031601120; _uetsid=baa7f66033b611f0ba5fe18a8cf23bb2; _uetvid=baa8449033b611f0a60cab422ba2d89c; FPLC=uoLaXE5DHsD3VpRIetW%2F3rxCdL6%2BG8m0AHIHMfCd3lmTB9yEPPN%2BrFFWovQJzxWcOuPaSfJoab6PoGaaiDYvQhCadD8hOEVtjFd2C%2FGAUGTvc%2BFbHu4ES%2Bm1wlvR%2BA%3D%3D; _hjSessionUser_1300776=eyJpZCI6IjAwZDIwMDVhLWQ3MTctNWE4Ny1hN2M1LWI2YTM2ZjYzOTA2NiIsImNyZWF0ZWQiOjE3NDc1NTIwMzU3NjEsImV4aXN0aW5nIjp0cnVlfQ==; _hjSession_1300776=eyJpZCI6ImVlOGE4OGIwLTEzZWItNDlhMi1hOWRkLTk3YjNkNzE0ZTMwNiIsImMiOjE3NDc1NTIwMzU3NjIsInMiOjEsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MX0=; __hstc=80469576.a0fed4ae76bc8473ce52551c73208b4f.1747552035821.1747552035821.1747552035821.1; hubspotutk=a0fed4ae76bc8473ce52551c73208b4f; __hssrc=1; _ga_W7JGN76FFP=GS2.1.s1747552034$o1$g0$t1747552039$j0$l0$h1614303979; wlw_search_term=solar%20installer; ufs_session_id=48f4fa36a11b9058; wlw_search_type=companies; __hssc=80469576.2.1747552035821; _ga_V3P0WCZ5B3=GS2.1.s1747552035$o1$g1$t1747552855$j0$l0$h0; _ga_L3FB6W3KNC=GS2.1.s1747552047$o1$g0$t1747552855$j0$l0$h1203696099; aws-waf-token=e8cfb685-567e-410a-9904-8cfb174f6e8e:CQoAaaAzVXlOAAAA:W+xRWTh1U2kA3hh+buAQOzTU8b8MCMzTuYg8mVyLFaV6Q6iF/Dx6gZxhGYEeRfx8PtJG+Buwuibbx/bBEgG3PdTVzCf7X9gh6Wb7xzMsjv90fZi5uhEElqTdX2+FF/z/Ma2IwFWd4t0SfOnScESpiLIwl6cFiagkB48MCQT8yMR+EZjijTBP17UUXGK9; ab_testing_variants_v2=%7B%22template%22%3A%7B%22name%22%3A%22control%22%2C%22dimension%22%3A%22%22%2C%22active%22%3Atrue%2C%22expiry%22%3A1748157668%7D%7D',
        }

        self.url = url
        self.items = []
        self.total_items = 0

    def create_params(self, url):
        params = {}
        if "/products" in url:
            print("[x] Product Pages Not Supported")
            exit()
        else:
            parsed_url = parse.urlparse(url)
            query_params = parsed_url.query.replace("q=", "")
            tld = parsed_url.netloc.split(".")[-1]
            params["query"] = query_params
            params["lang"] = tld
            params["country"] = tld.upper()
            params["site"] = "wlw"
            params["top_level_domain"] = tld.upper()
            params["city_extraction_radius"] = "50km"
            params["sort"] = "responsiveness"
            params["userLatitude"] = random.uniform(48.0, 54.0)
            params["userLongitude"] = random.uniform(6.0, 15.0)
        return params

    def scrape(self, page=1):
        if "/products" in self.url:
            print("[x] Product Pages Not Supported")
            return
        params = self.create_params(self.url)
        params["page"] = page
        response = fetch_url("https://www.wlw.de/search-frontend/alibaba-api/online.company.search", params=params, headers=self.headers)
        companies = response.get("data", {}).get("companies", [])
        for company in companies:
            self.items.append({
                "name": company.get("name"),
                "street": company.get("street"),
                "city": company.get("city"),
                "zip_code": company.get("zipcode"),
                "country": company.get("country_code"),
                "supplier_types": ", ".join(company.get("supplier_types", [])),
                "phone_number": company.get("phone_number"),
                "homepage": company.get("homepage"),
                "slug": company.get("slug"),
                "description": company.get("highlightings", {}).get("secondary_description", ""),
                "employee_count": company.get("employee_count"),
                "product_count": company.get("product_count"),
                "distribution_area": company.get("distribution_area"),
                "founding_year": company.get("founding_year"),
                "average_response_time": company.get("average_response_time"),
            })
            time.sleep(0.5)
        return self.total_items,self.items
