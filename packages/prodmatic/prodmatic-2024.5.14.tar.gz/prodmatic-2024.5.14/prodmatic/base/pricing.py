from pyrestcountries.api import RestCountriesAPI
from pppfy.converter import Converter
from moneymatters.api import ExchangeAPI, Formatter
from abc import ABC, abstractmethod


class StorePricing(ABC):
    countries_api = RestCountriesAPI()
    pppfy_converter = Converter()
    forex_api = ExchangeAPI()
    formatter = Formatter()

    def __init__(self):
        # A map of iso2_code: 3 letter ISO code for the currency used for that country in playstore
        self.map_country_to_store_currency = {}

        # A map of iso2_code: price
        self.map_country_to_reference_rounded_price = {}

    @abstractmethod
    def fetch_country_to_store_currency_map(self, store_reference_prices_file):
        """
        Get the recent most information on the currency that a given store supports for a given country
        """
        pass

    @abstractmethod
    def load_country_to_reference_rounded_prices(self):
        """
        Load, from local/network, reference prices for all the countries supported in a given store
        """
        pass

    def get_store_price_mapping(self, source_country="US", source_price=79, destination_country=None, year=None):
        # Get equivalent prices in destination countries, based on PPP
        ppp_price_mapping = self.pppfy_converter.get_price_mapping(
            source_country, source_price, destination_country, year
        )

        if isinstance(ppp_price_mapping, dict):
            ppp_price_mapping = [ppp_price_mapping]

        store_prices = []
        for mapping in ppp_price_mapping:
            iso2_code = mapping["ISO2"]
            local_price = mapping["ppp_adjusted_local_price"]
            country_info = self.countries_api.fetch_country_by_cca2(iso2_code)
            local_currencies = list(country_info.currencies.keys())

            # Convert local currency to store supported currency
            store_currency = "USD"
            if iso2_code in self.map_country_to_store_currency:
                store_currency = self.map_country_to_store_currency[iso2_code]["store_currency"]
            store_price = self.forex_api.convert(
                price=local_price, from_currency=local_currencies[0], to_currency=store_currency
            )

            # Some heavily devalued currencies might end up with very low usd values < 10
            # TODO needs a better fix
            if store_price < 10:
                store_price = 10

            # Round off to a format that store recommends
            store_price_format = self.map_country_to_reference_rounded_price.get(iso2_code, 0)
            rounded_price = self.formatter.apply_price_format(price=store_price, format=store_price_format)

            mapping["store_currency"] = store_currency
            mapping["store_price"] = rounded_price
            store_prices.append(mapping)

        return store_prices
