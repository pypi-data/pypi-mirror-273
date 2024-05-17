from typing import List, Optional
from popoll_backend.model.db.instrument import Instrument
from popoll_backend.model.db.user import User
from tests import IntegrationTest

class TestGetDate(IntegrationTest):
    
    def create_answer_false(self, user_id, date_id):
        id = self.create_answer(user_id=user_id, date_id=date_id)
        return self.update_answer(id, False)

    def setUp(self):
        
        # DATA
        # presence ->| present | absent  | unknown
        #            |         |         |         
        # |instrument|         |         |
        # v          |         |         |
        # -----------+---------+---------+---------
        #      1     |  user1  |  user2  | user3   
        #            | (user4) | (user9) |         
        #            | (user5) |         |         
        #            | (user8) |         |         
        # -----------+---------+---------+---------
        #      2     |  user4  |  user6  | user7
        #            |  user5  | (user2) |
        #            | (user1) | (user9) |
        # -----------+---------+---------+---------
        #      3     |  usr8   |   usr9  | usr10
        #            | (user5) | (user2) | 
        #
        
        
        super().setUp()
        self.user1_id = self.create_user('user1', self.instru1_id, [self.instru2_id])
        self.user2_id = self.create_user('user2', self.instru1_id, [self.instru2_id, self.instru3_id])
        self.user3_id = self.create_user('user3', self.instru1_id, [])
        
        self.user4_id = self.create_user('user4', self.instru2_id, [self.instru1_id])
        self.user5_id = self.create_user('user5', self.instru2_id, [self.instru1_id, self.instru3_id])
        self.user6_id = self.create_user('user6', self.instru2_id, [])
        self.user7_id = self.create_user('user7', self.instru2_id, [])
        
        self.user8_id = self.create_user('user8', self.instru3_id, [self.instru1_id])
        self.user9_id = self.create_user('user9', self.instru3_id, [self.instru1_id, self.instru2_id])
        self.user10_id = self.create_user('user10', self.instru3_id, [])
        
        self.date1_id = self.create_date(date='2025-03-10', time='15:00:00', title='firstDate', end_time=None)
        
        self.answer1_id = self.create_answer(user_id=self.user1_id, date_id=self.date1_id)
        self.answer2_id = self.create_answer_false(user_id=self.user2_id, date_id=self.date1_id)
        # self.answer3_id is None
        self.answer4_id = self.create_answer(self.user4_id, self.date1_id)
        self.answer5_id = self.create_answer(self.user5_id, self.date1_id)
        self.answer6_id = self.create_answer_false(self.user6_id, self.date1_id)
        # self.answer7_id is None
        self.answer8_id = self.create_answer(self.user8_id, self.date1_id)
        self.answer9_id = self.create_answer_false(self.user9_id, self.date1_id)
        # self.answer9_id is None
        

    def _assertAnswer(self, _json, presence: Optional[bool], user_id: int, instrument_id: int, is_main_instrument: bool):
        for answer in _json['answers']:
            if answer['user']['id'] == user_id and answer['instrument']['id'] == instrument_id and answer['is_main_instrument'] == is_main_instrument:
                if (presence == None and answer['answer'] == None) or answer['answer']['response'] == presence:
                    return True
        return False

    def test_stats_globals(self):            
        _json = self.get_date(self.date1_id)
        assert len(_json['answers']) == 19
        
        self._assertAnswer(_json, True, self.user1_id, self.instru1_id, True)
        self._assertAnswer(_json, True, self.user4_id, self.instru1_id, False)
        self._assertAnswer(_json, True, self.user5_id, self.instru1_id, False)
        self._assertAnswer(_json, True, self.user8_id, self.instru1_id, False)
        
        self._assertAnswer(_json, True, self.user4_id, self.instru2_id, True)
        self._assertAnswer(_json, True, self.user5_id, self.instru2_id, True)
        self._assertAnswer(_json, True, self.user1_id, self.instru2_id, False)
        
        self._assertAnswer(_json, True, self.user8_id, self.instru3_id, True)
        self._assertAnswer(_json, True, self.user5_id, self.instru3_id, False)
        
        self._assertAnswer(_json, False, self.user2_id, self.instru1_id, True)
        self._assertAnswer(_json, False, self.user9_id, self.instru1_id, False)
        
        self._assertAnswer(_json, False, self.user6_id, self.instru2_id, True)
        self._assertAnswer(_json, False, self.user2_id, self.instru2_id, False)
        self._assertAnswer(_json, False, self.user9_id, self.instru2_id, False)
        
        self._assertAnswer(_json, False, self.user9_id, self.instru3_id, True)
        self._assertAnswer(_json, False, self.user2_id, self.instru3_id, False)
        
        self._assertAnswer(_json, None, self.user3_id, self.instru1_id, True)
        
        self._assertAnswer(_json, None, self.user7_id, self.instru2_id, True)
        
        self._assertAnswer(_json, None, self.user10_id, self.instru3_id, True)
        