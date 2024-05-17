from tests import IntegrationTest

def test_line(json, method=None, ttype=None):
    assert json['method'] == method
    assert json['_type'] == ttype

class TestHistory(IntegrationTest):

    def setUp(self):
        super().setUp()
        self.user1_id = self.create_user('user1', self.instru1_id, [])
        self.user2_id = self.create_user('user2', self.instru2_id, [])
        self.date1_id = self.create_date(date='2025-03-10', time='15:00:00', title='firstDate')
        self.date2_id = self.create_date(date='2025-03-11', time='18:00:00', title='secondDate')
        self.date3_id = self.create_date(date='2025-03-12', time=None, title='thirdDate')
        self.answer1_id = self.create_answer(user_id=self.user1_id, date_id=self.date1_id, response=True)
        self.answer2_id = self.create_answer(user_id=self.user1_id, date_id=self.date2_id, response=True)
        self.answer3_id = self.create_answer(user_id=self.user1_id, date_id=self.date3_id, response=True)
        self.answer4_id = self.create_answer(user_id=self.user2_id, date_id=self.date1_id, response=True)
        self.answer5_id = self.create_answer(user_id=self.user2_id, date_id=self.date2_id, response=True)
        self.answer6_id = self.create_answer(user_id=self.user2_id, date_id=self.date3_id, response=True)
        self.udpateAnswer(self.answer1_id, False)
        self.delete_date(self.date2_id)

    def expected_lines(self, nbCreateInstrus, nbCreateUsers, nbCreateDates, nbCreateAnswers, nbUpdate, nbDelete):
        return nbCreateInstrus + nbCreateUsers*2 + nbCreateDates + nbCreateAnswers + nbUpdate + nbDelete
        
    # def test_get_user_sorted(self):
    #     _json = self.toJSON(self.get_history())['history']
    #     assert self.expected_lines(3, 2, 3, 6, 1, 1) == len(_json)
    #     test_line(_json[0], method='add', ttype='Instrument')
    #     test_line(_json[1], method='add', ttype='Instrument')
    #     test_line(_json[2], method='add', ttype='Instrument')
    #     test_line(_json[3], method='add', ttype='User')
    #     test_line(_json[4], method='update', ttype='User')
    #     test_line(_json[5], method='add', ttype='User')
    #     test_line(_json[6], method='update', ttype='User')
    #     test_line(_json[7], method='add', ttype='Date')
    #     test_line(_json[8], method='add', ttype='Date')
    #     test_line(_json[9], method='add', ttype='Date')
    #     test_line(_json[10], method='add', ttype='Answer')
    #     test_line(_json[11], method='add', ttype='Answer')
    #     test_line(_json[12], method='add', ttype='Answer')
    #     test_line(_json[13], method='add', ttype='Answer')
    #     test_line(_json[14], method='add', ttype='Answer')
    #     test_line(_json[15], method='add', ttype='Answer')
    #     test_line(_json[16], method='update', ttype='Answer')
    #     test_line(_json[17], method='delete', ttype='Date')
        
