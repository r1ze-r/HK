from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Сайт запущен!</h1><p>Без всяких папок и шаблонов.</p>"

if __name__ == "__main__":
    app.run(debug=True)
