import copy
import random


class Gametable():
    tiles = ["1m", "2m", "3m", "4m", "5m", "6m", "7m", "8m", "9m",
             "1p", "2p", "3p", "4p", "5p", "6p", "7p", "8p", "9p",
             "1s", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s",
             "f1", "f2", "f3", "f4", "d1", "d2", "d3"   # 为手牌排序时需要使用
             ] * 4       # 白 发 中 东 南 西 北
    # 34*4 = 136

    def __init__(self):
        self.shuffle()  # 生成本局牌排序
        self.dora()    # 确定本局所有宝牌


    def shuffle(self):
        self.__Tiles = copy.deepcopy(self.tiles)   # 这里需要深拷贝，否则类中保存的初始牌山排序就会被打乱
        random.shuffle(self.__Tiles)

        # 以下代码输出排序，测试用
        for i in range(136):
            if i % 16 == 0:
                print()
            print(self.__Tiles[i], end=' ')
        print()

    def dora(self):
        self.__doralist = []
        self.__dorapointer = [self.__Tiles[-5], self.__Tiles[-7], self.__Tiles[-9], self.__Tiles[-11], self.__Tiles[-13],
                       self.__Tiles[-6], self.__Tiles[-8], self.__Tiles[-10], self.__Tiles[-12], self.__Tiles[-14]]
        # 前5张为表宝牌，后5张为里宝牌
        self.getdora(self.__dorapointer)
        print(self.__dorapointer)
        print(self.__doralist)

    def getdora(self, dorapointer):
        for i in dorapointer:
            if i[0] in "0123456789":
                if i[0] in "123456789":
                    self.__doralist.append(str((eval(i[0])) % 9 + 1) + i[1])
                elif i[0] == "0":
                    self.__doralist.append("6" + i[1])
            elif i[0] == "d":
                self.__doralist.append("d" + str((eval(i[1])+1) % 3))
            else:
                self.__doralist.append("f" + str((eval(i[1]) + 1) % 4))

    def getTiles(self):
        return self.__Tiles

    def getDoraPointer(self):
        return self.__dorapointer

    # 九连宝灯
    # self.__Tiles = ["1m", "1m", "1m", "2m", "1p", "2p", "3p", "4p", "5p", "6p", "7p", "8p", "9p", "1s", "2s", "3s",
    #                 "2m", "4m", "4m", "6m", "4s", "5s", "6s", "7s", "8s", "9s", "f1", "f2", "f3", "f4", "d1", "d2",
    #                 "7m", "8m", "9m", "9m", "d3", "2m", "3m", "4m", "5m", "6m", "7m", "8m", "6s", "1p", "2p", "3p",
    #                 "9m", "4p", "5p", "6p", "5m", "7p", "8p", "9p", "1s", "2s", "3s", "4s", "5s", "6s", "7s", "8s",
    #                 "9s", "f1", "f2", "f3", "f4", "d1", "d2", "d3", "2m", "3m", "4m", "1m", "6m", "8m", "1p", "2p",
    #                 "3p", "4p", "5p", "6p", "7p", "8p", "9p", "3s", "2s", "3s", "4s", "5s", "7m", "7s", "8s", "9s",
    #                 "f1", "f2", "f3", "f4", "d1", "d2", "d3", "2m", "3m", "5m",  "6m", "7m", "8m", "9m", "1p", "2p",
    #                 "3p", "4p", "5p", "6p", "7p", "8p", "9p", "1s", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s",
    #                 "f1", "f2", "f3", "5m", "f4", "d1", "d2", "d3"
    #                 ]
    # # 七对子
    # self.__Tiles = ["d1", "d1", "d2", "d2", "1m", "2m", "3m", "4m", "1p", "2p", "3p", "4p", "1s", "2s", "3s", "4s",
    #                 "d3", "d3", "f1", "f1", "1m", "2m", "3m", "4m", "1p", "2p", "3p", "4p", "1s", "2s", "3s", "4s",
    #                 "f2", "f2", "f3", "f3", "1m", "2m", "3m", "4m", "1p", "2p", "3p", "4p", "1s", "2s", "3s", "4s",
    #                 "f4", "1m", "2m", "3m", "f4", "4m", "1p", "2p", "3p", "4p", "1s", "2s", "3s", "4s", "d1", "d1",
    #                 "d2", "d2", "d3", "d3", "f1", "f1", "f2", "f2", "f3", "f3", "f4", "f4", "5m", "6m", "7m", "8m",
    #                 "9m", "5m", "6m", "7m", "8m", "9m", "5m", "6m", "7m", "8m", "9m", "5m", "6m", "7m", "8m", "9m",
    #                 "5p", "6p", "7p", "8p", "9p", "5s", "6s", "7s", "8s", "9s",
    #                 "5p", "6p", "7p", "8p", "9p", "5s", "6s", "7s", "8s", "9s",
    #                 "5p", "6p", "7p", "8p", "9p", "5s", "6s", "7s", "8s", "9s",
    #                 "5p", "6p", "7p", "8p", "9p", "5s", "6s", "7s", "8s", "9s"
    #                 ]
    # # 国士无双
    # self.__Tiles = ["d1", "1m", "d2", "9m", "d1", "2m", "3m", "4m", "f2", "2p", "3p", "4p", "d3", "2s", "3s", "4s",
    #                 "d3", "1s", "f1", "9s", "1m", "2m", "3m", "4m", "1p", "2p", "3p", "4p", "1s", "2s", "3s", "4s",
    #                 "f2", "1p", "f3", "9p", "1m", "2m", "3m", "4m", "1p", "2p", "3p", "4p", "1s", "2s", "3s", "4s",
    #                 "f4", "1m", "2m", "3m", "4m", "f4", "1p", "2p", "3p", "4p", "1s", "2s", "3s", "4s", "d1", "d1",
    #                 "d2", "d2", "d3", "d3", "f1", "f1", "f2", "f2", "f3", "f3", "f4", "f4", "5m", "6m", "7m", "8m",
    #                 "9m", "5m", "6m", "7m", "8m", "9m", "5m", "6m", "7m", "8m", "9m", "5m", "6m", "7m", "8m", "d2",
    #                 "5p", "6p", "7p", "8p", "f3", "5s", "6s", "7s", "8s", "f1",
    #                 "5p", "6p", "7p", "8p", "9p", "5s", "6s", "7s", "8s", "9s",
    #                 "5p", "6p", "7p", "8p", "9p", "5s", "6s", "7s", "8s", "9s",
    #                 "5p", "6p", "7p", "8p", "9p", "5s", "6s", "7s", "8s", "9s"
    #                 ]