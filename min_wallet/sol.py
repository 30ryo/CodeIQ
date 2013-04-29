def min_coinset(coinlist, amount):
    """
    与えられた金額に対して、最小構成の硬貨のリストを返す。
    """
    coinset, remain = list(), amount
    for coin in coinlist:
        coinset.append(remain // coin)
        remain = remain % coin
    return coinset

def min_wallet(wallet, price):
    """
    input:
        *wallet 支払い前の財布の金額
        *price 支払い額
    var:
        *coinlist 硬貨の単位のリスト
        （※coinlistを書き換えることで紙幣や外国通貨にも対応可能）
        *wallet_coin 財布の最小構成
        *price_coin 支払金額の最小構成
        *subtracted_coin 支払金額の最小構成に対して、不足している財布の硬貨と枚数
        *payment_coin 支払うことが可能な最小構成の硬貨構成
        *carryover 不足している硬貨について、上位の硬貨に繰り上げるフラグ(※True=1, False=0)
    return:
        お釣りが最小硬貨枚数となる支払額
    """

    coinlist = [500,100,50,10,5,1]
    wallet_coin, price_coin = min_coinset(coinlist, wallet),\
                              min_coinset(coinlist, price)
    subtracted_coin = [wallet_coin[i] - price_coin[i] for i in range(len(wallet_coin))]
    payment_coin, carryover, payment = [], bool(), int()

    #下位の硬貨から順番に使用する枚数を計算していく。
    for i in range(len(wallet_coin)):
        
        #下位の硬貨からの繰り上がりも考慮して、その単位の硬貨が足りているかチェックする。
        num_coin = subtracted_coin.pop() - carryover

        #足りていない場合は、その硬貨は使用しないので、0枚をpayment_coinに追加する。
        if num_coin < 0:
            payment_coin.insert(0,0)
            carryover = True
        #足りている場合は、繰り上がりを考慮して使用する枚数をpayment_coinに追加する。
        else:
            payment_coin.insert(0,price_coin[5-i]+carryover)
            carryover = False

    #硬貨毎の合計金額を計算。
    payment = [coinlist[i] * payment_coin[i] for i in range(len(wallet_coin))]

    #支払い額の合計を出力する。
    return sum(payment)

print min_wallet(834, 157)	#設問の例題
print min_wallet(421, 201)	#ぴったり払える場合
print min_wallet(500, 111)	#500円玉1枚しかありえない。
print min_wallet(666, 243)	#5,50,500の単位をきっちり使えるか。
