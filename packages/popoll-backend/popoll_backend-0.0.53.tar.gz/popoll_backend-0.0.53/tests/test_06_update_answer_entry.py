from tests import IntegrationTest, TestForwardError

class TestUpdateAnswerEntry(IntegrationTest):

    def setUp(self):
        super().setUp()
        self.user1_id = self.create_user('user1', self.instru1_id, [])
        self.user2_id = self.create_user('user2', self.instru3_id, [])
        self.date1_id = self.create_date(date='2025-03-10', time='15:00:00', title='firstDate', end_time=None)
        self.answer1_id = self.create_answer(user_id=self.user1_id, date_id=self.date1_id)
        
    def test_update_answer_entry(self):
        updated_answer1_id = self.update_answer(self.answer1_id, False)
        assert updated_answer1_id == self.answer1_id
        _json = self.get_user(self.user1_id)
        assert _json['dates'][0]['answer']['response'] == False
        
    # TODO Does not make sens since is returning valid answer but nothing impacted  
    # def test_update_answer_entry_not_found(self):
    #     try:
    #         self.udpate_answer(self.answer1_id + 10, False)
    #         assert False
    #     except TestForwardError as e:
    #         assert e.rs.status_code == 404
    #         _json = self.toJSON(self.get())
    #         assert len(_json['answers']) == 1
