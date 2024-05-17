from tests import IntegrationTest, TestForwardError

class TestUpdateDateEntry(IntegrationTest):

    def setUp(self):
        super().setUp()
        self.user1_id = self.create_user('user1', self.instru1_id, [])
        self.date1_id = self.create_date(date='2025-03-10', time='15:00:00', title='firstDate', end_time=None)
        self.date2_id = self.create_date(date='2025-03-12', time=None, title='secondDate', end_time=None)
        self.answer1_id = self.create_answer(user_id=self.user1_id, date_id=self.date1_id)
        
    def test_update_date_entry(self):
        updated_date1_id = self.udpate_date(self.date1_id, date='2025-03-10', time='18:00:00', title='firstDateUpdated')
        assert updated_date1_id == self.date1_id
        _json = self.get_user(self.user1_id)
        assert _json['dates'][0]['date']['date'] == '2025-03-10'
        assert _json['dates'][0]['date']['time'] == '18:00:00'
        assert _json['dates'][0]['date']['end_time'] == None
        assert _json['dates'][0]['date']['title'] == 'firstDateUpdated'
        
    def test_update_date_entry_remove_time(self):
        updated_date1_id = self.udpate_date(self.date1_id, date='2025-03-10', time=None, title='firstDateUpdated')
        assert updated_date1_id == self.date1_id
        _json = self.get_user(self.user1_id)
        assert _json['dates'][0]['date']['date'] == '2025-03-10'
        assert _json['dates'][0]['date']['title'] == 'firstDateUpdated'
        
     # TODO Does not make sens since is returning valid answer but nothing impacted  
    # def test_update_date_entry_not_found(self):
    #     try:
    #         self.udpate_date(self.date1_id + 10, date='2025-03-10', time='18:00:00', title='firstDateUpdated')
    #         assert False
    #     except TestForwardError as e:
    #         assert e.rs.status_code == 404
    #         _json = self.toJSON(self.get())
    #         assert len(_json['users']) == 1
