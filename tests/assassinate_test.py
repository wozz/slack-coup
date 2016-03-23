import unittest


from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed

import engine
import coup


class TestAssassinate(unittest.TestCase):

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

    def test_assassinate(self):
        self.game = engine.GameState.get_by_id(self.game_id)
        self.game.players[0].money = 3
        self.game.players[1].cards[0].name = "duke"
        self.game.players[1].cards[1].name = "contessa"
        print self.game.players
        print self.game.unused_cards
        self.game.take_action(self.game.get_player("A"), "income", None)
        self.game.take_action(self.game.get_player("B"), "tax", None)
        self.game.pose_challenge(self.game.get_player("A"))
        self.game.resolve_challenge(self.game.get_player("B"), "duke")
        self.game.lose_challenge(self.game.get_player("A"), self.game.get_player("A").cards[0].name)
        self.game.take_action(self.game.get_player("C"), "income", None)
        self.game.take_action(self.game.get_player("D"), "income", None)
        self.game.take_action(self.game.get_player("A"), "assassinate", self.game.get_player("B"))
        self.game.pose_block(self.game.get_player("B"), "contessa")
        self.game.pose_challenge(self.game.get_player("A"))
        self.game.resolve_challenge(self.game.get_player("B"), "contessa")
        print self.game.players
        print self.game.unused_cards
        self.assertTrue(True)
