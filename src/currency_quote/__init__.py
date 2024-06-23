from config.endpoints import API
from api_to_dataframe import ClientBuilder, RetryStrategies


class CurrencyQuote:
    def __init__(self, currency_code: list):
        self.currency_code = currency_code

    def _validate_currency_code(self):
        client = ClientBuilder(
            endpoint=API.ENDPOINT_AVALIABLE_PARITIES,
            retry_strategy=RetryStrategies.LinearRetryStrategy
        )

        valid_list = client.get_api_data

        validated_list = []

        for currency_code in self.currency_code:
            if currency_code in valid_list:
                validated_list = validated_list.append(currency_code, ignore_index=True)

        return validated_list

    def get_last_quote(self):
        url = API.ENDPOINT_AVALIABLE_PARITIES + self._validate_currency_code()
        client = ClientBuilder(
            endpoint=url,
            retry_strategy=RetryStrategies.ExponentialRetryStrategy
        )

        response = client.get_api_data()

        return response

    def get_history_quote(self, reference_date: int):
        """
        Title: get_history_quote
        params: reference_date (int)
        example: 20240526

        returns: the json data with quote of reference_date

        """
        url = \
            (f"{API.ENDPOINT_HISTORY_COTATION}"
             f"{self._validate_currency_code()}"
             f"/?start_date={reference_date}&end_date={reference_date}")

        client = ClientBuilder(
            endpoint=url,
            retry_strategy=RetryStrategies.ExponentialRetryStrategy
        )

        response = client.get_api_data()

        return response