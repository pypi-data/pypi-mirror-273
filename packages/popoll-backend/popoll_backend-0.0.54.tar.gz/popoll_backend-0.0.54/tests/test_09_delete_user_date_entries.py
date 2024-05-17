from tests import IntegrationTest

class TestDeleteUserDateEntries(IntegrationTest):

    def setUp(self):
        super().setUp()
        self.user1_id = self.create_user('user1', self.instru1_id, [])
        self.user2_id = self.create_user('user2', self.instru2_id, [])
        self.date1_id = self.create_date(date='2025-03-10', time='15:00:00', title='firstDate', end_time=None)
        self.date2_id = self.create_date(date='2025-03-11', time='18:00:00', title='secondDate', end_time=None)
        self.date3_id = self.create_date(date='2025-03-12', time=None, title='thirdDate', end_time=None)
        self.answer1_id = self.create_answer(user_id=self.user1_id, date_id=self.date1_id)
        self.answer2_id = self.create_answer(user_id=self.user1_id, date_id=self.date2_id)
        self.answer3_id = self.create_answer(user_id=self.user1_id, date_id=self.date3_id)
        self.answer4_id = self.create_answer(user_id=self.user2_id, date_id=self.date1_id)
        self.answer5_id = self.create_answer(user_id=self.user2_id, date_id=self.date2_id)
        self.answer6_id = self.create_answer(user_id=self.user2_id, date_id=self.date3_id)
        
    def test_delete_user_date_entries(self):
        _json = self.get_users()
        assert len(_json['users']) == 2
        _json_user1 = self.get_user(self.user1_id)
        assert len(_json_user1['dates']) == 3
        assert _json_user1['dates'][0].get('answer', None) != None
        
        self.delete_date(self.date1_id)
        _json = self.get_user(self.user1_id)
        assert len(_json['dates']) == 2
        
        self.delete_user(self.user1_id)
        _json = self.get_users()
        assert len(_json['users']) == 1
        assert _json['users'][0]['user']['id'] == self.user2_id
        
        user3_id = self.create_user('user3', self.instru3_id, [])
        assert self.user1_id != user3_id
        _json = self.get_users()
        assert len(_json['users']) == 2
        _json = self.get_user(user3_id)
        assert _json['dates'][1].get('answer', None) == None
        
        answer7_id = self.create_answer(user_id=user3_id, date_id=self.date2_id)
        self.update_answer(answer7_id, False)
        _json = self.get_user(user3_id)
        assert len(_json['dates']) == 2
        assert _json['dates'][0]['answer']['response'] == False
