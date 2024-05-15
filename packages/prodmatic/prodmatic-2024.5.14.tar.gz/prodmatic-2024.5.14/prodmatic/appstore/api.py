import jwt
import datetime
import requests
from ..base.api import StoreAPI


class AppStoreAPI:
    def __init__(self, app_id, key_id, issuer_id, private_key):
        """
        Initialize the AppStoreAPI with credentials necessary for JWT authentication.

        Parameters:
        key_id (str): Key ID from the Apple Developer account.
        issuer_id (str): Issuer ID from the Apple Developer account.
        private_key (str): Contents of the private key (.p8 file) from your API key.
        """
        self.app_id = app_id
        self.key_id = key_id
        self.issuer_id = issuer_id
        self.private_key = private_key
        self.base_url = "https://api.appstoreconnect.apple.com"
        self.token = self._generate_token()

    def _generate_token(self):
        """Generate a JWT token for authentication."""
        time_now = datetime.datetime.utcnow()
        time_expire = time_now + datetime.timedelta(minutes=20)  # Token valid for 20 minutes
        payload = {"iss": self.issuer_id, "exp": int(time_expire.timestamp()), "aud": "appstoreconnect-v1"}
        header = {"alg": "ES256", "kid": self.key_id, "typ": "JWT"}
        token = jwt.encode(payload, self.private_key, algorithm="ES256", headers=header)
        return token.decode("utf-8") if isinstance(token, bytes) else token

    def list_iaps(self):
        """
        Retrieve all in-app purchases (IAPs) for a specific application using App Store Connect API v1.

        Parameters:
        app_id (str): The unique identifier for the app whose IAPs you want to list.

        Returns:
        list: A list of IAP details.
        """
        url = f"{self.base_url}/v1/apps/{self.app_id}/inAppPurchases"
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("data", [])
        else:
            raise Exception(f"Failed to list IAPs: {response.status_code} {response.text}")
