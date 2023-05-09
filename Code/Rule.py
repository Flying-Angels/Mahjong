import copy


def huJudge(hands, Chowlis, Punglis, Ganglis):
    count = len(Chowlis)/3 + len(Punglis) + len(Ganglis)
    if count == 0:
        if nanaJudge(hands) or kokushimusoJudge(hands):
            return True
    return tanyaoJudge(hands, count)

def nanaJudge(hands):
    i = 0
    temp = "0"
    while i < 12:
        if temp == hands[i]:
            return False
        if hands[i] != hands[i+1]:
            return False
        temp = hands[i]
        i += 2

    return True

def kokushimusoJudge(hands):
    handscopy = copy.deepcopy(hands)
    yaolist = ["1m", "9m", "1p", "9p", "1s", "9s", "d1", "d2", "d3", "f1", "f2", "f3", "f4"]
    for i in yaolist:
        if i in handscopy:
            handscopy.remove(i)
    if len(handscopy) == 1 and handscopy[0] in yaolist:
        return True
    else:
        return False

def tanyaoJudge(hands, count):
    for i in hands:
        if i[0] in "19fd":
            return False
    i = 0
    while(i < len(hands)-1):
        handscopy = copy.deepcopy(hands)
        if hands[i] == hands[i + 1]:
            handscopy.pop(i+1)
            handscopy.pop(i)
            if NormalJudge(handscopy, count):
                return True
        i += 1
    return False

def NormalJudge(hands, count):  # 如果是一般型
    i = 0
    while count < 4 and i < len(hands) - 2:
        if hands[i+2] == hands[i+1] == hands[i]:  # 刻子判断
            count += 1
            for _ in range(3):
                hands.pop(i)
            i -= 1
        else:   # 顺子判断
            if str(int(hands[i][0])+1) + hands[i][1] in hands and str(int(hands[i][0])+2) + hands[i][1] in hands:
                count += 1
                hands.remove(str(int(hands[i][0]) + 1) + hands[i][1])
                hands.remove(str(int(hands[i][0]) + 2) + hands[i][1])
                hands.pop(i)
                i -= 1
            else:
                return False
        i += 1
    return True





# hutest = ["2m", "2m", "2m", "3m", "3m", "4m", "4m", "5m", "5m", "6m", "6m", "7m", "7m", "8m"]
# hutest = ["1m", "1m", "1m", "2m", "3m", "4m", "5m", "5m", "6m", "7m", "8m", "9m", "9m", "9m"]
# guotest = ["1m", "9m", "1p", "9p", "1s", "9s", "d1", "d2", "d3", "f1", "f2", "f3", "f4", "f4"]
# nanatest = ["1m", "1m", "9m", "9m", "1p", "1p", "9p", "9p", "1s", "1s", "9s", "9s","d1","d1"]
# print(huJudge(hutest, [], [], []))
