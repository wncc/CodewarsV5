from scripts.Troops.dummies import *
from config import TEAM1
from config import TEAM2
from scripts.utils import rescale_position
from scripts.game_config import *

class DataFlow: 
    def provide_data(self):
        tower1_troops = []
        tower1_oppTroops = []
        tower2_troops = []
        tower2_oppTroops = []

        for troop in self.tower1.myTroops:
            tower1_troops.append(DummyTroop(troop,False,self.arena_display_size))
            troop.dummy_original = DummyTroop(troop,False,self.arena_display_size)
            t1 = DummyTroop(troop,True,self.arena_display_size)
            troop.dummy = t1
            tower2_oppTroops.append(t1)
        for troop in self.tower2.myTroops:
            tower2_troops.append(DummyTroop(troop,True,self.arena_display_size))
            troop.dummy_original = DummyTroop(troop,True,self.arena_display_size)
            t2 = DummyTroop(troop,False,self.arena_display_size)
            troop.dummy = t2
            tower1_oppTroops.append(t2)

        tower1 = DummyTower(self.tower1,False,self.arena_display_size)
        tower1_opp = DummyTower(self.tower2, False,self.arena_display_size)
        tower1_opp.deployable_troops = None
        tower1_opp.total_elixir = None
        tower1_opp.total_dark_elixir = None
        tower2 = DummyTower(self.tower2,True,self.arena_display_size)
        tower2_opp = DummyTower(self.tower1,True,self.arena_display_size)
        tower2_opp.deployable_troops = None
        tower2_opp.total_elixir = None
        tower2_opp.total_dark_elixir = None

        self.tower1.dummy = tower2_opp
        self.tower1.dummy_original = tower1
        self.tower2.dummy = tower1_opp
        self.tower2.dummy_original = tower2

        for dummy_troop, troop in zip(tower1_troops,self.tower1.myTroops):
            if troop.target:
                dummy_troop.target = troop.target.dummy
            else:
                dummy_troop.target = None
        for dummy_troop, troop in zip(tower2_troops,self.tower2.myTroops):
            if troop.target:
                dummy_troop.target = troop.target.dummy
            else:
                dummy_troop.target = None
        for dummy_troop, troop in zip(tower1_oppTroops,self.tower1.oppTroops):
            if troop.target:
                dummy_troop.target = troop.target.dummy_original
            else:
                dummy_troop.target = None
        for dummy_troop, troop in zip(tower2_oppTroops,self.tower2.oppTroops):
            if troop.target:
                dummy_troop.target = troop.target.dummy_original
            else:
                dummy_troop.target = None

        if self.tower1.target:
            tower1.target = self.tower1.target.dummy
            tower2_opp.target = self.tower1.target.dummy_original
        else:
            tower1.target = None
            tower2_opp.target = None
        if self.tower2.target:
            tower2.target = self.tower2.target.dummy
            tower1_opp.target = self.tower2.target.dummy_original
        else:
            tower2.target = None
            tower1_opp.target = None

        self.data_provided1["MyTower"] = tower1
        self.data_provided1["OppTower"] = tower1_opp
        self.data_provided1["MyTroops"] = tower1_troops
        self.data_provided1["OppTroops"] = tower1_oppTroops

        self.data_provided2["MyTower"] = tower2
        self.data_provided2["OppTower"] = tower2_opp
        self.data_provided2["MyTroops"] = tower2_troops
        self.data_provided2["OppTroops"] = tower2_oppTroops

    def deployment(self):
        troops1_list, team_signal1 = TEAM1.deploy(self.data_provided1)
        troops2_list, team_signal2 = TEAM2.deploy(self.data_provided2)
        self.data_provided1 = {}
        self.data_provided2 = {}
        for troop, position in troops2_list:
            position = rescale_position(position)
            self.tower2.deploy(troop,convert_player2(position,self.arena_display_size))
        for troop, position in troops1_list:
            position = rescale_position(position)
            self.tower1.deploy(troop,position)
        if len(team_signal1) > SIGNAL_LENGTH:
            self.team1_script_test = False
        if len(team_signal2) > SIGNAL_LENGTH:
            self.team2_script_test = False

    def attack_die(self):
        for troop in self.tower2.myTroops:
            troop.update_position()
        for troop in self.tower1.myTroops:
            troop.update_position()
        for troop in self.tower2.myTroops:
            troop.do_work()
        for troop in self.tower1.myTroops:
            troop.do_work()
        self.tower2.do_work()
        self.tower1.do_work()
        for troop in self.tower2.myTroops:
            troop.die()
        for troop in self.tower1.myTroops:
            troop.die()