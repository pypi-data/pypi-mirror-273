class Show:
    # 输出基本信息的类
    def __init__(self):
        pass

    def show_rule(self):
        # 输出游戏规则
        print('-' * 50)
        print('游戏规则如下：')
        print(
            'a、现有一副扑克牌，第一轮双方各有两张随机分发的扑克牌，其中一张为底牌，只有自己知晓，对方只能看到另一张牌。'
        )
        print(
            'b、接下来每一轮，每位玩家可以选择继续随机摸一张牌或者叫停（即此轮该玩家不摸牌）'
        )
        print(
            'c、在某一轮中，若双方都叫停，则进行结果评定。谁的“点数和”越接近21点且\
不大于21点（等于21点为最大）为获胜方，凡是大于21点（称为“引爆”）或者“点数和”小于对方的“点数和”的一方为输。'
        )
        print('d、大小王的点数为0。')
        print('e、J,Q,K的点数为10。')
        print('f、其余的点数都与自己所表示的数字一样。')
        print()

    def show_info(self, computer_show, player_show, num):
        # 展示手牌
        print('牌堆还有 ' + str(num) + ' 张牌')
        print('电脑展示的手牌是：', computer_show)
        print('玩家展示的手牌是：', player_show)
        print()
