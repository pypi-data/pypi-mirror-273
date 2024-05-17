from tests import IntegrationTest

class TestAddAnswerNoDupe(IntegrationTest):

    def setUp(self):
        super().setUp()
        self.date1_id = self.create_date(date='2025-03-10', time='15:00:00', title='firstDate', end_time=None)
        self.date2_id = self.create_date(date='2025-03-11', time=None, title='secondDate', end_time=None)

    def _assert_date(self, e_id, e_date, e_time, e_title, actual):
        assert e_id == actual['id']
        assert e_title == actual['title']
        assert e_date == actual['date']
        assert e_time == actual['time']

    def test_get_dates(self):
        rs = self.get_dates()
        assert len(rs['dates']) == 2
        self._assert_date(self.date1_id, '2025-03-10', '15:00:00', 'firstDate', rs['dates'][0])
        self._assert_date(self.date2_id, '2025-03-11', None, 'secondDate', rs['dates'][1])
        

