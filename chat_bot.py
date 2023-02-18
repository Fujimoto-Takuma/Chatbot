#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import pandas as pd
import re
import oseti
import MeCab
import datetime
import random

# アクセストークンを入れてください
TOKEN = "###"

# 以下の部分を各自書き換えれば自分のシステムができる
# ctrl-cで強制終了

class SampleBot:
    def __init__(self):
        self.name = ""
        self.name_log = []
        self.counter = 0
        self.df = pd.read_csv("C:\\Users\\ikaya\\Dropbox\\nlp\\np_savett_cp.csv",encoding="Shift-JIS")
        self.junle = list(self.df['jun'].unique())
        self.jun = ""
        self.jun_log = []
        self.tim = ""
        self.tim_log = []
        self.price = 0
        self.price_log = []
        self.url = ""
        self.url_log = []
        self.sorry1 = ["あちゃ～、","うおお、まじっすか","うぉっと...","そうッスか...","ひっ...","ほんとすかぁ?"]
        self.sorry2 = ["それは申し訳ないことしちゃいましたね。","気に入ってくれると思ったんすけどね...","自分の分析が足りなかったっす...","怒らせちゃいましたかね...?","意外っすね"]
        self.sorry3 = ["次は気に入って貰えるように気を付けるっす...","もっとよく考えてからおすすめするようにするッス...","次はいい店紹介するんで楽しみにしててくださいッス!","ちょっと調子悪かったかもしれないッス笑","俺はいい店だと思ったんッスけどね..."]
        self.normal = ["もしかして微妙ッスか...?そんなわけないッスよね!","普通でしたッスか?","可もなく不可も無くっていう感じッスかね...?","多分気に入ってくれたっすよね! よね...?"]
        self.good1 = ["了解っす!","おお～マジっすか!","ありがとうございますッス!","嬉しいっす!","やったッス!"]
        self.good2 = ["やっぱりここ気に入ってもらえると思ってたッス!","俺の目に狂いは無かったッスね!","喜んで貰えたようで嬉しいッス!","お役に立てて感激ッス!","めっちゃ嬉しいッス!"]
        self.good3 = ["またいつでも聞きに来てくださいッス!","次もばっちりのお店紹介するッスよ!","もっと良い所紹介できるよう頑張るッス!","北千住の食べ物なら任せてくれッス!"]
        self.per = 0
        self.shop = ""
        self.shop_log = []
        self.pshop = ""
        self.yourname = ""
        self.shop_list = []
        self.rep = False
        print(self.junle)
        pass


    def start(self, bot, update):
        #update.message.reply_text()内にテキストを入れるとtelegramに送信
        update.message.reply_text('初めましてッス!俺はtakuma_botッス!良かったら名前教えて欲しいッス!')
        


    def message(self, bot, update):
        #print(self.df)
        print('カウンター：', self.counter)
        #print("aaa")
        # 挨拶
        # 名前確認
        if self.counter == 0:
            add = ""
            if len(self.shop_log) >= 1:
                add = "また話に来てくれて嬉しいッス!"
            if self.yourname:
                pass
            else:
                self.yourname = update.message.text
            text = self.yourname + f'さん!!{add}俺は北千住の食べ物に関しては知り尽くしてるンで、' + self.yourname  +"さんが今食べたいものすぐに教えられるッスよ!"
            update.message.reply_text(text)
            text = "まずは食べたいジャンルを教えてくださいッス!無ければ「ない」って教えてほしいッス!"
            update.message.reply_text(text)
            self.counter += 1
        
        # 好きな食べ物
        elif self.counter == 1:
            word = []
            tf = True
            tagger = MeCab.Tagger()
            tem = tagger.parse(update.message.text).split("\n")
            for te in tem:
                t = te.split("\n")
                word.append(t[0].split("\t")[0])
            print(word)
            for wor in word:
                if wor in self.junle:
                    self.jun = wor
                    text = self.jun + "ッスね!俺も好きッスよ!"
                    tf = False
                    break
            if "ない" in update.message.text and tf:
                text = "特に希望はないッスね!了解ッス!"
            elif tf:
                text = update.message.text + "はちょっとわかんないッスすいません..."
                self.jun = False
            update.message.reply_text(text)
            text = '次に昼ごはんか夜ごはんかを教えてほしいっす!いつでも良ければそういってほしいっす!'
            update.message.reply_text(text)
            self.counter += 1
        
        elif self.counter == 2:
            if "昼" in update.message.text:
                self.tim = "lunch"
                text = self.tim + 'ッスね!了解ッス!'
            elif "夜" in update.message.text:
                self.tim = "dinner"
                text = self.tim + 'ッスね!了解ッス!'
            else:
                text = "わっかりやした!!"
                self.tim = False
            update.message.reply_text(text)
            text = '最後に予算を教えて欲しいッス!算用数字でお願いするッス!特に決まってなかったら「ない」で大丈夫ッス!'
            update.message.reply_text(text)
            self.counter += 1
        
        elif self.counter == 3:
            if re.sub(r"\D", "",update.message.text).isdecimal():
                self.price = int(re.sub(r"\D", "",update.message.text))
                print(type(self.price))
                text = str(self.price) + "円っすね!これで探してきやす!見る準備が出来たら教えてくださいッス!"
            elif "ない" in update.message.text:
                text = "何円でもいいっすね!太っ腹っすね!探してくるんで準備できたら教えてくださいッス!"
            else:
                text = "それ本当に数字っすか...?とりあえず探してくるんで、準備ができたら反応くださいッス!"
                self.price = 1000000
                #######ここ分割?
            update.message.reply_text(text)
            self.counter += 1
            
            ##ここでなんかの処理をしてショップを出さなければいけない
        elif self.counter == 4:
            if self.rep == True:
                self.shop = self.shop_list.sample()
                self.url = self.shop["url"].iloc[0]
            else:
                self.url = self.search_shop()
            text = '探してきやした!それだとこんな店がおすすめッスかね!'
            update.message.reply_text(text)
            text = self.url
            update.message.reply_text(text)
            text = "このお店はどうっすか?"
            update.message.reply_text(text)
            self.counter += 1
        
        elif self.counter == 5:
            text = ""
            analyzer = oseti.Analyzer()
            r = analyzer.analyze(update.message.text)
            print(r)
            rev = sum(r)
            print(rev)
            if int(rev) == 0:
                text = random.choice(self.normal) + random.choice(self.good2) + random.choice(self.good3)
            elif int(rev) > 0:
                text = random.choice(self.good1) + random.choice(self.good2) + random.choice(self.good3)
            else:
                text = random.choice(self.sorry1) + random.choice(self.sorry2) + random.choice(self.sorry3)
            update.message.reply_text(text)
            text = "同じ条件で検索するッスか?[はい]か[いいえ]でお願いするッス!"
            update.message.reply_text(text)
            self.jun_log.append(self.jun)
            self.jun = ""
            self.tim_log.append(self.tim)
            self.tim = ""
            #self.price_log.append(self.price)
            #self.price = 0
            self.url_log.append(self.url)
            self.url = ""
            self.counter += 1
            self.name_log.append(self.name)
            self.name = ""
            self.shop_log.append(self.shop)
            self.shop = ""
            print(self.name_log)
        
        elif self.counter == 6:
            text = ""
            if "はい" in update.message.text:
                text = "了解ッス!ちょっと待っててくださいな!"
                self.rep = True
                update.message.reply_text(text)
                self.counter = 4
                return
            elif "いいえ" in update.message.text:
                text = "わかりやした!またいつでも聞いてくださいッス!"
                self.rep = False
                update.message.reply_text(text)
                self.per += 0.333
                print(self.per)
                if random.random() < self.per:
                    self.counter += 1
                    return
                else:
                    self.counter = 0
                    print(self.counter)
                    return
            else:
                text = "[はい]か[いいえ]でお願いするッス!"
                update.message.reply_text(text)
                return
            
            
            
        elif self.counter == 7:
            self.pshop = random.choice(self.shop_log)
            name = self.pshop["name"].iloc[0]
            jun = self.pshop["jun"].iloc[0]
            text = f"そういえば前オススメした「{name}」はどうだったスか!?美味しかったっすか? たしか{jun}が食べれるお店だったッスよね?"
            update.message.reply_text(text)
            #self.shop_log.remove(self.pshop)
            self.per = 0
            self.counter += 1
            
        elif self.counter == 8:
            jun = self.pshop["jun"].iloc[0]
            print(jun)
            text = ""
            analyzer = oseti.Analyzer()
            r = analyzer.analyze(update.message.text)
            print(r)
            rev = sum(r)
            if rev >= 0:
                text = f"楽しんでくれたようで何よりッス!やっぱり{jun}は最高に美味しいッスよね!次は一緒に連れてってくださいッス!"
            else:
                text = f"もしかしてあんまり好みじゃ無かったッスかね...?でも{jun}は他にも美味しいところ沢山あるんでまた今度他のお店も紹介しやすよ!!"
            update.message.reply_text(text)
            self.pshop = ""
            self.counter = 0
            
    def search_shop(self):
        url = ""
        dt_now = datetime.datetime.now()
        print(dt_now)
        now = dt_now.hour
        ans_df = self.df
        if not self.tim:
            if now <= 17:
                self.tim = "lunch"
            else:
                self.tim = "dinner"
        print(self.price)
        ans_df = self.df[self.tim].str.lstrip(" ")
        b = ans_df.str.split(" ",expand=True)
        b.columns = [f"{self.tim}_min",f"{self.tim}_max"]
        ans_df = pd.concat([self.df,b],axis=1)

        ####時間帯で不具合
        if self.jun:
            ans_df = ans_df[ans_df["jun"].str.contains(self.jun)]
        #print(ans_df)
        if "lunch" == self.tim:
            ans_df = ans_df[~ans_df["lunch_max"].str.contains("-")]
        
        if "dinner" == self.tim:
            ans_df = ans_df[~ans_df["dinner_max"].str.contains("-")]
        print(ans_df)
        
        ##最後にpriceの関数
        #ans_df[f"{self.tim}_max"] = ans_df[f"{self.tim}_max"].astype("int")
        print(ans_df[f"{self.tim}_max"])
        ans_df[f"{self.tim}_max"] = ans_df[f"{self.tim}_max"].apply(lambda x: x.replace(' ', '').replace('　', '')).astype('int')
        print(type(ans_df[f"{self.tim}_max"].iloc[0]))
        ans_df = ans_df[ans_df[f"{self.tim}_max"] <= self.price+500]
        
        #print(ans_df)
        if len(ans_df) == 0:
            return "やっぱり無かったっす..."
        self.shop_list = ans_df
        self.shop = ans_df.sample()
        self.name = self.shop["name"].iloc[0]
        url = self.shop["url"].iloc[0]
        return url
#telegramの動作コマンド

    def run(self):
        updater = Updater(TOKEN)
        
        dp = updater.dispatcher

        dp.add_handler(CommandHandler("start", self.start))#スラッシュで鬱コマンドが第一引数で設定できる。それをやると第2引数の関数が呼び出される。
        
        dp.add_handler(MessageHandler(Filters.text, self.message))
        
        updater.start_polling()

        updater.idle()


if __name__ == '__main__':
    mybot = SampleBot()
    mybot.run()
