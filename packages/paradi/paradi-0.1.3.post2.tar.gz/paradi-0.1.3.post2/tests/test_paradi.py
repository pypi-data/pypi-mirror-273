# %% imports
import pytest
import requests
import json
import os
from paradi.paradi import Paradi
from dotenv import load_dotenv


# %% constants
load_dotenv()
with open("http.json", "r") as f:
    http_dict = json.load(f)


# %% fixtures
@pytest.fixture
def test_paradi_instance():
    class TestParadiClass(Paradi):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        def _save_auth(self,
                       response: requests.Response
                       ):
            if response.status_code == 200:
                self.auth = {"auth_saved": True}

    return TestParadiClass(entry=f"http://{os.getenv('TEST_SERVER_HOSTNAME')}:{os.getenv('TEST_SERVER_PORT')}",
                           login_uri="",
                           logout_uri="",
                           login_kwargs={})


# %% Tests
class TestParadi:
    def test_instantiate(self):
        with pytest.raises(TypeError):
            Paradi.__new__(Paradi)

    def test__request(self,
                      test_paradi_instance):
        with pytest.raises(AttributeError):
            test_paradi_instance.__request("GET", "200")

    def test_get(self,
                 test_paradi_instance):
        assert isinstance(test_paradi_instance.get("http/200"), requests.Response)
        for status_code, message in http_dict.items():
            if 200 <= int(status_code) < 300:
                assert test_paradi_instance.get(f"http/{status_code}").status_code == int(status_code)
            else:
                with pytest.raises(Exception):
                    test_paradi_instance.get(f"http/{status_code}")

    def test_post(self,
                  test_paradi_instance):
        test_request = test_paradi_instance.post("post/data")
        assert isinstance(test_request, requests.Response)
        assert test_request.status_code == 200

    def test__save_auth(self,
                        test_paradi_instance):
        response = test_paradi_instance.post("post/data")
        test_paradi_instance._save_auth(response=response)
        assert test_paradi_instance.auth is not None
