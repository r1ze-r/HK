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
            <title>HK - HelloKilaura</title>
            <style>
                :root { --bg: #111111; --card: #1c1c1c; --accent: #ff4444; --text: #ffffff; --subtext: #a1a1a1; }
                body { background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; margin: 0; display: flex; }
                
                /* Боковое меню в стиле Modrinth */
                .sidebar { width: 260px; background: var(--card); height: 100vh; padding: 20px; box-sizing: border-box; display: flex; flex-direction: column; border-right: 1px solid #333; }
                .sidebar img { width: 100%; border-radius: 12px; filter: drop-shadow(0 0 10px var(--accent)); margin-bottom: 20px; }
                .nav-item { padding: 12px; border-radius: 8px; cursor: pointer; color: var(--subtext); transition: 0.2s; text-decoration: none; margin-bottom: 5px; font-weight: 500; }
                .nav-item:hover, .nav-item.active { background: #333; color: white; }
                
                /* Основной контент */
                .main { flex: 1; padding: 40px; overflow-y: auto; }
                .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
                .search { background: var(--card); border: 1px solid #333; padding: 10px 20px; border-radius: 8px; width: 400px; color: white; }
                
                .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
                .card { background: var(--card); padding: 20px; border-radius: 12px; border: 1px solid #333; transition: 0.3s; cursor: pointer; }
                .card:hover { border-color: var(--accent); transform: translateY(-5px); }
                .card h3 { margin: 0 0 10px 0; color: var(--accent); }
                .card p { color: var(--subtext); font-size: 0.9rem; line-height: 1.4; }
                
                .btn-main { background: var(--accent); color: white; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: bold; }
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
                
                <h1>Добро пожаловать в HK</h1>
                <p style="color: var(--subtext);">The лютейшая имба is now under construction in Modrinth style.</p>
                
                <div class="grid">
                    <div class="card">
                        <h3>Envy Client</h3>
                        <p>Тот самый проект, который мы искали. Скоро здесь будет описание, список изменений и кнопка скачивания.</p>
                    </div>
                    <div class="card">
                        <h3>HK Core</h3>
                        <p>Ядро для всех будущих дополнений. Оптимизация и стабильность на высшем уровне.</p>
                    </div>
                    <div class="card">
                        <h3>Community Mods</h3>
                        <p>Раздел для ваших идей и предложений. Мы строим это вместе.</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
    ''')

if __name__ == "__main__":
    app.run()
