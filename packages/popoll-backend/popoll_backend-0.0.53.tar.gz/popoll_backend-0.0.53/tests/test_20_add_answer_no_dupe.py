from tests import IntegrationTest

class TestAddAnswerNoDupe(IntegrationTest):

    def setUp(self):
        super().setUp()
        self.user1_id = self.create_user('user1', self.instru1_id, [])
        self.date1_id = self.create_date(date='2025-03-10', time='15:00:00', title='firstDate', end_time=None)
        self.answer1_id = self.create_answer(self.user1_id, self.date1_id)


    def test_delete_database(self):            
        rs = self.create_answer(self.user1_id, self.date1_id, fail=True)
        assert rs.status_code == 400
        

