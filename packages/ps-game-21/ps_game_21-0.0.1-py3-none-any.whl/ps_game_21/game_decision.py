class GameDecision:
    # 游戏输赢判定

    def __init__(self):
        pass

    def game_decision(self, player_count, computer_count, player_cards, computer_cards):
        # 判断输赢
        # 平局返回1，电脑获胜返回2，玩家获胜返回3
        if player_count > 21 and computer_count > 21:
            print('平局')
            print('你的点数为%d点' % player_count)
            print('你的牌组为:',player_cards)
            print('电脑点数为%d点' % computer_count)
            print('电脑的牌组为:',computer_cards)
            print("你和电脑都“引爆”了")
            return 1
        elif player_count > 21 and computer_count <= 21:
            print('电脑赢了')
            print('你的点数为%d点' % player_count)
            print('你的牌组为:',player_cards)
            print('电脑点数为%d点' % computer_count)
            print('电脑的牌组为:',computer_cards)
            print("你“引爆”了")
            return 2
        elif player_count <= 21 and computer_count > 21:
            print('你赢了')
            print('你的点数为%d点' % player_count)
            print('你的牌组为:',player_cards)
            print('电脑点数为%d点' % computer_count)
            print('电脑的牌组为:',computer_cards)
            print("电脑“引爆”了")
            return 3
        elif player_count > computer_count:
            print('你赢了')
            print('你的点数为%d点' % player_count)
            print('你的牌组为:',player_cards)
            print('电脑点数为%d点' % computer_count)
            print('电脑的牌组为:',computer_cards)
            return 3
        elif player_count < computer_count:
            print('电脑赢了')
            print('你的点数为%d点' % player_count)
            print('你的牌组为:',player_cards)
            print('电脑点数为%d点' % computer_count)
            print('电脑的牌组为:',computer_cards)
            return 2
        return 0
