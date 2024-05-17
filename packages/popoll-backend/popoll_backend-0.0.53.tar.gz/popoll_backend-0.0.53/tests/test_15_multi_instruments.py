from tests import IntegrationTest

def _test_instru(expected_id, expected_name, isMain, actual):
        assert expected_id == actual['id']
        assert expected_name == actual['name']
        # assert isMain == actual['is_main']

class TestMultiInstruments(IntegrationTest):

    def setUp(self):
        super().setUp()
        self.user1_id = self.create_user('user1', self.instru1_id, [self.instru2_id])
        self.date1_id = self.create_date(date='2025-03-10', time='15:00:00', title='firstDate', end_time=None)
        self.answer1_id = self.create_answer(user_id=self.user1_id, date_id=self.date1_id)
        _json = self.get_user(self.user1_id)
        _test_instru(self.instru1_id, self.INSTRU1, True, _json['user']['main_instrument'])
        instruments = _json['user']['instruments']
        assert len(instruments) == 1
        _test_instru(self.instru2_id, self.INSTRU2, False, instruments[0])
        
    def test_multi_instruments_update_add(self):
        user1_id = self.update_user(self.user1_id, 'updatedUser1', self.instru1_id, [self.instru2_id, self.instru3_id])
        assert user1_id == self.user1_id
        _json = self.get_user(self.user1_id)
        _test_instru(self.instru1_id, self.INSTRU1, True, _json['user']['main_instrument'])
        instruments = _json['user']['instruments']
        assert len(instruments) == 2
        _test_instru(self.instru2_id, self.INSTRU2, False, instruments[0])
        _test_instru(self.instru3_id, self.INSTRU3, False, instruments[1])

    def test_multi_instruments_update_move(self):
        user1_id = self.update_user(self.user1_id, 'updatedUser1', self.instru2_id, [self.instru1_id])
        assert user1_id == self.user1_id
        _json = self.get_user(self.user1_id)
        _test_instru(self.instru2_id, self.INSTRU2, True, _json['user']['main_instrument'])
        assert len(_json['user']['instruments']) == 1
        _test_instru(self.instru1_id, self.INSTRU1, False, _json['user']['instruments'][0]) # Since is a set, order is a bit unpredictable

    def test_multi_instruments_update_delete(self):
        user1_id = self.update_user(self.user1_id, 'updatedUser1', self.instru1_id, [])
        assert user1_id == self.user1_id
        _json = self.get_user(self.user1_id)
        _test_instru(self.instru1_id, self.INSTRU1, True, _json['user']['main_instrument'])
        assert len(_json['user']['instruments']) == 0