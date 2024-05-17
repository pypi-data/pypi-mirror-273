from tests import IntegrationTest, TestForwardError

class TestUpdateuserEntry(IntegrationTest):

    def setUp(self):
        super().setUp()
        self.user1_id = self.create_user('user1', self.instru1_id, [])
        self.user3_id = self.create_user('user3', self.instru1_id, [])
        self.date1_id = self.create_date(date='2025-03-10', time='15:00:00', title='firstDate', end_time=None)
        self.answer1_id = self.create_answer(user_id=self.user1_id, date_id=self.date1_id)
        
    def test_update_user_entry(self):
        updated_user1_id = self.update_user(self.user1_id, 'user2', self.instru2_id, [])
        assert updated_user1_id == self.user1_id
        _json = self.get_user(updated_user1_id)
        assert _json['user']['user']['name'] == 'user2'
        assert _json['user']['main_instrument']['id'] == self.instru2_id
        assert _json['user']['main_instrument']['name'] == self.INSTRU2

    def test_update_user_entry_conflict(self):
        rs = self.update_user(self.user1_id, 'user3', self.instru2_id, [], fail=True)
        assert rs.status_code == 400
        # TODO assert json.loads(rs.json)["message"] == 'User with name user1 already exists.'
      
    # TODO Does not make sens since is returning valid answer but nothing impacted  
    # def test_update_user_entry_not_found(self):
    #     try:
    #         rs = self.update_user(self.user1_id + 10, 'user3', self.instru2_id, [], fail=True)
    #         print(rs)
    #         assert False
    #     except TestForwardError as e:
    #         assert e.rs.status_code == 404
    #         _json = self.toJSON(self.get())
    #         assert len(_json['users']) == 2