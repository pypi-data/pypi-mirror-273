from tests import IntegrationTest

class TestDBCreation(IntegrationTest):

    def test_db_creation(self):
        _json = self.get_instruments()
        
        assert _json['instruments'][0]['id'] == self.instru1_id
        assert _json['instruments'][0]['name'] == self.INSTRU1
        assert _json['instruments'][1]['id'] == self.instru2_id
        assert _json['instruments'][1]['name'] == self.INSTRU2
        assert _json['instruments'][2]['id'] == self.instru3_id
        assert _json['instruments'][2]['name'] == self.INSTRU3
