# -*- coding: utf-8 -*-
import re

class Password(object):
    def __init__(self, password):
        self.password = password
        self.chartypes = self.password2chartypes()

    def __str__(self):
        return self.password
    
    def password2chartypes(self):
        """
        パスワード文字列を文字タイプの文字列に変換する。
        例： "hoge_2_HOGE" -> "LLLLSNSUUUU"
        """
        chartypes = str()
        for char in self.password:
            if char.isalpha() and char.isupper():
                chartypes += 'U'
            elif char.isalpha() and char.islower():
                chartypes += 'L'
            elif char.isdigit():
                chartypes += 'N'
            else:
                chartypes += 'S'
        return chartypes

    def password_length(self):   #パスワードの桁数
        return len(self.chartypes)

    def num_upper(self):         #大文字の桁数
        return self.chartypes.count('U')

    def num_lower(self):         #小文字の桁数
        return self.chartypes.count('L')

    def num_number(self):        #数字の桁数
        return self.chartypes.count('N')

    def num_symbol(self):        #記号の桁数
        return self.chartypes.count('S')

    def short_password(self):
        '''
        パスワードが8文字以下の場合、桁数の差を返す
        '''
        if len(self.chartypes) < 8:
            return 8- len(self.chartypes)
        else:
            return 0

    def single_chartype(self):
        '''
        一種の文字タイプのみのパスワードの場合、文字列の桁数を返す
        '''
        if re.match(r"^UU+$|^LL+$|^NN+$|^SS+$", self.chartypes) != None:
            return len(self.chartypes)
        else:
            return 0

    def seq_chartype(self):
        '''
        文字タイプが連続している場合、連続した部分文字列を返す。
        例：　"LLSUUUUUNNNN" -> ['LL', 'UUUUU', 'NNNN'] -> [1, 4, 3] -> return 8
        '''        
        seq_list = list()
        seq_list.extend(re.findall(r"UU+", self.chartypes))
        seq_list.extend(re.findall(r"LL+", self.chartypes))        
        seq_list.extend(re.findall(r"NN+", self.chartypes))
        seq_list.extend(re.findall(r"SS+", self.chartypes))
        seq_digit_list = [len(d)-1 for d in seq_list]        
        return sum(seq_digit_list)

    def check(self):
        """
        各チェックポイントごとに加算スコア、減算スコアを合計し、
        (加算スコア/(加算スコア＋減算スコア))*100をパスワード強度とする。
        0%～50% => 弱
        ～80% => 中
        ～100% => 強
        """
        positive_score, negative_score = float(), float()

        #加算スコア
        positive_score += self.password_length() * 1
        positive_score += self.num_upper() * 1
        positive_score += self.num_lower() * 1
        positive_score += self.num_number() * 2
        positive_score += self.num_symbol() * 3

        #減算スコア
        negative_score += self.short_password() * 4
        negative_score += self.single_chartype() * 4
        negative_score += self.seq_chartype() * 4

        #結果
        result = positive_score / (positive_score + negative_score) * 100
        print "positive: ", positive_score
        print "negative: ", negative_score
        print "result: ", result
        
        if result <= 50:
            return "弱"
        elif 50 < result <= 80:
            return "中"
        elif 80 < result <= 100:
            return "強"
