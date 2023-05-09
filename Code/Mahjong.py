import copy
import pygame
import random
from GameTable import Gametable
from Rule import huJudge
from pygame.locals import *
from sys import exit


class Mahjong():
    def __init__(self):
        self.__clock = pygame.time.Clock()
        self.screenSet()   # 游戏画面设置
        self.playerSet()   # 玩家设置
        self.sitSet()      # 座次设置
        self.gameStart()   # 游戏开始

    def screenSet(self):
        pygame.init()
        screen = pygame.display.set_mode((600, 400))
        # screen 的本质上就是一个 Surface 对象，它是游戏的主窗口，
        # 也就是整个游戏中尺寸最大的“纸”，任何其他的 Surface 对象都需要附着在这张最大的“纸”上
        pygame.display.set_caption('Mahjong')

    def playerSet(self):
        # self.__playername = input("请输入您的昵称：")
        self.__playername = "飞翔大神天使"   # 方便测试用
        print("您好，{}！欢迎来到麻将世界！".format(self.__playername))

    def sitSet(self):
        self.__sit = random.randint(0, 3)
        # self.__sit = 3
        print("您这把{}起！".format("东南西北"[self.__sit]))

    def prepare(self):
        print("\n\n正在清理牌桌...")
        self.__table = Gametable()    # 清理牌桌
        print("正在获取初始手牌...")
        self.__hands = self.getfHands(self.__sit)
        print(self.__hands)

    def reset(self):
        print("\n\n正在清理牌桌...")
        self.__table = Gametable()  # 清理牌桌
        print("正在获取初始手牌...")
        self.__hands = self.getfHands(self.__sit)
        print(self.__hands)

    def getfHands(self, sit):
        hands = []
        base = (sit-1) * 4   # 摸牌起始位置
        # 东起 0，南起 4, 西起 8, 北起 12
        for i in range(3):  # 分3次摸2垛
            hands.append(self.__table.getTiles()[i * 16 + base])
            hands.append(self.__table.getTiles()[i * 16 + base + 1])
            hands.append(self.__table.getTiles()[i * 16 + base + 2])
            hands.append(self.__table.getTiles()[i * 16 + base + 3])
        hands.append(self.__table.getTiles()[48 + base])
        self.handsSort(hands)
        return hands

    def handsSort(self, hands):
        hands.sort(key=Gametable.tiles.index)
        return hands

    def gameStart(self):
        self.__game_num = 0       # 当前对局数
        # self.__current_turn = 0   # 当前局数
        self.__wind = "东"        # 从东场开始
        gamepara = self.__sit     # 参数记录起始位置
        while(self.__game_num < 8):
            self.reset()          # 准备下一局对局
            print("sit:", self.__sit, "gamenum:", self.__game_num)
            self.__sit = (gamepara - self.__game_num) % 4

            print("欢迎来到{}{}场！".format(self.__wind, self.__game_num % 4 + 1))

            print("您这把是{}家.".format("东南西北"[self.__sit]))
            self.__game_num += 1
            if self.__game_num % 4 == 0:
                self.__wind = "南"    # 进行4局后进入南场
            if self.game() == 0:     # 连庄则对局数不增加
                self.__game_num -= 1

    def game(self):
        winner = -1
        print("本局的宝牌指示牌为：", self.__table.getDoraPointer()[0])
        self.__cardremain = 70   # 牌山余量
        self.__cardgiver = 0     # 当前出牌人
        self.__tilepointer = 52  # 牌山位置指针
        self.__GangCount = 0     # 记录开杠次数
        self.__Ganglist = []     # 杠牌
        self.__Chowlist = []     # 吃牌
        self.__PUNGlist = []     # 碰牌
        self.__Reddora = [0, 0, 0]  # 是否有赤宝牌
        while(self.__cardremain > 0 and winner == -1):
            brand = self.cardplay(self.__cardgiver)
            if brand == "自摸":
                return self.__sit
            if self.__cardgiver % 4 != self.__sit:
                self.can_gang(brand)
                self.can_pung(brand)
                if self.__cardgiver % 4 == (self.__sit + 3) % 4:
                    self.can_chow(brand)
                winner = self.can_Hu(brand)
            self.__cardgiver += 1
        return winner

    def cardplay(self, giver):
        self.__cardremain -= 1
        self.__tilepointer += 1
        curCard = self.__table.getTiles()[self.__tilepointer - 1]
        if giver % 4 != self.__sit:
            print("{}家打出{}".format("东南西北"[giver % 4], curCard))
            return self.__table.getTiles()[self.__tilepointer - 1]  # 如果不是玩家直接摸切
        # 如果是玩家本人
        self.handsShow()
        print("您摸到了：", curCard)
        # 判断是否能开杠
        self.can_gang(curCard)
        # 判断是否自摸
        if self.can_Hu(curCard, 1) != -1:
            return "自摸"

        self.__hands.append(curCard)
        self.brand()  # 舍牌
        self.handsSort(self.__hands)
        self.handsShow()
        print()

    def can_gang(self, card):
        if self.__cardremain == 0 or self.__GangCount == 4:
            return False
        if card not in self.__hands:
            return False
        index = self.__hands.index(card)
        if index > len(self.__hands) - 3:
            return False
        if self.__hands[index] == self.__hands[index + 1] == self.__hands[index + 2]:
            ifGANG = input("杠？Y/N")
            if ifGANG in "Yy1":
                self.GANG(card)
            return True
        return False

    def GANG(self, card):
        self.__cardremain -= 1
        self.__GangCount += 1
        self.__cardgiver = self.__sit
        for _ in range(3):
            self.__hands.remove(card)
        print("新的宝牌指示牌为：", self.__table.getDoraPointer()[self.__GangCount])
        self.cardplay(self.__sit)
        self.__Ganglist.append(card)
        self.__hands.append(self.__table.getTiles()[-self.__GangCount])

    def can_pung(self, card):
        if card not in self.__hands:
            return False
        index = self.__hands.index(card)
        if index > len(self.__hands) - 2:
            return False
        if self.__hands[index] == self.__hands[index + 1]:
            ifPUNG = input("碰？Y/N")
            if ifPUNG in "Yy1":
                self.PUNG(card)
            return True
        return False

    def PUNG(self, card):
        self.__cardgiver = self.__sit
        for _ in range(2):
            self.__hands.remove(card)
        self.__PUNGlist.append(card)
        self.brand()
        self.handsShow()
        print()

    def can_chow(self, card):
        if card[0] in "fd":
            return
        lis = []
        canchow = []
        num = int(card[0])
        for i in self.__hands:
            if i[1] == card[1]:
                lis.append(int(i[0]))
        lis.sort()
        # case 1: 1 2 (3)
        if num > 2:
            if num-1 in lis and num-2 in lis:
                print(str(num - 2)+card[1] + str(num - 1)+card[1] + card, card, end="  ")
                canchow.append(0)
        # case 2: 1 (2) 3
        if num > 1:
            if num-1 in lis and num+1 in lis:
                print(str(num - 1)+card[1] + card + str(num + 1)+card[1], card, end="  ")
                canchow.append(1)
        # case 3: (1) 2 3
        if num < 8:
            if num+1 in lis and num+2 in lis:
                print(card + str(num + 1)+card[1] + str(num + 2)+card[1], card, end="  ")
                canchow.append(2)

        if len(canchow) == 1:
            ifCHOW = input("吃？Y/N")
            if ifCHOW in "Yy1":
                self.CHOW(card, 0, canchow)
        elif len(canchow) > 1:
            ifCHOW = input("吃？1-{}/N".format(len(canchow)))
            if ifCHOW in "123":
                self.CHOW(card, eval(ifCHOW)-1, canchow)
        return canchow

    def CHOW(self, card, mode, lis):
        self.__cardgiver = self.__sit
        mode = lis[mode]
        if mode == 0:  # case 1: 1 2 (3)
           for i in [str(int(card[0])-2)+card[1], str(int(card[0])-1)+card[1], card]:
               if i != card:
                   self.__hands.remove(i)
               self.__Chowlist.append(i)
        elif mode == 1:  # case 2: 1 (2) 3
           for i in [str(int(card[0])-1)+card[1], card, str(int(card[0])+1)+card[1]]:
               if i != card:
                   self.__hands.remove(i)
               self.__Chowlist.append(i)
        elif mode == 2:  # case 3: (1) 2 3
           for i in [card, str(int(card[0])+1)+card[1], str(int(card[0])+2)+card[1]]:
               if i != card:
                   self.__hands.remove(i)
               self.__Chowlist.append(i)
        self.brand()
        self.handsShow()
        print()

    def can_Hu(self, card, Self=0):
        handstry = copy.deepcopy(self.__hands)
        handstry.append(card)
        if huJudge(self.handsSort(handstry), self.__Chowlist, self.__PUNGlist, self.__Ganglist):
            if Self:
                ifHU = input("自摸？Y/N")
            else:
                ifHU = input("胡？Y/N")
            if ifHU in "Yy1":
                self.__hands = handstry
                self.HU(handstry)
                return self.__sit
        return -1

    def HU(self, hands):
        print("胡牌手牌：", end='')
        self.handsShow()
        print("恭喜{}家获得胜利！".format("东南西北"[self.__sit]))

    def handsShow(self):
        print(self.__hands, end='  ')
        if self.__Ganglist != []:
            print("已杠：", end='')
            for i in self.__Ganglist:
                print(i*4, end=' ')
        if self.__PUNGlist != []:
            print("已碰：", end='')
            for i in self.__PUNGlist:
                print(i*3, end=' ')
        if self.__Chowlist != []:
            print("已吃：", end='')
            count = 0
            for i in self.__Chowlist:
                count += 1
                print(i, end='')
                if count % 3 == 0:
                    print(end=' ')

    def brand(self):
        brand = input("您要打出？")  # 舍牌
        if brand in self.__hands:
            self.__hands.remove(brand)
        elif brand in [str(i) for i in range(1, len(self.__hands)+1)]:
            self.__hands.pop(eval(brand) - 1)
        else:
            self.__hands.pop()

