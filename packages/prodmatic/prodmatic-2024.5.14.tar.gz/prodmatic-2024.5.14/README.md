# Prodmatic

Prodmatic is a Python library that provides seamless management and pricing solutions for in-app products and subscriptions on both Google Play Store and Apple App Store. It simplifies access to store APIs and provides country-specific pricing using Public-Private Partnership (PPP) conversions.

## Features

- **Google Play Store Integration**:

  - List, add, update, and delete in-app products and subscriptions
  - Convert in-app prices to store-compatible formats based on PPP and forex exchange rates

- **Apple App Store Integration** (WIP):

  - Placeholder for future features

- **Pricing Module**:
  - Convert prices based on PPP, forex rates, and store pricing guidelines
  - Support for Google Play Store reference pricing

## Installation

You can install Prodmatic using pip:

```bash
pip install prodmatic
```

## Usage

### Play Store Integration

To integrate with the Google Play Store, you'll need a service account with the appropriate permissions.

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build
from prodmatic.playstore.api import PlayStoreAPI

SCOPES = ['https://www.googleapis.com/auth/androidpublisher']
SERVICE_ACCOUNT_FILE = 'path/to/your/service-account.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('androidpublisher', 'v3', credentials=credentials)

# Initialize PlayStoreAPI
play_store_api = PlayStoreAPI(service, 'com.example.app')

# List all in-app products
iaps = play_store_api.list_iaps()

# Add a new in-app product
iap_data = {
    'sku': 'new_sku',
    'title': 'New In-App Product',
    'description': 'Description of the new in-app product',
    # Add other fields as required
}
play_store_api.add_iap('new_sku', iap_data)
```

### Play Store Pricing

To get equivalent in-app product pricing in different countries based on PPP and store pricing formats:

```python
from prodmatic.playstore.pricing import PlayStorePricing

# Initialize PlayStorePricing
play_store_pricing = PlayStorePricing()

# Get store price mapping
price_mapping = play_store_pricing.get_store_price_mapping(
    source_country='US',
    source_price=79,
    destination_country='IN'
)

print(price_mapping)
```

## Directory Structure

```
prodmatic
├── __init__.py
├── appstore
│   ├── __init__.py
│   ├── api.py (WIP)
│   └── pricing.py (WIP)
├── base
│   ├── __init__.py
│   ├── api.py
│   └── pricing.py
├── playstore
│   ├── __init__.py
│   ├── api.py
│   └── pricing.py
└── resources
    ├── appstore_reference_prices.csv
    ├── data_sources.json
    └── playstore_reference_prices.csv
```

## Resources

- `data_sources.json`: Contains URLs for currency mappings
- `playstore_reference_prices.csv`: Google Play Store reference pricing data

## License

Prodmatic is licensed under the [GNU Affero General Public License v3.0](https://www.gnu.org/licenses/agpl-3.0.html).

## Repository

For more information and to contribute, please visit the GitHub repository:
[https://github.com/musicmuni/prodmatic](https://github.com/musicmuni/prodmatic)
