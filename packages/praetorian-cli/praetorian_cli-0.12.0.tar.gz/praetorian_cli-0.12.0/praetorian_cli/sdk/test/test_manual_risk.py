from praetorian_cli.sdk.test import BaseTest
from praetorian_cli.sdk.test.utils import Utils


class TestRisk(BaseTest):

    def setup_class(self):
        self.chariot, self.username = BaseTest.setup_chariot(self)
        self.seed = "contoso.com"
        self.name = "Foobar Finding"
        self.utils = Utils(self.chariot)

    def test_risk(self):
        self.utils.add_seed(self.seed)
        response = self.utils.wait_for_key(dict(key=f'#asset#{self.seed}'))
        assert response, "Received empty response for my Assets"

        self.chariot.add_risk(key=f'#asset#{self.seed}', name=self.name)
        my_risk = self.chariot.my(dict(key=f'#risk#{self.seed}'))
        assert my_risk is not None
        self.chariot.delete_asset(key=f'#seed#{self.seed}')
