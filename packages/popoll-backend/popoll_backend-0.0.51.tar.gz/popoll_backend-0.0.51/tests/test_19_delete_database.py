from tests import IntegrationTest

class TestDeleteDatabase(IntegrationTest):

    def setUp(self):
        super().setUp()
        self.user1_id = self.create_user('user1', self.instru1_id, [])


    def test_delete_database(self):            
        _json = self.get_users()
        assert len(_json['users']) == 1
        self.delete_database()
        rs = self.get_users(fail=True)
        assert rs.status_code == 400
        

