import paramiko
import telebot
import time

bot = telebot.('')
user_answers = {}

@bot.message_handler(commands=['register'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать в сервис подключения новых серверов для развёртывания IKEv2.")
    bot.send_message(message.chat.id, "Каков адрес нового сервера?")
    bot.register_next_step_handler(message, ask_question_2)

def ask_question_2(message):
    user_answers['ip'] = message.text
    bot.send_message(message.chat.id, "Какой логин использовать?")
    bot.register_next_step_handler(message, ask_question_3)

def ask_question_3(message):
    user_answers['login'] = message.text
    bot.send_message(message.chat.id, "Какой пароль для доступа на сервер?")
    bot.register_next_step_handler(message, execute_command)

def execute_command(message):
    user_answers['password'] = message.text

    # Пробуем подключиться к SSH  выполнить команды
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(user_answers['ip'], username=user_answers['login'], password=user_answers['password'])

        stdin, stdout, stderr = ssh.exec_command('wget https://get.vpnsetup.net -O vpn.sh && sudo sh vpn.sh -y')
        output1 = stdout.read().decode('utf-8')
        err1 = stdout.read().decode()
        time.sleep(30)

        stdin, stdout, stderr = ssh.exec_command('ikev2.sh --auto')
        output2 = stdout.read().decode('utf-8')
        err2 = stdout.read().decode()


        ssh.close()

        bot.send_message(message.chat.id, f"wget:\n{output1}\nPossible errors:\n{err1}")
        bot.send_message(message.chat.id, f"ikev2.sh:\n{output2}\nPossible errors:\n{err2}")

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при подключении к серверу: {str(e)}")

bot.polling()
