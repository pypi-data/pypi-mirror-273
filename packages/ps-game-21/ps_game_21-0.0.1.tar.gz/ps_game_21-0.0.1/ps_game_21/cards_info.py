class CardsInfo:
    # 设置牌组基础信息的类
    def __init__(self):
        self.put_card()  # 初始化牌组
        self.get_cards_data()  # 初始化牌组点数

    def put_card(self):
        # 初始化牌组
        self.cards = []  # 存储牌组里所有的牌的名字
        self.cards.append('黑桃A')
        self.cards.append('红桃A')
        self.cards.append('梅花A')
        self.cards.append('方片A')
        for i in range(2, 11):
            self.cards.append('黑桃' + str(i))
            self.cards.append('红桃' + str(i))
            self.cards.append('梅花' + str(i))
            self.cards.append('方片' + str(i))
        self.cards.append('黑桃J')
        self.cards.append('红桃J')
        self.cards.append('梅花J')
        self.cards.append('方片J')
        self.cards.append('黑桃Q')
        self.cards.append('红桃Q')
        self.cards.append('梅花Q')
        self.cards.append('方片Q')
        self.cards.append('黑桃K')
        self.cards.append('红桃K')
        self.cards.append('梅花K')
        self.cards.append('方片K')
        self.cards.append('大王')
        self.cards.append('小王')
        return self.cards

    def get_cards_data(self):
        # 每张牌对应的点数
        self.cards_data = {}
        for i in range(len(self.cards)):
            if i < 4:
                # A
                self.cards_data[self.cards[i]] = 1
            elif i < 8:
                # 2
                self.cards_data[self.cards[i]] = 2
            elif i < 12:
                # 3
                self.cards_data[self.cards[i]] = 3
            elif i < 16:
                # 4
                self.cards_data[self.cards[i]] = 4
            elif i < 20:
                # 5
                self.cards_data[self.cards[i]] = 5
            elif i < 24:
                # 6
                self.cards_data[self.cards[i]] = 6
            elif i < 28:
                # 7
                self.cards_data[self.cards[i]] = 7
            elif i < 32:
                # 8
                self.cards_data[self.cards[i]] = 8
            elif i < 36:
                # 9
                self.cards_data[self.cards[i]] = 9
            elif i < 52:
                # 10 J Q K
                self.cards_data[self.cards[i]] = 10
            elif i < 54:
                # 大小王
                self.cards_data[self.cards[i]] = 0
        return self.cards_data
