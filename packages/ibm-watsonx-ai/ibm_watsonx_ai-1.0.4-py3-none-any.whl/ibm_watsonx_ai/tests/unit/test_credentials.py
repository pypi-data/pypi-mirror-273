#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------
import pytest

from ibm_watsonx_ai import Credentials


@pytest.mark.unittest
class TestCredentials:
    """
    These tests cover:
    - getting the attribute directly
    - method get
    - method __getitem__
    - method from_dict
    - method to_dict
    """

    def test_getters_valid(self) -> None:
        url = "testing-credentials.com"
        credentials = Credentials(url=url)

        assert credentials.url == url, "Invalid url initialized"
        assert credentials["url"] == url, "Invalid url initialized"
        assert credentials.get("url") == url, "Invalid url initialized"

    def test_getters_no_key(self) -> None:
        credentials = Credentials(url="testing-credentials.com")

        assert credentials.api_key is None, "Invalid attribute initialized"
        assert credentials.get("api_key") is None, "Invalid attribute initialized"
        with pytest.raises(KeyError) as e:
            _ = credentials["api_key"]

        assert str(e.value) == "'api_key'", "No exception for invalid attribute"

    def test_getters_apikey(self) -> None:
        credentials = Credentials(api_key="aaaa-bbbb")

        assert credentials["api_key"] == "aaaa-bbbb", "Invalid apikey"
        assert credentials["apikey"] == "aaaa-bbbb", "Invalid apikey"
        assert credentials.get("apikey") == "aaaa-bbbb", "Invalid apikey"
        assert credentials.get("api_key") == "aaaa-bbbb", "Invalid apikey"

    def test_getters_apikey_non_existing(self) -> None:
        credentials = Credentials(url="testing-credentials.com")

        with pytest.raises(KeyError):
            credentials["api_key"]

        with pytest.raises(KeyError):
            credentials["apikey"]

    def test_get_return_default(self) -> None:
        url = "testing-credentials.com"
        credentials = Credentials(url=url)

        assert credentials.get("api_key", {}) == {}, "Invalid default returned"
        assert credentials.get("api_key", "abcd") == "abcd", "Invalid default returned"
        assert credentials.get("api_key") is None, "Invalid default returned"

        assert credentials.get("apikey", {}) == {}, "Invalid default returned"
        assert credentials.get("apikey", "abcd") == "abcd", "Invalid default returned"
        assert credentials.get("apikey") is None, "Invalid default returned"

    def test_from_dict(self) -> None:
        credentials = Credentials.from_dict({"url": "abcd-test.com"})

        assert isinstance(credentials, Credentials), "Not instance of `Credentials`"
        assert credentials.url == "abcd-test.com", "Invalid attribute initialized"
        assert credentials["url"] == "abcd-test.com", "Invalid attribute initialized"
        assert credentials.api_key is None, "Invalid attribute initialized"

    def test_to_dict_simple(self) -> None:
        exp_creds = {"url": "abcd-test.com", "username": "user-random"}
        credentials = Credentials.from_dict(exp_creds)

        assert credentials.to_dict() == exp_creds, "Invalid dict returned"

    def test_to_dict_instance_id(self) -> None:
        exp_creds = {
            "url": "abcd-test.com",
            "instance_id": "icp",
        }
        credentials = Credentials.from_dict(exp_creds)

        assert credentials.to_dict() == exp_creds, "Invalid dict returned"

    def test_to_dict_instance_id_invalid(self) -> None:
        credentials = Credentials(url="abcd-test.com", instance_id="invalid")

        assert credentials.to_dict() == {
            "url": "abcd-test.com"
        }, "`instance_id` in credetials"
