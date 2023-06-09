import openai
import os
import logging

logging.basicConfig(level=logging.INFO)

class GPT_API:
    def __init__(self):
        """
        Initialize the API

        :return: None
        """
        self._api_key_file = "API\mdp.txt"
        self._api_organisation_file = "API\organisation.txt"
        self._api_key = self._load_api_key(self._api_key_file)
        self._api_organisation = self._load_api_organisation(self._api_organisation_file)

    def _load_api_key(self, api_key_file):
        """
        Load the API key from the file
        :param api_key_file: File to load the API key from
        :return: API key
        """
        with open(api_key_file, "r") as file:
            api_key = file.read().strip()
        return api_key

    def _load_api_organisation(self, self_organisation_file):
        """
        Load the API organisation from the file
        :param self_organisation_file: File to load the API organisation from
        :return: API organisation
        """
        with open(self_organisation_file, "r") as file:
            api_organisation = file.read().strip()
        return api_organisation

    def init_api(self):
        """
        Initialize the API
        :return: None
        """
        try:
            openai.api_key = self._api_key
            openai.organization = self._api_organisation
            logging.info("API connect...")
        except Exception as e:
            raise ValueError("\nError initializing API: " + str(e))