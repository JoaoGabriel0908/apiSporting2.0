import datetime
import requests
import telebot
import time
import json


class BOT_Roleta:
    def __init__(self):
        self.game = "NAME_GAME"  # NAME GAME
        self.chat_id = 'CHAT_ID' # CHAT ID - GET IN >> https://t.me/chatIDrobot
        self.token = 'TOKEN_BOT' # TOKEN BOT -  GET IN >> https://t.me/BotFather
        self.url_API = 'SPORTINGBET-API' # API - GET IN >> https://t.me/sportingbetapi_bot
        self.link = "[CADASTRE-SE AGORA!](https://sshortly1.com/JpRYM9)"
        self.gales = 2 # QUATOS GALES
        self.hits = 3 # DIFICULDADE DA ESTRATÉGIA
        self.max_hate = 0
        self.win_hate = 0
        self.win_results = 0
        self.loss_results = 0
        self.empate_results = 0
        self.count_colum_01 = 0
        self.count_colum_02 = 0
        self.count_colum_03 = 0
        self.columns = {
            "03": [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
            "02": [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
            "01": [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34],
            }
        self.count = 0
        self.analisar = True
        self.protection = True
        self.message_delete = False
        self.direction_color = "None"
        self.bot = telebot.TeleBot(token=self.token, parse_mode="MARKDOWN", disable_web_page_preview=True)
        self.date_now = str(datetime.datetime.now().strftime("%d/%m/%Y"))
        self.check_date = self.date_now

    def restart(self):
        if self.date_now != self.check_date:
            print("Reiniciando bot!")
            self.check_date = self.date_now

            self.bot.send_sticker(
                self.chat_id,
                sticker="CAACAgEAAxkBAAEBbJJjXNcB92-_4vp2v0B3Plp9FONrDwACvgEAAsFWwUVjxQN4wmmSBCoE",
            )

            # ZERA OS RESULTADOS
            self.win_results = 0
            self.loss_results = 0
            self.empate_results = 0
            self.max_hate = 0
            self.win_hate = 0
            time.sleep(10)

            self.bot.send_sticker(
                self.chat_id,
                sticker="CAACAgEAAxkBAAEBPQZi-ziImRgbjqbDkPduogMKzv0zFgACbAQAAl4ByUUIjW-sdJsr6CkE",
            )
            self.results()
            return True
        else:
            return False

    def results(self):
        self.count_colum_01 = 0
        self.count_colum_02 = 0
        self.count_colum_03 = 0

        if self.win_results + self.empate_results + self.loss_results != 0:
            a = (
                100
                / (self.win_results + self.empate_results + self.loss_results)
                * (self.win_results + self.empate_results)
            )
        else:
            a = 0
        self.win_hate = f"{a:,.2f}%"

        self.bot.send_message(
            chat_id=self.chat_id,
            text=(
                f"""

► PLACAR = ✅{self.win_results} | 🟠{self.empate_results} | 🚫{self.loss_results} 
► Consecutivas = {self.max_hate}
► Assertividade = {self.win_hate}
    
    """
            ),
        )
        return

    def alert_sinal(self):
        message_id = self.bot.send_message(
            self.chat_id,
            text=f"""
⚠️ *ANALIZANDO POSSÍVEL ENTRADA...* ⚠️
""",
        ).message_id
        self.message_ids = message_id
        self.message_delete = True
        return

    def alert_gale(self):
        self.message_ids = self.bot.send_message(
            self.chat_id, text=f"""⚠️ Vamos para o {self.count}ª GALE"""
        ).message_id
        self.message_delete = True
        return

    def delete(self):
        if self.message_delete == True:
            self.bot.delete_message(chat_id=self.chat_id, message_id=self.message_ids)
            self.message_delete = False

    def send_sinal(self, colunas):
        self.analisar = False

        if colunas == 12:
            msg = "1 e 2"
        elif colunas == 13:
            msg = "1 e 3"
        elif colunas == 23:
            msg = "2 e 3"

        self.bot.send_message(
            chat_id=self.chat_id,
            text=(
                f"""
🎰  *ENTRADA CONFIRMADA* 🎰
🎮  {self.game}
🎯  Entrar nas colunas {msg}
⚔️  Cobrir o ZERO 🟢
🛟  Fazer {self.gales} proteções

📲  {self.link}
                                                          
    """))
        return

    def martingale(self, result, resultado):
        if result == "WIN":
            print(f"WIN")
            self.win_results += 1
            self.max_hate += 1
            # self.bot.send_sticker(self.chat_id, sticker='CAACAgEAAxkBAAECAkJk6IGeT9cIk6JjPCnC9q2aoB4OGQAC_wIAAlzNSEe28lhwKCgO0DAE')
            self.bot.send_message(
                chat_id=self.chat_id, text=(f"""✅✅✅ WIN! {resultado} ✅✅✅""")
            )

        elif result == "LOSS":
            self.count += 1

            if self.count > self.gales:
                print(f"LOSS")
                self.loss_results += 1
                self.max_hate = 0
                # self.bot.send_sticker(self.chat_id, sticker='CAACAgEAAxkBAAECAkZk6IGgljJmg8kv22NgsD6r8b2rnwAC4wIAAhqOSEd84O1M4ZV2rTAE')
                self.bot.send_message(chat_id=self.chat_id, text=(f"""🚫 RED"""))

            else:
                print(f"Vamos para o {self.count}ª gale!")
                self.alert_gale()
                return

        elif result == "EMPATE":
            print(f"EMPATE")
            self.empate_results += 1
            self.max_hate += 1
            # self.bot.send_sticker(self.chat_id, sticker='CAACAgEAAxkBAAECAkpk6IGkWrBptIKaai6JGoUeUhE7ZQACKQMAAk_-QUcZCw8psoK_3jAE')
            self.bot.send_message(chat_id=self.chat_id, text=(f"""✅✅✅ ZERO ✅✅✅"""))

        self.count = 0
        self.analisar = True
        self.results()
        self.restart()
        return

    def check_results(self, results):
        if results == 0:
            self.martingale("EMPATE", results)
            return

        elif (
            self.entradas == 23
            and results in self.columns["02"]
            or self.entradas == 23
            and results in self.columns["03"]
        ):
            self.martingale("WIN", results)
            return

        elif (
            self.entradas == 12
            and results in self.columns["01"]
            or self.entradas == 12
            and results in self.columns["02"]
        ):
            self.martingale("WIN", results)
            return

        elif (
            self.entradas == 13
            and results in self.columns["01"]
            or self.entradas == 13
            and results in self.columns["03"]
        ):
            self.martingale("WIN", results)
            return

        else:
            self.martingale("LOSS", results)
            return

    def estrategy(self, results):
        print(self.hora, results[0:20])

        if self.analisar == False:
            self.check_results(results[0])
            return

        elif self.analisar == True:
            if results[0] in self.columns["01"]:
                self.count_colum_01 += 1
                self.count_colum_02 = 0
                self.count_colum_03 = 0

            elif results[0] in self.columns["02"]:
                self.count_colum_01 = 0
                self.count_colum_02 += 1
                self.count_colum_03 = 0

            elif results[0] in self.columns["03"]:
                self.count_colum_01 = 0
                self.count_colum_02 = 0
                self.count_colum_03 += 1

            else:
                self.count_colum_01 = 0
                self.count_colum_02 = 0
                self.count_colum_03 = 0

            if self.count_colum_01 == self.hits:
                self.entradas = 23
                self.send_sinal(self.entradas)
                return

            elif self.count_colum_02 == self.hits:
                self.entradas = 13
                self.send_sinal(self.entradas)
                return

            elif self.count_colum_03 == self.hits:
                self.entradas = 12
                self.send_sinal(self.entradas)
                return

    def start(self):
        check = []

        while True:
            try:
                self.date_now = str(datetime.datetime.now().strftime("%d/%m/%Y"))
                self.hora = str(datetime.datetime.now().strftime("%H:%M"))

                results = []
                time.sleep(1)

                response = requests.get(self.url_API)
                json_data = json.loads(response.text)

                for i in json_data:
                    results.append(int(i))

                if check != results and len(results) > 5:
                    check = results
                    self.delete()
                    self.estrategy(results)

            except Exception as e:
                print(e)
                continue

script = BOT_Roleta()
script.start()
