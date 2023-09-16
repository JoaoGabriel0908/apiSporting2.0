import datetime
import requests
import telebot
import time
import json
import csv

class BOT_Spaceman:
    def __init__(self):
        self.game = "NAME_GAME"  # NAME GAME
        self.chat_id = 'CHAT_ID' # CHAT ID - GET IN >> https://t.me/chatIDrobot
        self.token = 'TOKEN_BOT' # TOKEN BOT -  GET IN >> https://t.me/BotFather
        self.url_API = 'SPORTINGBET-API' # API - GET IN >> https://t.me/sportingbetapi_bot
        self.link = "[CADASTRE-SE AGORA!](https://sshortly1.com/JpRYM9)"
        self.gales = 2
        self.alvo = 0
        self.count = 0
        self.max_hate = 0
        self.win_hate = 0
        self.win_results = 0
        self.loss_results = 0
        self.message_delete = False
        self.analisar = True
        self.bot = telebot.TeleBot(token=self.token, parse_mode='MARKDOWN', disable_web_page_preview = True)
        self.date_now = str(datetime.datetime.now().strftime("%d/%m/%Y"))
        self.check_date = self.date_now

    def restart(self):
        if self.date_now != self.check_date:           
            print('Reiniciando bot!')
            self.check_date = self.date_now
            
            self.bot.send_sticker(
                self.chat_id, sticker='CAACAgEAAxkBAAEBbJJjXNcB92-_4vp2v0B3Plp9FONrDwACvgEAAsFWwUVjxQN4wmmSBCoE')

            #ZERA OS RESULTADOS
            self.win_results = 0
            self.loss_results = 0
            self.max_hate = 0
            self.win_hate = 0
            time.sleep(10)

            self.bot.send_sticker(
                self.chat_id, sticker='CAACAgEAAxkBAAEBPQZi-ziImRgbjqbDkPduogMKzv0zFgACbAQAAl4ByUUIjW-sdJsr6CkE')
            self.results()
            return True
        else:
            return False

    def results(self):

        if self.win_results + self.loss_results != 0:
            a = 100 / (self.win_results + self.loss_results) * self.win_results 
        else:
            a = 0
        self.win_hate = (f'{a:,.2f}%')


        self.bot.send_message(chat_id=self.chat_id, text=(f'''

► PLACAR GERAL = ✅{self.win_results}  |  🚫{self.loss_results} 
► Consecutivas = {self.max_hate}
► Assertividade = {self.win_hate}
    
    '''))
        return
       
    def alert_sinal(self):
        message_id = self.bot.send_message(
            self.chat_id, text='''
⚠️ ANALISANDO, FIQUE ATENTO!!!
''').message_id
        self.message_ids = message_id
        self.message_delete = True
        return
    
    def alert_gale(self):
        self.message_ids = self.bot.send_message(self.chat_id, text=f'''⚠️ Vamos para o {self.count}ª GALE''').message_id
        self.message_delete = True
        return

    def delete(self):
        if self.message_delete == True:
            self.bot.delete_message(chat_id=self.chat_id,
                                    message_id=self.message_ids)
            self.message_delete = False
      
    def send_sinal(self, finalnum):
        self.analisar = False
        self.bot.send_message(chat_id=self.chat_id, text=(f'''

🎲 *ENTRADA CONFIRMADA!*

🎰 Apostar após o {finalnum}x
🟡 Sair em {self.alvo}x 
🔁 Fazer até {self.gales} gales

📱 *{self.game}* '''f'{self.link}''''

    '''))
        return

    def martingale(self, result):

        if result == "WIN":
            print(f"WIN")
            self.win_results += 1
            self.max_hate += 1
            self.bot.send_message(chat_id=self.chat_id, text=(f'''✅✅✅ WIN ✅✅✅'''))
            # self.bot.send_sticker(self.chat_id, sticker='CAACAgEAAxkBAAEBuhtkFBbPbho5iUL3Cw0Zs2WBNdupaAACQgQAAnQVwEe3Q77HvZ8W3y8E')
        
        elif result == "LOSS":
            self.count += 1
            
            if self.count > self.gales:
                print(f"LOSS")
                self.loss_results += 1
                self.max_hate = 0
                self.bot.send_message(chat_id=self.chat_id, text=(f'''🚫🚫🚫 LOSS 🚫🚫🚫'''))
                #self.bot.send_sticker(self.chat_id, sticker='CAACAgEAAxkBAAEBuh9kFBbVKxciIe1RKvDQBeDu8WfhFAACXwIAAq-xwEfpc4OHHyAliS8E')

            else:
                print(f"Vamos para o {self.count}ª gale!")
                self.alert_gale()
                return
            

        self.count = 0
        self.analisar = True
        self.results()
        self.restart()
        return

    def check_results(self, results):

        if results >= self.alvo:
            self.martingale('WIN')
            return
        
        elif results < self.alvo:
            self.martingale('LOSS')
            return

    def estrategy(self, results):
        print(datetime.datetime.now().strftime("%H:%M/%Y"), self.game)

        if self.analisar == False:
            self.check_results(results[0])
            return

        elif self.analisar == True:  
            with open('strategies_spaceman.csv', newline='') as f:
                reader = csv.reader(f)

                ESTRATEGIAS = []

                for row in reader:
                    string = str(row[0])

                    split_saida = string.split('=')
                    split_string = split_saida[0].split('-')

                    listx = []
                    for i in split_string:
                        listx.append(float(i))

                    values = listx
                    values.reverse()
                    dictionary = {'PADRAO': values, 'SAIDA': float(split_saida[1])}
                    ESTRATEGIAS.append(dictionary)


                for i in ESTRATEGIAS:
                    lista = results[0:len(i['PADRAO'])]
                    self.alvo = i['SAIDA']
                    count = 0
                    sinal = False

                    for i in i['PADRAO']:
                        try:
                            if i >= lista[count]:
                                sinal = True
                                count += 1
                            else:
                                sinal = False
                                break
                        except:
                            sinal = False
                            print("Resultados incompletos")
                            break
                   
                    if sinal:
                        print("Sinal ENCONTRADO!")
                        self.send_sinal(results[0])
                        return

            if results[0] <= 2.0 and results[1] <= 2.0 and results[2] <= 2.0:
                print("Sinal ENCONTRADO!")
                self.alvo = 1.5
                self.send_sinal(results[0])
                return
            
            if results[0] <= 2.0 and results[1] <= 2.0:
                self.alert_sinal()
                return

    def start(self):
        check = []
        while True:
            try:
                self.date_now = str(datetime.datetime.now().strftime("%d/%m/%Y"))

                response = requests.get(self.url_API)
                json_data = json.loads(response.text)
       
                results = []
                for i in json_data:
                    results.append(float(i))

                if check != results and len(results) > 5:
                    check = results
                    self.delete()
                    self.estrategy(results)
                
                time.sleep(1)
            except Exception as e:
                print("ERROR - 404!", e)
                continue

scraper = BOT_Spaceman()
scraper.start()