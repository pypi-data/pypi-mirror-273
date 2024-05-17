from tests import IntegrationTest

class TestDeleteUserEntry(IntegrationTest):

    def setUp(self):
        super().setUp()
        self.user1_id = self.create_user('user1', self.instru1_id, [])
        self.user2_id = self.create_user('user2', self.instru2_id, [])
        self.date1_id = self.create_date(date='2025-03-10', time='15:00:00', title='firstDate', end_time=None)
        self.answer1_id = self.create_answer(user_id=self.user1_id, date_id=self.date1_id)
        
    def test_delete_user_entry(self):
        deleted_user_id = self.delete_user(self.user1_id)
        assert deleted_user_id == self.user1_id
        _json = self.get_users()
        assert len(_json['users']) == 1
        assert _json['users'][0]['user']['name'] == 'user2'        
