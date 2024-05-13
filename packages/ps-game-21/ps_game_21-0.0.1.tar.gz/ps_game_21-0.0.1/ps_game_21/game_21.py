'''
该模块可以实现一个21点扑克牌游戏程序，实现电脑AI和玩家的比拼
'''

from ps_game_21.cards_info import CardsInfo
from ps_game_21.game_decision import GameDecision
from ps_game_21.show import Show
from ps_game_21.computer import Computer
from ps_game_21.player import Player


class Game_21:
    '''
    游戏规则如下：
    a、	现有一副扑克牌，第一轮双方各有两张随机分发的扑克牌，其中一张为底牌，只有自己知
    晓，对方只能看到另一张牌。
    b、	接下来每一轮，每位玩家可以选择继续随机摸一张牌或者叫停（即此轮该玩家不摸牌）
    c、	在某一轮中，若双方都叫停，则进行结果评定。谁的“点数和”越接近21点且不大于21点
    （等于21点为最大）为获胜方，凡是大于21点（称为“引爆”）或者“点数和”小于对方的“点数
    和”的一方为输。
    d、	大小王的点数为0。
    e、	J,Q,K的点数为10。
    f、	其余的点数都与自己所表示的数字一样。
    '''

    def __init__(self):
        self.num = 54  # 扑克牌总数
        self.end = 21  # 最大点数
        self.player_count = 0  # 玩家点数
        self.computer_count = 0  # 电脑点数
        self.player_cards = []  # 玩家手牌
        self.computer_cards = []  # 电脑手牌
        self.player_status = 1  # 玩家状态,1为继续摸牌,0为叫停
        self.computer_status = 1  # 电脑状态,1为继续摸牌,0为叫停
        self.computer_show = None  # 电脑展示的手牌
        self.player_show = None  # 玩家展示的手牌

        # 初始牌组信息
        cards_info = CardsInfo()
        self.cards = cards_info.put_card()  # 初始化牌组
        self.cards_data = cards_info.get_cards_data()  # 每张牌对应的点数

        # 显示信息的对象
        self.show = Show()

        # 初始化电脑、玩家对象
        self.computer = Computer()
        self.player = Player()

        # 初始化输赢判定对象
        self.game_decision = GameDecision()

    def play_game(self):
        # 开始游戏
        # 展示游戏规则
        self.show.show_rule()
        
        # 电脑和玩家先交替摸2张牌
        for _ in range(2):
            self.computer_count, self.computer_cards, self.num = (
                self.computer.computer_get_card(
                    self.computer_count,
                    self.computer_cards,
                    self.computer_status,
                    self.cards,
                    self.cards_data,
                    self.num,
                )
            )
            self.player_count, self.player_cards, self.num = (
                self.player.player_get_card(
                    self.player_count,
                    self.player_cards,
                    self.player_status,
                    self.cards,
                    self.cards_data,
                    self.num,
                )
            )

        # 选择要展示的手牌
        self.computer_show = self.computer.show_card(self.computer_cards)
        self.player_show = self.player.show_card(self.player_cards)

        # 正式开始游戏
        while True:
            self.show.show_rule()
            self.show.show_info(self.computer_show, self.player_show, self.num)

            # 玩家先判断是否叫停或者摸牌
            self.player_status = self.player.player_stop(
                self.player_count, self.player_status
            )
            self.player_count, self.player_cards, self.num = (
                self.player.player_get_card(
                    self.player_count,
                    self.player_cards,
                    self.player_status,
                    self.cards,
                    self.cards_data,
                    self.num,
                )
            )

            # 电脑先判断是否叫停或者摸牌
            self.computer_status = self.computer.computer_stop(
                self.computer_count, self.computer_status
            )
            self.computer_count, self.computer_cards, self.num = (
                self.computer.computer_get_card(
                    self.computer_count,
                    self.computer_cards,
                    self.computer_status,
                    self.cards,
                    self.cards_data,
                    self.num,
                )
            )

            # 若双方都叫停，则进行输赢判定
            if self.computer_status == 0 and self.player_status == 0:
                result = self.game_decision.game_decision(
                    self.player_count,
                    self.computer_count,
                    self.player_cards,
                    self.computer_cards,
                )
                return result
