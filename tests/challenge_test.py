import unittest


from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed

import engine
import coup


class TestChallenge(unittest.TestCase):

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

    def test_challenge(self):
        self.game = engine.GameState.get_by_id(self.game_id)
        self.game.players[0].cards[0].name = "duke"
        self.game.players[1].money = 3
        self.game.players[1].cards[0].name = "assassin"
        print self.game.players
        print self.game.unused_cards
        self.game.take_action(self.game.get_player("A"), "tax", None)
        self.game.pose_challenge(self.game.get_player("C"))
        self.game.resolve_challenge(self.game.get_player("A"), "duke")
        self.game.lose_challenge(self.game.get_player("C"), self.game.get_player("C").live_card_names()[0])
        self.game.take_action(self.game.get_player("B"), "assassinate", self.game.get_player("C"))
        self.game.lose_card(self.game.get_player("C"), self.game.get_player("C").live_card_names()[0])
        self.game.take_action(self.game.get_player("D"), "tax", None)
        with self.assertRaises(engine.Misplay):
            self.game.pose_challenge(self.game.get_player("C"))
        self.game.take_action(self.game.get_player("A"), "income", None)
        print self.game.players
        print self.game.unused_cards
        self.assertTrue(True)
