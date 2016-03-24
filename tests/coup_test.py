import unittest


from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed

import engine
import coup


class TestCoup(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().set_cache_policy(False)

        self.game_id = "test_game"
        self.game = engine.GameState.get_by_id(self.game_id)
        self.list_of_players = ["A", "B", "C", "D"]
        coup.deal_cards(self.game, self.game_id, self.list_of_players)

    def tearDown(self):
        self.testbed.deactivate()

    def test_coup(self):
        self.game = engine.GameState.get_by_id(self.game_id)
        self.game.players[0].money = 8
        self.game.players[1].cards[0].eliminated = True
        print self.game.players
        print self.game.unused_cards
        self.game.take_action(self.game.get_player("A"), "coup", self.game.get_player("B"))
        self.game.take_action(self.game.get_player("C"), "tax", None)
        with self.assertRaises(engine.Misplay):
            self.game.pose_challenge(self.game.get_player("B"))
        self.game.take_action(self.game.get_player("D"), "income", None)
        print self.game.players
        print self.game.unused_cards
        self.assertTrue(True)
