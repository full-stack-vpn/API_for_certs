import paramiko

class SSHClientManager:
    def __init__(self, hostname, port, username, password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        self.client.connect(self.hostname, self.port, self.username, self.password)

    def disconnect(self):
        self.client.close()

    def execute_command(self, command, input_data=None):
        stdin, stdout, stderr = self.client.exec_command(command)
        if input_data:
            stdin.write(input_data)
            stdin.flush()
        return stdout.read().decode(), stderr.read().decode()


class SSHCommandExecutor:
    def __init__(self, ssh_client_manager, option, name, duration):
        self.ssh_client_manager = ssh_client_manager
        self.option = option
        self.name = name
        self.duration = duration

    def prepare_input_data(self):
        return f"{self.option}\n{self.name}\n{self.duration}\n"

    def run(self):
        command = 'ikev2.sh'
        input_data = self.prepare_input_data()
        stdout, stderr = self.ssh_client_manager.execute_command(command, input_data)
        print(stdout)
        print("STDERR:", stderr)


if __name__ == "__main__":
    hostname = '178.208.80.140' # здесь указываем сервер для выдачи сертификата
    port = 22
    username = 'root'
    password = 'QtA3K9fbXJ'

    # Параметры команды
    option = '1' # НЕ ТРОГАТЬ НИ В КОЕМ СЛУЧАЕ ЭТО ОПЦИЯ ДЛЯ ДОБАВЛЕНИЯ КЛИЕНТА
    name = 'hfhgufdh' # имя клииента, КАЖДЫЙ РАЗ РАЗНОЕ ИЛИ ВСЕ ПОЛЕТИТ К ЧЕРТЯМ
    duration = '2' # валидность сертификата в месяцах

    # Создание клиента и соединения
    ssh_client_manager = SSHClientManager(hostname, port, username, password)
    ssh_client_manager.connect()
    # Выполнение команд
    command_executor = SSHCommandExecutor(ssh_client_manager, option, name, duration)
    command_executor.run()
    # Порвать соедпинение
    ssh_client_manager.disconnect()
