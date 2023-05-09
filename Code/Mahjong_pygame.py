import copy
import pygame
import random
from GameTable import Gametable
from Rule import huJudge
from pygame.locals import *
from sys import exit


class Mahjong():
    def __init__(self):
        self.LoginPage()  # 游戏画面设置
        self.sitSet()     # 座次设置
        self.gameStart()  # 游戏开始

    def sitSet(self):
        self.__sit = random.randint(0, 3)
        # self.__sit = 0
        print("您这把{}起！".format("东南西北"[self.__sit]))

    def reset(self):
        print("\n\n正在清理牌桌...")
        self.__table = Gametable()  # 清理牌桌
        print("正在获取初始手牌...")
        self.__hands = self.getfHands(self.__sit)
        print(self.__hands)

    def getfHands(self, sit):
        hands = []
        base = sit * 4  # 摸牌起始位置
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
        self.__game_num = 0      # 当前对局数
        self.__wind = "东"       # 从东场开始
        gamepara = self.__sit   # 参数记录起始位置
        while (self.__game_num < 8):
            self.reset()  # 准备下一局对局
            print("sit:", self.__sit, "gamenum:", self.__game_num)
            self.__sit = (gamepara - self.__game_num) % 4
            print("欢迎来到{}{}场！".format(self.__wind, self.__game_num % 4 + 1))
            print("您这把是{}家.".format("东南西北"[self.__sit]))
            if (self.__game_num + 1) % 4 == 0:
                self.__wind = "南"  # 进行4局后进入南场
            if self.game() == 0:   # 连庄则对局数不增加
                self.__game_num -= 1
            self.__game_num += 1

    def game(self):
        winner = -1
        print("本局的宝牌指示牌为：", self.__table.getDoraPointer()[0])
        self.__cardremain = 70      # 牌山余量
        self.__cardgiver = 0        # 当前出牌人
        self.__tilepointer = 52     # 牌山位置指针
        self.__GangCount = 0        # 记录开杠次数
        self.__Ganglist = []        # 杠牌
        self.__Chowlist = []        # 吃牌
        self.__PUNGlist = []        # 碰牌
        self.__Reddora = [0, 0, 0]  # 是否有赤宝牌
        while (self.__cardremain > 0 and winner == -1):
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
        print("您摸到了：", curCard)
        # 判断是否能开杠
        self.can_gang(curCard)
        # 判断是否自摸
        if self.can_Hu(curCard, 1) != -1:
            return "自摸"
        self.__hands.append(curCard)
        self.brand()  # 舍牌
        self.handsSort(self.__hands)
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

            pygame.init()
            window_size = (880, 300)
            screen = pygame.display.set_mode(window_size, 0, 32)
            pygame.display.set_caption('GANG')  # 设置窗口标题
            screen.fill((255, 255, 255))
            self.DoraShow(screen)
            self.SitShow(screen)
            self.CardShow(screen)
            self.PlayerShow(screen)
            self.FuLuShow(screen)
            # 显示这张牌是哪家打出来的
            font_family = pygame.font.Font('C:/Windows/Fonts/SIMLI.TTF', 24)
            PlayerInfo = "{}家:".format("东南西北"[self.__cardgiver % 4])
            screen.blit(font_family.render(PlayerInfo, True, (0, 0, 0)), (145 + len(self.__hands) * 48, 80))
            # 显示这张牌
            image = pygame.image.load(card + '.png').convert()
            screen.blit(image, (155 + len(self.__hands) * 48, 120))
            pygame.display.update()
            flag = 0
            ifGANG = 0
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        flag = 1
                        pygame.quit()
                        exit()
                        break
                    x, y = pygame.mouse.get_pos()
                    screen.set_clip(170, 200, 100, 50)  # submit button's location
                    screen.fill((40, 225, 40))  # submit button's color
                    Login_name = '杠'
                    screen.blit(font_family.render(Login_name, True, (255, 255, 255)), (205, 213))
                    screen.set_clip(400, 200, 100, 50)  # submit button's location
                    screen.fill((39, 17, 39))           # submit button's color
                    Login_name = '跳过'
                    screen.blit(font_family.render(Login_name, True, (255, 255, 255)), (425, 213))
                    if 170 < x < 270 and 200 < y < 250 and event.type == MOUSEBUTTONDOWN:
                        screen.set_clip(170, 200, 100, 50)
                        screen.fill((84, 255, 159))
                        pygame.quit()
                        flag = 1
                        ifGANG = 1
                        break
                    elif 400 < x < 500 and 200 < y < 250 and event.type == MOUSEBUTTONDOWN:
                        screen.set_clip(400, 200, 100, 50)
                        screen.fill((84, 255, 159))
                        pygame.quit()
                        flag = 1
                        ifGANG = 0
                        break
                if flag:
                    break
                pygame.display.update()
            if ifGANG:
                self.GANG(card)
            return True
        return False

    def GANG(self, card):
        self.__cardremain -= 1         # 牌山存量-1
        self.__GangCount += 1          # 杠牌次数+1
        self.__cardgiver = self.__sit  # 出牌人变为自己
        for _ in range(3):
            self.__hands.remove(card)
        print("新的宝牌指示牌为：", self.__table.getDoraPointer()[self.__GangCount])
        self.__Ganglist.append(card)
        # 从王牌堆中摸一张牌
        self.__hands.append(self.__table.getTiles()[-self.__GangCount])
        self.brand()                   # 舍牌

    def can_pung(self, card):
        if card not in self.__hands:
            return False
        index = self.__hands.index(card)
        if index > len(self.__hands) - 2:
            return False
        if self.__hands[index] == self.__hands[index + 1]:
            pygame.init()
            window_size = (880, 300)
            screen = pygame.display.set_mode(window_size, 0, 32)
            pygame.display.set_caption('PUNG')  # 设置窗口标题
            screen.fill((255, 255, 255))
            self.DoraShow(screen)
            self.SitShow(screen)
            self.CardShow(screen)
            self.PlayerShow(screen)
            self.FuLuShow(screen)
            # 显示这张牌是哪家打出来的
            font_family = pygame.font.Font('C:/Windows/Fonts/SIMLI.TTF', 24)
            PlayerInfo = "{}家:".format("东南西北"[self.__cardgiver % 4])
            screen.blit(font_family.render(PlayerInfo, True, (0, 0, 0)), (145 + len(self.__hands) * 48, 80))
            # 显示这张牌
            image = pygame.image.load(card + '.png').convert()
            screen.blit(image, (155 + len(self.__hands) * 48, 120))
            pygame.display.update()
            flag = 0
            ifPUNG = 0
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        flag = 1
                        pygame.quit()
                        exit()
                        break
                    x, y = pygame.mouse.get_pos()
                    screen.set_clip(170, 200, 100, 50)
                    screen.fill((225, 17, 39))
                    Login_name = '碰'
                    screen.blit(font_family.render(Login_name, True, (255, 255, 255)), (205, 213))

                    screen.set_clip(400, 200, 100, 50)
                    screen.fill((39, 17, 39))
                    Login_name = '跳过'
                    screen.blit(font_family.render(Login_name, True, (255, 255, 255)), (425, 213))
                    if 170 < x < 270 and 200 < y < 250 and event.type == MOUSEBUTTONDOWN:
                        screen.set_clip(170, 200, 100, 50)
                        screen.fill((84, 255, 159))
                        pygame.quit()
                        flag = 1
                        ifPUNG = 1
                        break
                    elif 400 < x < 500 and 200 < y < 250 and event.type == MOUSEBUTTONDOWN:
                        screen.set_clip(400, 200, 100, 50)
                        screen.fill((84, 255, 159))
                        pygame.quit()
                        flag = 1
                        ifPUNG = 0
                        break
                if flag:
                    break
                pygame.display.update()
            if ifPUNG:
                self.PUNG(card)
            return True
        return False

    def PUNG(self, card):
        self.__cardgiver = self.__sit
        for _ in range(2):
            self.__hands.remove(card)
        self.__PUNGlist.append(card)
        self.brand()
        print()

    def can_chow(self, card):
        if card[0] in "fd":   # 如果是字牌则不能一定不能吃
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
        if len(canchow) == 0:
            return

        pygame.init()
        window_size = (880, 300)
        screen = pygame.display.set_mode(window_size, 0, 32)
        pygame.display.set_caption('CHOW')  # 设置窗口标题
        screen.fill((255, 255, 255))
        self.DoraShow(screen)
        self.SitShow(screen)
        self.CardShow(screen)
        self.PlayerShow(screen)
        self.FuLuShow(screen)
        # 显示这张牌是哪家打出来的
        font_family = pygame.font.Font('C:/Windows/Fonts/SIMLI.TTF', 24)
        PlayerInfo = "{}家:".format("东南西北"[self.__cardgiver % 4])
        screen.blit(font_family.render(PlayerInfo, True, (0, 0, 0)), (145 + len(self.__hands) * 48, 80))
        # 显示这张牌
        image = pygame.image.load(card + '.png').convert()
        screen.blit(image, (155 + len(self.__hands) * 48, 120))
        pygame.display.update()
        flag = 0
        ifCHOW = -1  # 选择吃模式
        postemp = 130
        # case 1: 1 2 (3)
        if 0 in canchow:
            image = pygame.image.load(str(num - 2) + card[1] + '.png').convert()
            screen.blit(image, (postemp, 180))
            image = pygame.image.load(str(num - 1) + card[1] + '.png').convert()
            screen.blit(image, (postemp + 1 * 45, 180))
            image = pygame.image.load(card + '.png').convert()
            screen.blit(image, (postemp + 2 * 45, 180))
        postemp += 190
        # case 2: 1 (2) 3
        if 1 in canchow:
            image = pygame.image.load(str(num - 1) + card[1] + '.png').convert()
            screen.blit(image, (postemp, 180))
            image = pygame.image.load(card + '.png').convert()
            screen.blit(image, (postemp + 1 * 45, 180))
            image = pygame.image.load(str(num + 1) + card[1] + '.png').convert()
            screen.blit(image, (postemp + 2 * 45, 180))
        postemp += 190
        # case 3: (1) 2 3
        if 2 in canchow:
            image = pygame.image.load(card + '.png').convert()
            screen.blit(image, (postemp, 180))
            image = pygame.image.load(str(num + 1) + card[1] + '.png').convert()
            screen.blit(image, (postemp + 1 * 45, 180))
            image = pygame.image.load(str(num + 2) + card[1] + '.png').convert()
            screen.blit(image, (postemp + 2 * 45, 180))
        postemp += 190
        if 0 in canchow:
            screen.set_clip(130 + 15, 240, 100, 50)
            screen.fill((40, 40, 200))
            Login_name = '吃'
            screen.blit(font_family.render(Login_name, True, (255, 255, 255)), (130 + 50, 253))
        if 1 in canchow:
            screen.set_clip(320 + 15, 240, 100, 50)
            screen.fill((40, 40, 200))
            Login_name = '吃'
            screen.blit(font_family.render(Login_name, True, (255, 255, 255)), (320 + 50, 253))
        if 2 in canchow:
            screen.set_clip(510 + 15, 240, 100, 50)
            screen.fill((40, 40, 200))
            Login_name = '吃'
            screen.blit(font_family.render(Login_name, True, (255, 255, 255)), (510 + 50, 253))
        screen.set_clip(postemp, 200, 100, 50)
        screen.fill((39, 17, 39))
        Login_name = '跳过'
        screen.blit(font_family.render(Login_name, True, (255, 255, 255)), (postemp + 25, 213))
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    flag = 1
                    pygame.quit()
                    exit()
                    break
                x, y = pygame.mouse.get_pos()
                if 100 < x < postemp and 200 < y < 300 and event.type == MOUSEBUTTONDOWN:
                    ifCHOW = int((x - 130)/190)
                    pygame.quit()
                    flag = 1
                    break
                elif postemp < x and 200 < y < 250 and event.type == MOUSEBUTTONDOWN:
                    pygame.quit()
                    flag = 1
                    break
            if flag:
                break
            pygame.display.update()
        if ifCHOW != -1:
            self.CHOW(card, ifCHOW, canchow)
        return canchow

    def CHOW(self, card, mode, lis):
        self.__cardgiver = self.__sit
        if mode == 0:  # case 1: 1 2 (3)
            for i in [str(int(card[0]) - 2) + card[1], str(int(card[0]) - 1) + card[1], card]:
                if i != card:
                    self.__hands.remove(i)
                self.__Chowlist.append(i)
        elif mode == 1:  # case 2: 1 (2) 3
            for i in [str(int(card[0]) - 1) + card[1], card, str(int(card[0]) + 1) + card[1]]:
                if i != card:
                    self.__hands.remove(i)
                self.__Chowlist.append(i)
        elif mode == 2:  # case 3: (1) 2 3
            for i in [card, str(int(card[0]) + 1) + card[1], str(int(card[0]) + 2) + card[1]]:
                if i != card:
                    self.__hands.remove(i)
                self.__Chowlist.append(i)
        self.brand()
        print()

    def can_Hu(self, card, Self=0):
        handstry = copy.deepcopy(self.__hands)
        handstry.append(card)
        if huJudge(self.handsSort(handstry), self.__Chowlist, self.__PUNGlist, self.__Ganglist):
            if Self:
                HU = "自摸"
            else:
                HU = "胡"
            pygame.init()
            window_size = (880, 300)
            screen = pygame.display.set_mode(window_size, 0, 32)
            pygame.display.set_caption('HU')  # 设置窗口标题
            screen.fill((255, 255, 255))
            self.DoraShow(screen)
            self.SitShow(screen)
            self.CardShow(screen)
            self.PlayerShow(screen)
            self.FuLuShow(screen)
            # 显示这张牌是哪家打出来的
            font_family = pygame.font.Font('C:/Windows/Fonts/SIMLI.TTF', 24)  # setting the font
            PlayerInfo = "{}家:".format("东南西北"[self.__cardgiver % 4])
            screen.blit(font_family.render(PlayerInfo, True, (0, 0, 0)), (145 + len(self.__hands) * 48, 80))
            # 显示这张牌
            image = pygame.image.load(card + '.png').convert()
            screen.blit(image, (155 + len(self.__hands) * 48, 120))
            pygame.display.update()
            flag = 0
            ifHU = 0
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        flag = 1
                        pygame.quit()
                        exit()
                        break
                    x, y = pygame.mouse.get_pos()
                    screen.set_clip(170, 200, 100, 50)
                    screen.fill((225, 225, 225))
                    screen.blit(font_family.render(HU, True, (255, 10, 10)), (215-10*len(HU), 213))

                    screen.set_clip(400, 200, 100, 50)
                    screen.fill((39, 17, 39))
                    Login_name = '跳过'
                    screen.blit(font_family.render(Login_name, True, (255, 255, 255)), (425, 213))
                    if 170 < x < 270 and 200 < y < 250 and event.type == MOUSEBUTTONDOWN:
                        screen.set_clip(170, 200, 100, 50)
                        screen.fill((84, 255, 159))
                        pygame.quit()
                        flag = 1
                        ifHU = 1
                        break
                    elif 400 < x < 500 and 200 < y < 250 and event.type == MOUSEBUTTONDOWN:
                        screen.set_clip(400, 200, 100, 50)
                        screen.fill((84, 255, 159))
                        pygame.quit()
                        flag = 1
                        ifHU = 0
                        break
                if flag:
                    break
                pygame.display.update()
            if ifHU:
                self.__hands = handstry
                self.HU(handstry)
                return self.__sit
        return -1

    def HU(self, hands):
        print("胡牌手牌：", end='')
        if self.__Ganglist != []:
            for i in self.__Ganglist:
                self.__hands.append(i)
                self.__hands.append(i)
                self.__hands.append(i)
                self.__hands.append(i)
        if self.__PUNGlist != []:
            for i in self.__PUNGlist:
                self.__hands.append(i)
                self.__hands.append(i)
                self.__hands.append(i)
        if self.__Chowlist != []:
            for i in self.__Chowlist:
                self.__hands.append(i)

        pygame.init()
        window_size = (880, 300)
        screen = pygame.display.set_mode(window_size, 0, 32)
        pygame.display.set_caption('HU SHOW')  # 设置窗口标题
        screen.fill((255, 255, 255))  # background color
        font_family = pygame.font.Font('C:/Windows/Fonts/STXINGKA.TTF', 24)  # setting the font
        GameInfo = "{}家胡牌！胡牌手牌：".format("东南西北"[self.__sit])
        screen.blit(font_family.render(GameInfo, True, (0, 0, 0)), (130, 80))
        self.PlayerShow(screen)
        self.DoraShow(screen)
        self.SitShow(screen)
        self.CardShow(screen)

        flag = 0
        while True:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    flag = 1
                    pygame.quit()
                    break
                elif event.type == QUIT:
                    flag = 1
                    pygame.quit()
                    exit()
                    break
            if flag:
                break
        print("恭喜{}家获得胜利！".format("东南西北"[self.__sit]))

    def handsShow(self):
        print(self.__hands, end='  ')
        if self.__Ganglist != []:
            print("已杠：", end='')
            for i in self.__Ganglist:
                print(i * 4, end=' ')
        if self.__PUNGlist != []:
            print("已碰：", end='')
            for i in self.__PUNGlist:
                print(i * 3, end=' ')
        if self.__Chowlist != []:
            print("已吃：", end='')
            count = 0
            for i in self.__Chowlist:
                count += 1
                print(i, end='')
                if count % 3 == 0:
                    print(end=' ')
        pygame.init()
        window_size = (880, 300)
        screen = pygame.display.set_mode(window_size, 0, 32)
        pygame.display.set_caption('Mahjong')  # 设置窗口标题
        screen.fill((255, 255, 255))
        self.PlayerShow(screen)
        self.DoraShow(screen)
        self.SitShow(screen)
        self.CardShow(screen)
        self.FuLuShow(screen)

        flag = 0
        while True:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    flag = 1
                    pygame.quit()
                    break
                elif event.type == QUIT:
                    flag = 1
                    pygame.quit()
                    exit()
                    break
            if flag:
                break

    def FuLuShow(self, screen):
        postemp = 840   # 位置辅助变量
        if self.__Ganglist != []:
            for i in self.__Ganglist:
                image = pygame.image.load(i + '.png').convert()
                screen.blit(image, (postemp, 250))
                screen.blit(image, (postemp - 48, 250))
                screen.blit(image, (postemp - 48 * 2, 250))
                screen.blit(image, (postemp - 48 * 3, 250))
                postemp -= 202
                pygame.display.update()
        if self.__PUNGlist != []:
            for i in self.__PUNGlist:
                image = pygame.image.load(i + '.png').convert()
                screen.blit(image, (postemp, 250))
                screen.blit(image, (postemp - 48, 250))
                screen.blit(image, (postemp - 48 * 2, 250))
                postemp -= 154
                pygame.display.update()
        if self.__Chowlist != []:
            length = int(len(self.__Chowlist) / 3)
            for i in range(length):
                image = pygame.image.load(self.__Chowlist[i * 3 + 2] + '.png').convert()
                screen.blit(image, (postemp, 250))
                image = pygame.image.load(self.__Chowlist[i * 3 + 1] + '.png').convert()
                screen.blit(image, (postemp - 48, 250))
                image = pygame.image.load(self.__Chowlist[i * 3] + '.png').convert()
                screen.blit(image, (postemp - 48 * 2, 250))
                postemp -= 154
                pygame.display.update()

    def CardShow(self, screen):
        for i in range(len(self.__hands)):
            image = pygame.image.load(self.__hands[i]+'.png').convert()
            screen.blit(image, (130 + i * 48, 120))
            pygame.display.update()

    def PlayerShow(self, screen):
        font_family = pygame.font.Font('C:/Windows/Fonts/timesi.ttf', 20)  # setting the font
        PlayerInfo = "Player: {}".format(self.__playername)
        screen.blit(font_family.render(PlayerInfo, True, (0, 0, 0)), (5, 270))

    def DoraShow(self, screen):
        i = 0
        while i < self.__GangCount + 1:
            image = pygame.image.load(self.__table.getDoraPointer()[i] + '.png').convert()
            screen.blit(image, (i * 48, 0))
            pygame.display.update()
            i += 1
        while i < 5:
            image = pygame.image.load('hidden.png').convert()
            screen.blit(image, (i * 48, 0))
            pygame.display.update()
            i += 1

    def SitShow(self, screen):
        font_family = pygame.font.Font('C:/Windows/Fonts/SIMLI.TTF', 24)  # setting the font
        GameInfo = "{}{}场  {}家".format(self.__wind, self.__game_num % 4 + 1, "东南西北"[self.__sit])
        screen.blit(font_family.render(GameInfo, True, (0, 0, 0)), (5, 55))

    def brand(self):
        brand = len(self.__hands)-1
        pygame.init()
        window_size = (880, 300)
        screen = pygame.display.set_mode(window_size, 0, 32)
        pygame.display.set_caption('BRAND')  # 设置窗口标题
        screen.fill((255, 255, 255))
        self.PlayerShow(screen)
        self.DoraShow(screen)
        self.SitShow(screen)
        self.FuLuShow(screen)
        image = pygame.image.load(self.__hands[len(self.__hands)-1] + '.png').convert()
        screen.blit(image, (150 + (len(self.__hands)-1) * 48, 120))
        for i in range(len(self.__hands)-1):
            image = pygame.image.load(self.__hands[i]+'.png').convert()
            screen.blit(image, (130 + i * 48, 120))
            pygame.display.update()
        pygame.display.update()
        flag = 0
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    flag = 1
                    pygame.quit()
                    exit()
                    break
                x, y = pygame.mouse.get_pos()
                if 130 < x < 130 + len(self.__hands) * 48 and 120 < y < 250 and event.type == MOUSEBUTTONDOWN:
                    brand = int((x-130)/48)
                    pygame.quit()
                    flag = 1
                    break
                elif event.type == MOUSEBUTTONDOWN:
                    pygame.quit()
                    flag = 1
                    break
            if flag:
                break
            pygame.display.update()
        self.__hands.pop(brand)

    # 图形化窗口
    def LoginPage(self):
        pygame.init()

        window_size = (1280, 750)
        screen = pygame.display.set_mode(window_size, 0, 32)
        pygame.display.set_caption('Mahjong')  # 设置窗口标题
        message_box = []
        back_image = pygame.image.load('Mahjong.png').convert()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                screen.fill((255, 255, 255))  # background color
                screen.blit(back_image, (230, 30))
                screen.set_clip(470, 400, 300, 50)  # location
                screen.fill((59, 37, 59))  # color
                x, y = pygame.mouse.get_pos()
                if 500 < x < 800 and 400 < y < 450:
                    if event.type == KEYDOWN:
                        key_num = event.key
                        if 48 <= key_num <= 57:
                            message_box.append(chr(key_num))  # get the value of keyboard
                        elif 97 <= key_num <= 122:
                            message_box.append(chr(key_num))
                        elif key_num == 46:
                            message_box.append(".")
                        elif key_num == 8 and len(message_box) != 0:
                            message_box.pop()
                self.__playername = ''.join(message_box)  # join the list value to a string
                font_family = pygame.font.Font('C:/Windows/Fonts/times.ttf', 26)  # setting the font
                ID_name = ' ID: '
                screen.blit(font_family.render(ID_name, True, (255, 255, 255)), (480, 410))
                screen.blit(font_family.render(self.__playername, True, (255, 255, 255)), (560, 410))
                screen.set_clip(470, 470, 300, 50)
                screen.fill((39, 17, 39))
                Login_name = 'Start!'
                screen.blit(font_family.render(Login_name, True, (255, 255, 255)), (585, 480))
                if 470 < x < 770 and 470 < y < 520 and event.type == MOUSEBUTTONDOWN:
                    screen.set_clip(470, 470, 300, 50)
                    screen.fill((84, 255, 159))
                    pygame.quit()
                    return self.Welcome()
            pygame.display.update()

    def Welcome(self):
        pygame.init()
        print('Welcome to Mahjong World! {}'.format(self.__playername))
        window_size = (1280, 750)
        screen = pygame.display.set_mode(window_size, 0, 32)
        pygame.display.set_caption('Mahjong Welcome')  # 设置窗口标题

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                screen.fill((255, 255, 255))
                font_family = pygame.font.Font('C:/Windows/Fonts/times.ttf', 56)  # setting the font
                WelcomeSentence = "Hello! {}".format(self.__playername)
                screen.blit(font_family.render('Welcome to Mahjong World!', True, (82, 15, 173)), (295, 230))
                screen.blit(font_family.render(WelcomeSentence, True, (26, 31, 179)), (548-len(self.__playername)*16, 160))
                screen.set_clip(470, 370, 300, 50)  # submit button's location
                screen.fill((10, 97, 163))  # submit button's color

                font_family = pygame.font.Font('C:/Windows/Fonts/times.ttf', 26)  # setting the font
                screen.blit(font_family.render('Play!', True, (255, 255, 255)), (590, 380))
                pygame.display.update()
                x, y = pygame.mouse.get_pos()
                if 470 < x < 770 and 370 < y < 420 and event.type == MOUSEBUTTONDOWN:
                    screen.set_clip(470, 370, 300, 50)
                    screen.fill((10, 97, 163))
                    pygame.quit()
                    return
