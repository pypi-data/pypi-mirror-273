#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

import os
import copy
import unittest

from requests.exceptions import ProxyError

from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai._wrappers import requests

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.tests.utils import get_wml_credentials, is_cp4d
from ibm_watsonx_ai.wml_client_error import WMLClientError


@unittest.skipIf(is_cp4d(), "Not supported on ICP")
class TestAutoAIRemote(unittest.TestCase):
    """
    The test can be run on CLOUD
    """

    incorrect_version_error_message = "The version was recognized incorrectly."
    version_not_recognized_error_message = "The version was not recognized."

    credentials: Credentials
    token: str

    @classmethod
    def setUpClass(cls) -> None:
        """
        Load WML credentials from config.ini file based on ENV variable.
        """
        cls.credentials = get_wml_credentials()
        api_client = APIClient(credentials=cls.credentials)
        cls.token = api_client.token

    def test_01_missing_url(self):
        url_not_provided_error_message = "`url` is not provided."
        credentials = copy.copy(self.credentials)
        credentials.url = None

        with self.assertRaises(WMLClientError) as context:
            APIClient(credentials=credentials)

        self.assertTrue(url_not_provided_error_message in context.exception.error_msg)

    def test_02_invalid_url(self):
        url_syntax_error_message = "`url` must start with `https://`."
        credentials = copy.copy(self.credentials)
        credentials.url = "banana"

        with self.assertRaises(WMLClientError) as context:
            APIClient(credentials=credentials)

        self.assertTrue(url_syntax_error_message in context.exception.error_msg)

    def test_apikey_auth_scenario_01_correct(self):
        credentials = Credentials(
            url=self.credentials.url,
            api_key=self.credentials.api_key,
        )

        APIClient(credentials=credentials)

    def test_apikey_auth_scenario_02_invalid_apikey_key(self):
        error_message = "Error getting IAM Token."
        credentials = Credentials(url=self.credentials.url, api_key="banana")

        with self.assertRaises(WMLClientError) as context:
            APIClient(credentials=credentials)

        self.assertTrue(error_message in context.exception.error_msg)

    def test_apikey_auth_scenario_03_url_in_env_variables(self):
        os.environ["RUNTIME_ENV_APSX_URL"] = self.credentials.url

        credentials = Credentials(api_key=self.credentials.api_key)

        APIClient(credentials=credentials)

    def test_token_auth_scenario_01_correct(self):
        credentials = Credentials(url=self.credentials.url, token=self.token)

        APIClient(credentials=credentials)

    def test_token_auth_scenario_02_missing_token(self):
        username_is_missing_error_message = (
            "`api_key` for IAM token is not provided in credentials for the client"
        )
        credentials = Credentials(url=self.credentials.url)

        with self.assertRaises(WMLClientError) as context:
            APIClient(credentials=credentials)

        self.assertTrue(
            username_is_missing_error_message in context.exception.error_msg
        )

    def test_token_auth_scenario_03_token_with_bearer_prefix(self):
        os.environ['USER_ACCESS_TOKEN'] = "Bearer " + self.token

        credentials = Credentials.from_dict(
            {
                "instance_id": self.credentials.instance_id,
                "url": self.credentials.url,
                "version": self.credentials.version,
            }
        )

        try:
            client = APIClient(credentials=credentials)

            self.assertIsNotNone(client.token)
            self.assertTrue("Bearer " not in client.token)
            self.assertTrue(client.token == self.token)

        finally:
            del os.environ['USER_ACCESS_TOKEN']

    def test_project_id_auth_scenario_01_correct_char_key(self):
        project_id_syntax_error_message = "`project_id` parameter contains bad syntax!"
        project_id_special_characters_error_message = (
            "`project_id` parameter can not contain special characters in blocks!"
        )
        credentials = copy.copy(self.credentials)
        project_id = credentials.__dict__.get('project_id')

        first_block = str(project_id[:7]).isalnum()
        second_block = str(project_id[9:12]).isalnum()
        third_block = str(project_id[14:17]).isalnum()
        fourth_block = str(project_id[19:22]).isalnum()
        fifth_block = str(project_id[24:]).isalnum()

        self.assertTrue(
            project_id[8]
            and project_id[13]
            and project_id[18]
            and project_id[23] == "-",
            project_id_syntax_error_message,
        )
        self.assertTrue(
            first_block
            and second_block
            and third_block
            and fourth_block
            and fifth_block,
            project_id_special_characters_error_message,
        )

        APIClient(credentials=credentials)

    def test_proxies_scenario_01_invalid_type_proxies(self):
        error_message = "'str' object has no attribute 'get'"
        credentials = Credentials(
            url=self.credentials.url,
            api_key=self.credentials.api_key,
            proxies="banana",
        )

        try:

            with self.assertRaises(AttributeError) as context:
                APIClient(credentials=credentials)

            self.assertTrue(error_message in context.exception.args[0])
        finally:
            requests.additional_settings = {}

    def test_proxies_scenario_02_non_existing_proxies(self):
        credentials = Credentials(
            url=self.credentials.url,
            api_key=self.credentials.api_key,
            proxies={
                "http": "http://non.existing.url.ibm.com/",
                "https": "http://non.existing.url.ibm.com/",
            },
        )

        try:
            with self.assertRaises(ProxyError):
                APIClient(credentials=credentials)

        finally:
            requests.additional_settings = {}

    def test_verify_01_bool_verify_written_to_env_var(self):

        if os.environ.get("WX_CLIENT_VERIFY_REQUESTS") is not None:
            del os.environ["WX_CLIENT_VERIFY_REQUESTS"]

        credentials = Credentials(
            url=self.credentials.url, api_key=self.credentials.api_key, verify=False
        )

        APIClient(credentials=credentials)

        self.assertTrue(os.environ.get("WX_CLIENT_VERIFY_REQUESTS") is not None)
        self.assertTrue(os.environ.get("WX_CLIENT_VERIFY_REQUESTS") == "False")

    def test_verify_02_bool_verify_written_to_env_var_2(self):

        if os.environ.get("WX_CLIENT_VERIFY_REQUESTS") is not None:
            del os.environ["WX_CLIENT_VERIFY_REQUESTS"]

        credentials = Credentials(
            url=self.credentials.url, api_key=self.credentials.api_key, verify=True
        )

        APIClient(credentials=credentials)

        self.assertTrue(os.environ.get("WX_CLIENT_VERIFY_REQUESTS") is not None)
        self.assertTrue(os.environ.get("WX_CLIENT_VERIFY_REQUESTS") == "True")

    def test_verify_03_str_verify_written_to_env_var(self):

        if os.environ.get("WX_CLIENT_VERIFY_REQUESTS") is not None:
            del os.environ["WX_CLIENT_VERIFY_REQUESTS"]

        credentials = Credentials(
            url=self.credentials.url, api_key=self.credentials.api_key, verify="tmp.txt"
        )

        client = APIClient(credentials=credentials)

        self.assertTrue(os.environ.get("WX_CLIENT_VERIFY_REQUESTS") is not None)
        self.assertTrue(os.environ.get("WX_CLIENT_VERIFY_REQUESTS") == "tmp.txt")
        self.assertTrue(client.credentials.verify == True)

    def test_verify_04_bool_verify_written_to_credentials(self):

        os.environ["WX_CLIENT_VERIFY_REQUESTS"] = "False"

        credentials = Credentials(
            url=self.credentials.url,
            api_key=self.credentials.api_key,
        )

        client = APIClient(credentials=credentials)

        self.assertTrue(client.credentials.verify == False)
        self.assertTrue(os.environ["WX_CLIENT_VERIFY_REQUESTS"] == "False")

    def test_verify_05_bool_verify_written_to_credentials_2(self):

        os.environ["WX_CLIENT_VERIFY_REQUESTS"] = "True"

        credentials = Credentials(
            url=self.credentials.url,
            api_key=self.credentials.api_key,
        )

        client = APIClient(credentials=credentials)

        self.assertTrue(client.credentials.verify == True)
        self.assertTrue(os.environ["WX_CLIENT_VERIFY_REQUESTS"] == "True")

    def test_verify_06_str_verify_written_to_credentials(self):

        os.environ["WX_CLIENT_VERIFY_REQUESTS"] = "tmp.txt"

        credentials = Credentials(
            url=self.credentials.url,
            api_key=self.credentials.api_key,
        )

        client = APIClient(credentials=credentials)

        self.assertTrue(client.credentials.verify == True)
        self.assertTrue(os.environ["WX_CLIENT_VERIFY_REQUESTS"] == "tmp.txt")

    def test_verify_07_empty_str_env_verify_fixed_by_credentials(self):

        os.environ["WX_CLIENT_VERIFY_REQUESTS"] = ""

        credentials = Credentials(
            url=self.credentials.url,
            api_key=self.credentials.api_key,
            verify="True",
        )

        client = APIClient(credentials=credentials)

        self.assertTrue(client.credentials.verify == True)
        self.assertTrue(os.environ["WX_CLIENT_VERIFY_REQUESTS"] == "True")

    def test_verify_08_empty_verify(self):

        os.environ["WX_CLIENT_VERIFY_REQUESTS"] = ""

        credentials = Credentials(
            url=self.credentials.url,
            api_key=self.credentials.api_key,
        )

        client = APIClient(credentials=credentials)

        self.assertTrue(client.credentials.verify is None)
        self.assertTrue(os.environ["WX_CLIENT_VERIFY_REQUESTS"] == "")

    def test_flight_01_set_env_vars_from_credentials(self):

        if os.environ.get('FLIGHT_SERVICE_LOCATION') is not None:
            del os.environ['FLIGHT_SERVICE_LOCATION']

        if os.environ.get('FLIGHT_SERVICE_PORT') is not None:
            del os.environ['FLIGHT_SERVICE_PORT']

        credentials = Credentials.from_dict(
            {
                "url": self.credentials.url,
                "apikey": self.credentials.api_key,
                "flight_service_location": "test_location.com",
                "flight_service_port": 111
            },
        )

        try:
            APIClient(credentials=credentials)

            self.assertTrue(os.environ['FLIGHT_SERVICE_LOCATION'] == "test_location.com")
            self.assertTrue(os.environ['FLIGHT_SERVICE_PORT'] == "111")
        finally:
            if os.environ.get('FLIGHT_SERVICE_LOCATION') is not None:
                del os.environ['FLIGHT_SERVICE_LOCATION']

            if os.environ.get('FLIGHT_SERVICE_PORT') is not None:
                del os.environ['FLIGHT_SERVICE_PORT']


if __name__ == "__main__":
    unittest.main()
