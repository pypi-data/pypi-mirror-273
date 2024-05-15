from ..base.api import StoreAPI


class PlayStoreAPI(StoreAPI):
    def __init__(self, google_service, package_name):
        """
        Initialize the PlayStoreAPI with a Google API service object and a package name.

        Parameters:
        google_service (Resource): This is an instance of googleapiclient.discovery.build that is setup
                                   to have access to your Google Play Console account/app.
                                   You need to have authenticated credentials that have the necessary
                                   permissions to access the Android Publisher API.
        package_name (str): The Google Play package name of your app (e.g., 'com.example.app').

        Example:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

        SCOPES = ['https://www.googleapis.com/auth/androidpublisher']
        SERVICE_ACCOUNT_FILE = 'path/to/your/service-account.json'

        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('androidpublisher', 'v3', credentials=credentials)

        play_store_api = PlayStoreAPI(service, 'com.example.app')
        """
        super().__init__()
        self.service = google_service
        self.package_name = package_name

    def list_iaps(self):
        """
        Retrieve all in-app products (IAPs) configured for the application using the monetization API,
        automatically handling pagination.

        Returns:
        list: A complete list of dictionaries, each containing details of an IAP.
        """
        all_iaps = []
        page_token = None
        try:
            while True:
                response = (
                    self.service.monetization()
                    .inappproducts()
                    .list(packageName=self.package_name, pageToken=page_token)
                    .execute()
                )
                iaps = response.get("inappproducts", [])
                all_iaps.extend(iaps)
                page_token = response.get("nextPageToken")
                if not page_token:
                    break
        except Exception as e:
            raise Exception(f"Error listing IAPs: {e}")
        return all_iaps

    def get_iap(self, iap_identifier):
        """
        Retrieve the details of an in-app product (IAP) if it exists.

        Parameters:
        iap_identifier (str): The SKU of the in-app product.

        Returns:
        dict: A dictionary containing the IAP details if found, None otherwise.
        """
        try:
            result = self.service.inappproducts().get(packageName=self.package_name, sku=iap_identifier).execute()
            return result
        except Exception as e:
            print(f"Error fetching IAP: {e}")
            return None

    def add_iap(self, iap_identifier, iap_data):
        """
        Add a new in-app product (IAP) to the Google Play Store.

        Parameters:
        iap_identifier (str): The SKU of the new in-app product.
        iap_data (dict): A dictionary containing the details of the IAP. This should conform to the
                         structure required by the Google Play Developer API.

        Returns:
        dict: A dictionary containing the response from the API if the IAP is successfully added.
        None: If the addition fails, returns None.

        Raises:
        Exception: If the API request fails, raises an exception with a clear error message.
        """
        try:
            response = self.service.inappproducts().insert(packageName=self.package_name, body=iap_data).execute()
            return response
        except Exception as e:
            raise Exception(f"Failed to add IAP '{iap_identifier}': {e}")

    def delete_iap(self, iap_identifier):
        """
        Delete an in-app product (IAP) from the Google Play Store.

        Parameters:
        iap_identifier (str): The SKU of the in-app product to be deleted.

        Returns:
        bool: True if the deletion was successful, False otherwise.

        Raises:
        Exception: If the API request fails, raises an exception with a clear error message.
        """
        try:
            self.service.inappproducts().delete(packageName=self.package_name, sku=iap_identifier).execute()
            return True
        except Exception as e:
            raise Exception(f"Failed to delete IAP '{iap_identifier}': {e}")

    def update_iap(self, iap_identifier, iap_data):
        """
        Update an existing in-app product (IAP) in the Google Play Store.

        Parameters:
        iap_identifier (str): The SKU of the in-app product to be updated.
        iap_data (dict): A dictionary containing the updated details of the IAP. This should conform to
                        the structure required by the Google Play Developer API.

        Returns:
        dict: A dictionary containing the response from the API if the IAP is successfully updated.
        None: If the update fails, returns None.

        Raises:
        Exception: If the API request fails, raises an exception with a clear error message.
        """
        try:
            response = (
                self.service.inappproducts()
                .update(packageName=self.package_name, sku=iap_identifier, body=iap_data)
                .execute()
            )
            return response
        except Exception as e:
            raise Exception(f"Failed to update IAP '{iap_identifier}': {e}")

    def list_subscriptions(self):
        """
        Retrieve all subscriptions configured for the application using the monetization API,
        automatically handling pagination.

        Returns:
        list: A complete list of dictionaries, each containing details of a subscription.
        """
        all_subscriptions = []
        page_token = None
        try:
            while True:
                response = (
                    self.service.monetization()
                    .subscriptions()
                    .list(packageName=self.package_name, pageToken=page_token)
                    .execute()
                )
                subscriptions = response.get("subscriptions", [])
                all_subscriptions.extend(subscriptions)
                page_token = response.get("nextPageToken")
                if not page_token:
                    break
        except Exception as e:
            raise Exception(f"Error listing subscriptions: {e}")
        return all_subscriptions

    def get_subscription(self, subscription_identifier):
        """
        Retrieve the details of a specific subscription if it exists, using the monetization API.

        Parameters:
        subscription_identifier (str): The identifier of the subscription.

        Returns:
        dict: A dictionary containing the subscription details if found, None otherwise.
        """
        try:
            result = (
                self.service.monetization()
                .subscriptions()
                .get(packageName=self.package_name, productId=subscription_identifier)
                .execute()
            )
            return result
        except Exception as e:
            raise Exception(f"Error fetching subscription '{subscription_identifier}': {e}")

    def add_subscription(self, subscription_identifier, subscription_data):
        """
        Add a new subscription to the Google Play Store.

        Parameters:
        subscription_identifier (str): The identifier for the new subscription.
        subscription_data (dict): A dictionary containing the details of the subscription. This should conform to the
                                structure required by the Google Play Developer API.

        Returns:
        dict: A dictionary containing the response from the API if the subscription is successfully added.
        None: If the addition fails, returns None.

        Raises:
        Exception: If the API request fails, raises an exception with a clear error message.
        """
        try:
            response = (
                self.service.monetization()
                .subscriptions()
                .create(packageName=self.package_name, productId=subscription_identifier, body=subscription_data)
                .execute()
            )
            return response
        except Exception as e:
            raise Exception(f"Failed to add subscription '{subscription_identifier}': {e}")

    def update_subscription(self, subscription_identifier, subscription_data):
        """
        Update an existing subscription in the Google Play Store.

        Parameters:
        subscription_identifier (str): The identifier of the subscription to be updated.
        subscription_data (dict): A dictionary containing the updated details of the subscription. This should conform to
                                the structure required by the Google Play Developer API.

        Returns:
        dict: A dictionary containing the response from the API if the subscription is successfully updated.
        None: If the update fails, returns None.

        Raises:
        Exception: If the API request fails, raises an exception with a clear error message.
        """
        try:
            response = (
                self.service.monetization()
                .subscriptions()
                .update(packageName=self.package_name, productId=subscription_identifier, body=subscription_data)
                .execute()
            )
            return response
        except Exception as e:
            raise Exception(f"Failed to update subscription '{subscription_identifier}': {e}")

    def delete_subscription(self, subscription_identifier):
        """
        Delete a subscription from the Google Play Store.

        Parameters:
        subscription_identifier (str): The identifier of the subscription to be deleted.

        Returns:
        bool: True if the deletion was successful, False otherwise.

        Raises:
        Exception: If the API request fails, raises an exception with a clear error message.
        """
        try:
            self.service.monetization().subscriptions().delete(
                packageName=self.package_name, productId=subscription_identifier
            ).execute()
            return True
        except Exception as e:
            raise Exception(f"Failed to delete subscription '{subscription_identifier}': {e}")
