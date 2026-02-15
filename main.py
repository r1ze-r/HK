from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="icon" href="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png" type="image/png">
            <title>HK - HelloKilaura</title>
            <style>
                :root { --bg: #111111; --card: #1c1c1c; --accent: #ff4444; --text: #ffffff; --subtext: #a1a1a1; }
                body { background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; margin: 0; display: flex; min-height: 100vh; flex-direction: column; }
                
                .sidebar { width: 260px; background: var(--card); height: 100vh; padding: 20px; box-sizing: border-box; display: flex; flex-direction: column; border-right: 1px solid #333; position: fixed; }
                .sidebar img { width: 100%; border-radius: 12px; filter: drop-shadow(0 0 10px var(--accent)); margin-bottom: 20px; }
                .nav-item { padding: 12px; border-radius: 8px; cursor: pointer; color: var(--subtext); transition: 0.2s; text-decoration: none; margin-bottom: 5px; font-weight: 500; }
                .nav-item:hover, .nav-item.active { background: #333; color: white; }
                
                .main { flex: 1; padding: 40px; margin-left: 260px; display: flex; flex-direction: column; }
                .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
                .search { background: var(--card); border: 1px solid #333; padding: 10px 20px; border-radius: 8px; width: 400px; color: white; outline: none; }
                
                .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; flex-grow: 1; }
                .card { background: var(--card); padding: 25px; border-radius: 15px; border: 1px solid #333; transition: 0.3s; height: fit-content; }
                .card:hover { border-color: var(--accent); transform: translateY(-5px); }
                .card h3 { margin: 0 0 12px 0; color: var(--accent); font-size: 1.4rem; }
                .card p { color: var(--subtext); font-size: 0.95rem; line-height: 1.5; margin: 0; }
                
                .btn-main { background: var(--accent); color: white; padding: 10px 25px; border-radius: 8px; text-decoration: none; font-weight: bold; }
                
                /* Тот самый маленький текст внизу */
                .footer { padding: 20px 0; font-size: 0.75rem; color: #555; text-align: center; }
                .footer a { color: #555; text-decoration: none; transition: 0.2s; }
                .footer a:hover { color: var(--accent); }
            </style>
        </head>
        <body>
            <div class="sidebar">
                <img src="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png" alt="HK Logo">
                <a href="#" class="nav-item active">Главная</a>
                <a href="#" class="nav-item">Проекты</a>
                <a href="#" class="nav-item">Версии</a>
                <a href="#" class="nav-item">Настройки</a>
            </div>
            
            <div class="main">
                <div class="header">
                    <input type="text" class="search" placeholder="Поиск по HelloKilaura...">
                    <a href="#" class="btn-main">Войти</a>
                </div>
                
                <h1>Проекты HK</h1>
                
                <div class="grid">
                    <div class="card">
                        <h3>Envy Client</h3>
                        <p>Инструмент для оптимизации и расширения возможностей. Полная поддержка последних версий.</p>
                    </div>
                    <div class="card">
                        <h3>HK Core</h3>
                        <p>Стабильная библиотека для работы всех модулей HelloKilaura.</p>
                    </div>
                </div>

                <div class="footer">
                    Наши новости в телеграм канале <a href="https://t.me/hellokilaura" target="_blank">https://t.me/hellokilaura</a>
                </div>
            </div>
        </body>
        </html>
    ''')

if __name__ == "__main__":
    app.run()
