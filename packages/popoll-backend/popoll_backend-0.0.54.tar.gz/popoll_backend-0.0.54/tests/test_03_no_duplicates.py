import json

from tests import IntegrationTest, TestForwardError

class TestNoDuplicates(IntegrationTest):

    def setUp(self):
        super().setUp()
        self.user1_id = self.create_user('user1', self.instru1_id, [])
        self.date1_id = self.create_date(date='2025-03-10', time='15:00:00', title='firstDate', end_time=None)
        self.answer1_id = self.create_answer(user_id=self.user1_id, date_id=self.date1_id)
        
    def test_no_duplicate_user(self):
        rs = self.create_user('user1', self.instru1_id, [], fail=True)
        assert rs.status_code == 400
        # TODO assert json.loads(rs.json)["message"] == 'User with name user1 already exists.'
    
    def test_no_duplicate_user_then_valid(self):
        rs = self.create_user('user1', self.instru1_id, [], fail=True)
        assert rs.status_code == 400
        user2_id = self.create_user('user2', self.instru2_id, [])
        _json = self.get_users()
        assert len(_json['users']) == 2

            
    def test_can_duplicate_dates(self):
        date2_id = self.create_date(date='2025-03-10', time='15:00:00', title='firstDate', end_time='18:00:00')
        _json = self.get_user(self.user1_id)
        assert len(_json['dates']) == 2
        assert self.date1_id != date2_id