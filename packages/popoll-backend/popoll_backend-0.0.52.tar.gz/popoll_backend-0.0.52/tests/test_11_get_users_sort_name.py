from tests import IntegrationTest

class TestGetUsersSortByName(IntegrationTest):

    def setUp(self):
        super().setUp()
        self.user1_id = self.create_user('BBB', self.instru2_id, [])
        self.user2_id = self.create_user('AAA', self.instru1_id, [])
        
    def test_get_user_sorted(self):
        _json = self.get_users()
        assert len(_json['users']) == 2
        assert _json['users'][0]['user']['name'] == 'AAA'
        assert _json['users'][0]['user']['id'] == self.user2_id
        assert _json['users'][1]['user']['name'] == 'BBB'
        assert _json['users'][1]['user']['id'] == self.user1_id
