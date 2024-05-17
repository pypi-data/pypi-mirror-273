from tests import IntegrationTest

class TestGetInstruments(IntegrationTest):

    def setUp(self):
        super().setUp()

    def test_get_instruments(self):            
        _json = self.get_instruments()
        assert len(_json['instruments']) >= 3
        assert self.INSTRU1 in [i['name'] for i in _json['instruments']]
        assert self.INSTRU2 in [i['name'] for i in _json['instruments']]
        assert self.INSTRU3 in [i['name'] for i in _json['instruments']]

