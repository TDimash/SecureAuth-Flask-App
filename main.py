from flask import Flask
import socket
import logging

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(filename='server_log.txt', level=logging.INFO, 
                    format='%(asctime)s %(message)s')

@app.route('/')
def hello_world():
    logging.info('Received request on /')
    return 'Hello, World!'

if __name__ == '__main__':
    # Получаем IP-адрес устройства
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    log_message = f'Server is running on http://{ip_address}:5000'
    
    # Выводим в терминал и записываем в файл
    print(log_message)
    logging.info(log_message)
    
    # Запускаем сервер на всех интерфейсах
    app.run(host='0.0.0.0', port=5000)
