from flask import Flask, request
from telegram import Bot
from prometheus_client import start_http_server, Counter

# Telegram токен
TOKEN = "Yuor Token"
bot = Bot(token=TOKEN)

# Flask-сервер
app = Flask(__name__)

# Prometheus метрики
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint'])

# Подсчет запросов
@app.before_request
def before_request():
    REQUEST_COUNT.labels(request.method, request.endpoint).inc()

# Обработка GET-запросов
@app.route('/get', methods=['GET'])
def handle_get():
    chat_id = request.args.get('chat_id', default=None, type=int)
    message = request.args.get('message', default='Привет!', type=str)
    if chat_id:
        bot.send_message(chat_id=chat_id, text=message)
        return "Сообщение отправлено!"
    return "Не указан chat_id", 400

# Обработка POST-запросов
@app.route('/post', methods=['POST'])
def handle_post():
    data = request.json
    chat_id = data.get('chat_id')
    message = data.get('message', 'Привет!')
    if chat_id:
        bot.send_message(chat_id=chat_id, text=message)
        return "Сообщение отправлено!"
    return "Не указан chat_id", 400

if __name__ == '__main__':
    # Prometheus сервер на порту 8000
    start_http_server(8000)
    # Flask сервер
    app.run(host='0.0.0.0', port=5000)
