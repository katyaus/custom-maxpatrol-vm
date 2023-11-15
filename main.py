import sys
import paramiko
import logging
import psycopg2
from psycopg2 import OperationalError
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from interface import Ui_MainWindow


logging.basicConfig(level=logging.INFO, filename='mp_logging.log')


class Scanner(QtWidgets.QMainWindow):
    def __init__(self):
        super(Scanner, self).__init__()
        self.interface = Ui_MainWindow()
        self.interface.setupUi(self)
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle('MaxPatrol VM')
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        self.interface.input_host.setPlaceholderText('HOST')
        self.interface.input_username.setPlaceholderText('LOGIN')
        self.interface.input_password.setPlaceholderText('PASSWORD')
        self.interface.input_port.setPlaceholderText('PORT')
        self.interface.pushButton.clicked.connect(self.process)

    def process(self):  # подключение к удаленному хосту, получение сведений об операционке и внесение их в БД

        # обработка инфы от пользователя о профиле сканирования
        host = self.interface.input_host.text()
        login = self.interface.input_username.text()
        password = self.interface.input_password.text()
        port = self.interface.input_port.text()

        # установка сессии ssh
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(host, username=login, password=password, port=port)
            logging.info(f"Установлено подключение по ssh к хосту {host}")
        except:
            logging.error(f"Ошибка подключения к хосту {host} по ssh")
        # выполнение команды для получения типа ОС
        ssh_stdin_OSt, ssh_stdout_OSt, ssh_stderr_OSt = client.exec_command(
            'uname -o')

        # выполнение команды для получения версии ОС
        ssh_stdin_OSv, ssh_stdout_OSv, ssh_stderr_OSv = client.exec_command(
            'lsb_release -d')

        # выполнение команды для получения информации о ядре
        ssh_stdin_mh, ssh_stdout_mh, ssh_stderr_mh = client.exec_command(
            'uname -m')

        # выполнение команды для получения информации об архитектуре процессора
        ssh_stdin_kv, ssh_stdout_kv, ssh_stderr_kv = client.exec_command(
            'uname -r')

        # форматирование вывода о типе ОС
        output_type = ssh_stdout_OSt.read()
        output_type = output_type.decode('utf-8')
        output_type = output_type.strip('\n')

        # форматирование вывода о версии ОС
        output_version = ssh_stdout_OSv.read()
        output_version = output_version.decode('utf-8')
        output_version = output_version.strip('\n')
        output_version = output_version.replace('Description:\t', '')

        # форматирование вывода о ядре
        output_kernel = ssh_stdout_kv.read()
        output_kernel = output_kernel.decode('utf-8')
        output_kernel = output_kernel.strip('\n')

        # форматирование вывода о процессоре
        output_cpu = ssh_stdout_mh.read()
        output_cpu = output_cpu.decode('utf-8')
        output_cpu = output_cpu.strip('\n')

        self.interface.output_type.addItem(output_type)
        self.interface.output_version.addItem(output_version)
        self.interface.output_kernel.addItem(output_kernel)
        self.interface.output_cpu.addItem(output_cpu)

        # подключение к postgresql для внесения полученных данных
        try:
            db_conn = psycopg2.connect(
                database='maxpatrolvm',
                user='postgres',
                password='qwerty',
            )
            query = """INSERT INTO os (os_type, os_vers, cpu_arch, kernel_vers, addr_host) VALUES (%s, %s, %s, %s, %s);"""
            cursor = db_conn.cursor()
            cursor.execute(query, (output_type, output_version,
                           output_cpu, output_kernel, host))
            db_conn.commit()
            logging.info(
                f'''В базу данных были добавлены следующие значения:\nos_type: {output_type}\nos_vers:{output_version}\ncpu_arch:{output_cpu}\nkernel_vers: {output_kernel}\naddr_host: {host}''')
            cursor.close()
            db_conn.close()
        except OperationalError as er:
            logging.error(
                f"Возникла ошибка '{er}' при подключении к базе данных")


app = QtWidgets.QApplication([])
application = Scanner()
application.show()

sys.exit(app.exec())
