from tests import IntegrationTest

def _test_date_time(expectedDate, expectedTime, actualDate):
        assert expectedDate == actualDate['date']
        assert expectedTime == actualDate['time']

class TestGetDatesSortByDate(IntegrationTest):

    def setUp(self):
        super().setUp()
        self.user1_id = self.create_user(name='user1', main_instrument=self.instru1_id, instruments=[])
        self.date1_id = self.create_date(date='2025-03-12', time='15:00:00', title='firstDate', end_time=None)
        self.create_answer(self.user1_id, self.date1_id)
        self.date2_id = self.create_date(date='2025-03-11', time='18:00:00', title='secondDate', end_time=None)
        self.create_answer(self.user1_id, self.date2_id)
        self.date3_id = self.create_date(date='2025-03-11', time=None, title='thirdDate', end_time=None)
        self.create_answer(self.user1_id, self.date3_id)
        
    def test_get_user_sorted(self):
        _json = self.get_user(self.user1_id)
        assert len(_json['dates']) == 3
        _test_date_time('2025-03-11', None, _json['dates'][0]['date'])
        _test_date_time('2025-03-11', '18:00:00', _json['dates'][1]['date'])
        _test_date_time('2025-03-12', '15:00:00', _json['dates'][2]['date'])
