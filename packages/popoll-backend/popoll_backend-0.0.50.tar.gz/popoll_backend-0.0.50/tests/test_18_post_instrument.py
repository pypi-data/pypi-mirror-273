from tests import IntegrationTest

class TestGetInstruments(IntegrationTest):

    def setUp(self):
        super().setUp()

    def test_add_instruments(self):            
        _json = self.get_instruments()
        assert len(_json['instruments']) == 3
        self.create_instrument('INSTR4')
        _json = self.get_instruments()
        assert len(_json['instruments']) == 4
        assert 'INSTR4' == _json['instruments'][3]['name']

