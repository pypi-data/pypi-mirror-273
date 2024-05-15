import csv
import json
from decimal import Decimal

import requests
from bs4 import BeautifulSoup
from importlib import resources
from ..base.pricing import StorePricing


class AppStorePricing(StorePricing):
    def __init__(self):
        super().__init__()
        self.fetch_country_to_store_currency_map()
        self.load_country_to_reference_rounded_prices()

    def load_country_to_reference_rounded_prices(self):
        with resources.open_text("prodmatic.resources", "appstore_reference_prices.csv") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                country = self.countries_api.search_countries(row["Countries or Regions"])[0]
                iso_code = country.cca2
                if iso_code:
                    self.map_country_to_reference_rounded_price[iso_code] = Decimal(row["Price"])
                else:
                    print(f"No ISO code found for {row['Countries or Regions']}")

    def fetch_country_to_store_currency_map(self):
        # Get the data from the appstore's official link
        data_sources = json.load(resources.open_text("prodmatic.resources", "data_sources.json"))
        region_currency_reference_url = data_sources["appstore_region_currency_reference"]
        response = requests.get(region_currency_reference_url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the table - you may need to adjust the selector based on the actual page structure
        table = soup.find("table")
        headers = [th.get_text(strip=True) for th in table.find_all("th")]
        data = []
        for row in table.find_all("tr")[1:]:  # Skip header row
            columns = [col.get_text(strip=True) for col in row.find_all("td")]
            data.append(dict(zip(headers, columns)))

        # Some of the rows have region with multiple countries, let's split them up
        self.map_country_to_store_currency = {}
        for item in data:
            if item["Region Code"] in ["ZZ", "Z1"]:
                continue
            if "," in item["Countries or Regions"]:
                country_names = [i.strip() for i in item["Countries or Regions"].split(",")]
                for c in country_names:
                    country = self.countries_api.search_countries(c)[0]
                    iso_code = country.cca2
                    if not iso_code:
                        print(c, "has no iso code!")

                    # Countries like Vietnam and Pakistan have their own currencies supported, but are mentioned in WW as well
                    # Keep their own currencies
                    if iso_code in self.map_country_to_store_currency.keys() and item["Region Code"] in [
                        "EU",
                        "LL",
                        "WW",
                    ]:
                        continue

                    country_info = {
                        "country": c,
                        "iso2_code": iso_code,
                        "store_currency": item["Report Currency"],
                    }
                    self.map_country_to_store_currency[iso_code] = country_info
            else:
                country_info = {
                    "country": item["Countries or Regions"],
                    "iso2_code": item["Region Code"],
                    "store_currency": item["Report Currency"],
                }
                self.map_country_to_store_currency[item["Region Code"]] = country_info
