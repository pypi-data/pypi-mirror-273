from tests import IntegrationTest

class TestSimpleAdds(IntegrationTest):

    def setUp(self):
        super().setUp()
        self.user1_id = self.create_user('user1', self.instru1_id, [])
        self.date1_id = self.create_date(date='2025-03-10', time='15:00:00', title='firstDate', end_time='18:00:00')
        self.answer1_id = self.create_answer(user_id=self.user1_id, date_id=self.date1_id)
        
    def test_simple_adds(self):
        assert self.user1_id != None
        assert self.date1_id != None
        assert self.answer1_id != None
        _json = self.get_user(self.user1_id)
        assert _json['user']['user']['id'] == self.user1_id
        assert _json['user']['user']['name'] == 'user1'
        assert _json['user']['main_instrument']['id'] == self.instru1_id
        assert len(_json['user']['instruments']) == 0
        assert len(_json['dates']) == 1
        assert _json['dates'][0]['date']['id'] == self.date1_id
        assert _json['dates'][0]['date']['title'] == 'firstDate'
        assert _json['dates'][0]['date']['date'] == '2025-03-10'
        assert _json['dates'][0]['date']['time'] == '15:00:00'
        assert _json['dates'][0]['date']['end_time'] == '18:00:00'
        assert _json['dates'][0]['answer']['id'] == self.answer1_id
        assert _json['dates'][0]['answer']['response'] == True
        