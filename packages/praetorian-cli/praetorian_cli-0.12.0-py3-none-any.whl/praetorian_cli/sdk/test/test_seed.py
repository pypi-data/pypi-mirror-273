import pytest

from praetorian_cli.sdk.test import BaseTest
from praetorian_cli.sdk.test.utils import Utils, threshold


@pytest.fixture(scope="class", params=["contoso.com", "1.1.1.1/32"])
def seed(request):
    request.cls.seed = request.param


@pytest.mark.usefixtures("seed")
class TestSeed(BaseTest):

    def setup_class(self):
        self.chariot, self.username = BaseTest.setup_chariot(self)
        self.utils = Utils(self.chariot)

    def test_add_seed(self):
        response = self.utils.add_seed(self.seed)
        assert response['seed'] == self.seed, "Response does not have correct seed"
        assert response['status'] == "AA"

    def test_my_seed(self):
        response = self.chariot.my(dict(key=f'#seed#{self.seed}'))
        for my_seed in response['seeds']:
            assert my_seed['username'] == self.username, f"Seed did not have username = {self.username}"
            assert my_seed['seed'] in self.seed

    def test_my_job(self):
        response = self.utils.wait_for_key(dict(key=f'#job#{self.seed}'))
        assert response is not None, "Received empty response for my Jobs"
        for job in response['jobs']:
            assert job['source'] is not '', "Job Capability is empty"
            assert job['status'] is not None, "Job Status is empty"

    def test_my_asset(self):
        response = self.utils.wait_for_key(dict(key=f'#asset#{self.seed}'))
        assert response is not None, "Received empty response for my Assets"
        for asset in response['assets']:
            assert asset['seed'] == self.seed, "Seed is empty"
            assert asset['name'] or asset['dns'], "Asset fields IP and DNS are both empty"

    def test_delete_seed(self):
        self.chariot.delete_asset(key=f'#seed#{self.seed}')
        response = self.chariot.my(dict(key=f'#seed#{self.seed}'))
        assert response == {}
