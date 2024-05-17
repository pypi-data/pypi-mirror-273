from tests import IntegrationTest, TestForwardError

class TestDeleteDateEntry(IntegrationTest):

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
        
    def test_delete_date_entry(self):
        deleted_date2_id = self.delete_date(self.date2_id)
        deleted_date3_id = self.delete_date(self.date3_id)
        assert deleted_date2_id == self.date2_id
        assert deleted_date3_id == self.date3_id
        _json = self.get_user(self.user1_id)
        assert len(_json['dates']) == 1
        
        
    def test_delete_non_existing_date(self):
        rs = self.delete_date(self.date2_id)
        _json = self.get_user(self.user1_id)
        assert len(_json['dates']) == 2
        rs = self.delete_date(self.date2_id)
        _json = self.get_user(self.user1_id)
        assert len(_json['dates']) == 2