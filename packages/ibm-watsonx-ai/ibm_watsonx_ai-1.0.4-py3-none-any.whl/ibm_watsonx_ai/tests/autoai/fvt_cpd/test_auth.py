#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

import os
import copy
import unittest

from requests.exceptions import ProxyError

from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.experiment import AutoAI
from ibm_watsonx_ai._wrappers import requests

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.tests.utils import get_wml_credentials, is_cp4d
from ibm_watsonx_ai.wml_client_error import WMLClientError, CannotAutogenerateBedrockUrl
from ibm_watsonx_ai.messages.messages import Messages


@unittest.skipIf(not is_cp4d(), "Not supported on cloud")
class TestAutoAIRemote(unittest.TestCase):
    """
    The test can be run on CPD
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

    def test_01_missing_version(self):
        credentials = copy.copy(self.credentials)

        credentials.version = None
        client = APIClient(credentials=credentials)

        self.assertTrue(
            client.CPD_version == float(client.CPD_version.supported_version_list[-1])
        )

    def test_01a_missing_version_in_AutoAI(self):
        credentials = copy.copy(self.credentials)

        credentials.version = None
        autoai = AutoAI(
            credentials=credentials, project_id=credentials.get("project_id")
        )

        self.assertTrue(autoai, "AutoAI object is not initialised correctly")

    def test_02_missing_url(self):
        url_not_provided_error_message = "`url` is not provided."
        credentials = copy.copy(self.credentials)
        credentials.url = None

        with self.assertRaises(WMLClientError) as context:
            APIClient(credentials=credentials)

        self.assertTrue(url_not_provided_error_message in context.exception.error_msg)

    def test_03_missing_instance_id(self):
        url_is_not_valid_error_message = 'The specified url is not valid. To authenticate with your Cloud Pak for Data installed software, add `"instance_id": "openshift"` to your credentials. To authenticate with your Cloud Pak for Data as a Service account, see https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/ml-authentication.html .'
        credentials = copy.copy(self.credentials)
        credentials.instance_id = None

        with self.assertRaises(WMLClientError) as context:
            APIClient(credentials=credentials)

        self.assertTrue(url_is_not_valid_error_message in context.exception.error_msg)

    def test_04_invalid_version(self):
        credentials = copy.copy(self.credentials)
        credentials.version = "banana"
        message = WMLClientError(
            Messages.get_message(
                credentials.version,
                APIClient.version,
                message_id="invalid_version_from_automated_check",
            )
        )

        with self.assertRaises(WMLClientError) as context:
            APIClient(credentials=credentials)

        self.assertTrue(str(message) in context.exception.error_msg)

    def test_05_invalid_url(self):
        url_syntax_error_message = "`url` must start with `https://`."
        credentials = copy.copy(self.credentials)
        credentials.url = "banana"

        with self.assertRaises(WMLClientError) as context:
            APIClient(credentials=credentials)

        self.assertTrue(url_syntax_error_message in context.exception.error_msg)

    def test_06_invalid_instance_id(self):
        invalid_instance_id_error_message = 'Invalid instance_id for Cloud Pak for Data. Use `"instance_id": "openshift"` in your credentials. To authenticate with a different offering, refer to the product documentation for authentication details.'
        credentials = copy.copy(self.credentials)
        credentials.instance_id = "banana"

        with self.assertRaises(WMLClientError) as context:
            APIClient(credentials=credentials)

        self.assertTrue(
            invalid_instance_id_error_message in context.exception.error_msg
        )

    def test_username_password_auth_scenario_01_correct(self):
        credentials = Credentials.from_dict(
            {
                "instance_id": self.credentials.instance_id,
                "url": self.credentials.url,
                "version": self.credentials.version,
                "username": self.credentials.username,
                "password": self.credentials.password,
            }
        )
        APIClient(credentials=credentials)

    def test_username_password_auth_scenario_02_missing_password(self):
        password_is_missing_error_message = "`password` missing in credentials."
        credentials = Credentials.from_dict(
            {
                "instance_id": self.credentials.instance_id,
                "url": self.credentials.url,
                "version": self.credentials.version,
                "username": self.credentials.username,
            }
        )

        with self.assertRaises(WMLClientError) as context:
            APIClient(credentials=credentials)

        self.assertTrue(
            password_is_missing_error_message in context.exception.error_msg
        )

    def test_username_password_auth_scenario_03_missing_username(self):
        username_is_missing_error_message = "`username` missing in credentials."
        credentials = Credentials.from_dict(
            {
                "instance_id": self.credentials.instance_id,
                "url": self.credentials.url,
                "version": self.credentials.version,
                "password": self.credentials.password,
            }
        )

        with self.assertRaises(CannotAutogenerateBedrockUrl) as context:
            APIClient(credentials=credentials)

        self.assertTrue(
            username_is_missing_error_message in context.exception.args[0].error_msg
        )

    def test_username_apikey_auth_scenario_01_correct(self):
        if self.credentials.api_key is None:
            self.skipTest("No apikey in creds")

        credentials = Credentials.from_dict(
            {
                "instance_id": self.credentials.instance_id,
                "url": self.credentials.url,
                "version": self.credentials.version,
                "username": self.credentials.username,
                "apikey": self.credentials.api_key,
            }
        )
        APIClient(credentials=credentials)

    def test_username_apikey_auth_scenario_02_invalid_apikey_key(self):
        if self.credentials.api_key is None:
            self.skipTest("No apikey in creds")

        credentials = Credentials.from_dict(
            {
                "instance_id": self.credentials.instance_id,
                "url": self.credentials.url,
                "version": self.credentials.version,
                "username": self.credentials.username,
                "apikey": self.credentials.api_key,
            }
        )
        APIClient(credentials=credentials)

    def test_username_apikey_auth_scenario_03_url_in_env_variables(self):
        if self.credentials.api_key is None:
            self.skipTest("No apikey in creds")

        os.environ["RUNTIME_ENV_APSX_URL"] = self.credentials.url

        credentials = Credentials.from_dict(
            {
                "instance_id": self.credentials.instance_id,
                "version": self.credentials.version,
                "username": self.credentials.username,
                "apikey": self.credentials.api_key,
            }
        )
        APIClient(credentials=credentials)

    def test_token_auth_scenario_01_correct(self):
        credentials = Credentials.from_dict(
            {
                "instance_id": self.credentials.instance_id,
                "url": self.credentials.url,
                "version": self.credentials.version,
                "token": self.token,
            }
        )
        APIClient(credentials=credentials)

    def test_token_auth_scenario_02_missing_token(self):
        username_is_missing_error_message = "`username` missing in credentials."
        credentials = Credentials.from_dict(
            {
                "instance_id": self.credentials.instance_id,
                "url": self.credentials.url,
                "version": self.credentials.version,
            }
        )

        with self.assertRaises(WMLClientError) as context:
            APIClient(credentials=credentials)

        self.assertTrue(
            username_is_missing_error_message in context.exception.error_msg
        )

    def test_token_auth_scenario_03_token_with_bearer_prefix(self):
        os.environ["USER_ACCESS_TOKEN"] = "Bearer " + self.token

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
            del os.environ["USER_ACCESS_TOKEN"]

    def test_project_id_auth_scenario_01_correct_char_key(self):
        project_id_syntax_error_message = "`project_id` parameter contains bad syntax!"
        project_id_special_characters_error_message = (
            "`project_id` parameter can not contain special characters in blocks!"
        )
        credentials = copy.copy(self.credentials)
        project_id = credentials.__dict__.get("project_id")

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
        credentials = Credentials.from_dict(
            {
                "instance_id": self.credentials.instance_id,
                "url": self.credentials.url,
                "version": self.credentials.version,
                "username": self.credentials.username,
                "password": self.credentials.password,
                "proxies": "banana",
            }
        )

        try:

            with self.assertRaises(AttributeError) as context:
                APIClient(credentials=credentials)

            self.assertTrue(error_message in context.exception.args[0])
        finally:
            requests.additional_settings = {}

    def test_proxies_scenario_02_non_existing_proxies(self):
        credentials = Credentials.from_dict(
            {
                "instance_id": self.credentials.instance_id,
                "url": self.credentials.url,
                "version": self.credentials.version,
                "username": self.credentials.username,
                "password": self.credentials.password,
                "proxies": {
                    "http": "http://non.existing.url.ibm.com/",
                    "https": "http://non.existing.url.ibm.com/",
                },
            }
        )

        try:
            with self.assertRaises((ProxyError, OSError)):
                APIClient(credentials=credentials)
        finally:
            requests.additional_settings = {}

    def test_verify_01_bool_verify_written_to_env_var(self):

        if os.environ.get("WX_CLIENT_VERIFY_REQUESTS") is not None:
            del os.environ["WX_CLIENT_VERIFY_REQUESTS"]

        credentials = Credentials.from_dict(
            {
                "instance_id": self.credentials.instance_id,
                "url": self.credentials.url,
                "version": self.credentials.version,
                "username": self.credentials.username,
                "password": self.credentials.password,
                "verify": False,
            },
        )

        APIClient(credentials=credentials)

        self.assertTrue(os.environ.get("WX_CLIENT_VERIFY_REQUESTS") is not None)
        self.assertTrue(os.environ.get("WX_CLIENT_VERIFY_REQUESTS") == "False")

    def test_verify_02_bool_verify_written_to_env_var_2(self):

        if os.environ.get("WX_CLIENT_VERIFY_REQUESTS") is not None:
            del os.environ["WX_CLIENT_VERIFY_REQUESTS"]

        credentials = Credentials.from_dict(
            {
                "instance_id": self.credentials.instance_id,
                "url": self.credentials.url,
                "version": self.credentials.version,
                "username": self.credentials.username,
                "password": self.credentials.password,
                "verify": True,
            },
        )

        APIClient(credentials=credentials)

        self.assertTrue(os.environ.get("WX_CLIENT_VERIFY_REQUESTS") is not None)
        self.assertTrue(os.environ.get("WX_CLIENT_VERIFY_REQUESTS") == "True")

    def test_verify_03_str_verify_written_to_env_var(self):

        if os.environ.get("WX_CLIENT_VERIFY_REQUESTS") is not None:
            del os.environ["WX_CLIENT_VERIFY_REQUESTS"]

        credentials = Credentials.from_dict(
            {
                "instance_id": self.credentials.instance_id,
                "url": self.credentials.url,
                "version": self.credentials.version,
                "username": self.credentials.username,
                "password": self.credentials.password,
                "verify": "tmp.txt",
            },
        )

        client = APIClient(credentials=credentials)

        self.assertTrue(os.environ.get("WX_CLIENT_VERIFY_REQUESTS") is not None)
        self.assertTrue(os.environ.get("WX_CLIENT_VERIFY_REQUESTS") == "tmp.txt")
        self.assertTrue(client.credentials.verify == True)

    def test_verify_04_bool_verify_written_to_credentials(self):

        os.environ["WX_CLIENT_VERIFY_REQUESTS"] = "False"

        credentials = Credentials.from_dict(
            {
                "instance_id": self.credentials.instance_id,
                "url": self.credentials.url,
                "version": self.credentials.version,
                "username": self.credentials.username,
                "password": self.credentials.password,
            },
        )

        client = APIClient(credentials=credentials)

        self.assertTrue(client.credentials.verify == False)
        self.assertTrue(os.environ["WX_CLIENT_VERIFY_REQUESTS"] == "False")

    def test_verify_05_bool_verify_written_to_credentials_2(self):

        os.environ["WX_CLIENT_VERIFY_REQUESTS"] = "True"

        credentials = Credentials.from_dict(
            {
                "instance_id": self.credentials.instance_id,
                "url": self.credentials.url,
                "version": self.credentials.version,
                "username": self.credentials.username,
                "password": self.credentials.password,
            },
        )

        client = APIClient(credentials=credentials)

        self.assertTrue(client.credentials.verify == True)
        self.assertTrue(os.environ["WX_CLIENT_VERIFY_REQUESTS"] == "True")

    def test_verify_06_str_verify_written_to_credentials(self):

        os.environ["WX_CLIENT_VERIFY_REQUESTS"] = "tmp.txt"

        credentials = Credentials.from_dict(
            {
                "instance_id": self.credentials.instance_id,
                "url": self.credentials.url,
                "version": self.credentials.version,
                "username": self.credentials.username,
                "password": self.credentials.password,
            },
        )

        client = APIClient(credentials=credentials)

        self.assertTrue(client.credentials.verify == True)
        self.assertTrue(os.environ["WX_CLIENT_VERIFY_REQUESTS"] == "tmp.txt")

    def test_verify_07_empty_str_env_verify_fixed_by_credentials(self):

        os.environ["WX_CLIENT_VERIFY_REQUESTS"] = ""

        credentials = Credentials.from_dict(
            {
                "instance_id": self.credentials.instance_id,
                "url": self.credentials.url,
                "version": self.credentials.version,
                "username": self.credentials.username,
                "password": self.credentials.password,
                "verify": "True",
            },
        )

        client = APIClient(credentials=credentials)

        self.assertTrue(client.credentials.verify == True)
        self.assertTrue(os.environ["WX_CLIENT_VERIFY_REQUESTS"] == "True")

    def test_verify_08_empty_verify(self):

        os.environ["WX_CLIENT_VERIFY_REQUESTS"] = ""

        credentials = Credentials.from_dict(
            {
                "instance_id": self.credentials.instance_id,
                "url": self.credentials.url,
                "version": self.credentials.version,
                "username": self.credentials.username,
                "password": self.credentials.password,
            },
        )

        client = APIClient(credentials=credentials)

        self.assertTrue(client.credentials.verify is None)
        self.assertTrue(os.environ["WX_CLIENT_VERIFY_REQUESTS"] == "")

    def test_flight_01_set_env_vars_from_credentials(self):

        if os.environ.get("FLIGHT_SERVICE_LOCATION") is not None:
            del os.environ["FLIGHT_SERVICE_LOCATION"]

        if os.environ.get("FLIGHT_SERVICE_PORT") is not None:
            del os.environ["FLIGHT_SERVICE_PORT"]

        credentials = Credentials.from_dict(
            {
                "instance_id": self.credentials.instance_id,
                "url": self.credentials.url,
                "version": self.credentials.version,
                "username": self.credentials.username,
                "password": self.credentials.password,
                "flight_service_location": "test_location.com",
                "flight_service_port": 111,
            },
        )

        try:
            APIClient(credentials=credentials)

            self.assertTrue(
                os.environ["FLIGHT_SERVICE_LOCATION"] == "test_location.com"
            )
            self.assertTrue(os.environ["FLIGHT_SERVICE_PORT"] == "111")
        finally:
            if os.environ.get("FLIGHT_SERVICE_LOCATION") is not None:
                del os.environ["FLIGHT_SERVICE_LOCATION"]

            if os.environ.get("FLIGHT_SERVICE_PORT") is not None:
                del os.environ["FLIGHT_SERVICE_PORT"]


if __name__ == "__main__":
    unittest.main()
