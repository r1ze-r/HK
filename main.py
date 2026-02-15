from flask import Flask, render_template_string

app = Flask(__name__)

# Общий стиль (CSS)
STYLE = '''
<style>
    :root { --bg: #0a0a0a; --card: #161616; --accent: #ff4444; --green: #2ecc71; --text: #ffffff; --subtext: #a1a1a1; }
    body { background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; margin: 0; display: flex; min-height: 100vh; }
    
    /* Сайдбар с нормальным логотипом */
    .sidebar { width: 1080px; background: var(--card); height: 100vh; padding: 25px 15px; box-sizing: border-box; display: flex; flex-direction: column; border-right: 1px solid #222; position: fixed; z-index: 100; }
    .logo-container { text-align: center; margin-bottom: 30px; }
    .logo-container img { width: 120px; height: 120px; border-radius: 18px; filter: drop-shadow(0 0 8px var(--accent)); }
    
    .nav-item { padding: 10px 15px; border-radius: 8px; cursor: pointer; color: var(--subtext); transition: 0.2s; text-decoration: none; margin-bottom: 5px; font-weight: 500; display: block; font-size: 0.9rem; }
    .nav-item:hover { background: #222; color: white; }
    .active { background: #333; color: white; }
    
    /* Зеленая кнопка установки (теперь только для страниц читов) */
    .btn-install { background: var(--green); color: black; padding: 12px; border-radius: 8px; text-decoration: none; font-weight: bold; text-align: center; margin-top: auto; transition: 0.3s; font-size: 0.9rem; }
    .btn-install:hover { transform: scale(1.05); box-shadow: 0 0 20px rgba(46, 204, 113, 0.4); }

    /* Контент */
    .main { flex: 1; padding: 40px; margin-left: 240px; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
    
    /* Карточка */
    .card { background: var(--card); border-radius: 15px; border: 1px solid #222; overflow: hidden; transition: 0.3s; text-decoration: none; color: inherit; display: block; }
    .card:hover { border-color: var(--accent); transform: translateY(-5px); }
    .card-img { width: 100%; height: 160px; object-fit: cover; }
    .card-content { padding: 15px; }
    .card h3 { margin: 0 0 8px 0; color: var(--accent); font-size: 1.2rem; }
    .card p { color: var(--subtext); font-size: 0.85rem; margin: 0; line-height: 1.4; }
    
    /* Страница проекта */
    .project-header { width: 100%; height: 250px; border-radius: 15px; object-fit: cover; margin-bottom: 20px; border: 1px solid #333; display: block; }
    .btn-back { color: var(--accent); text-decoration: none; margin-bottom: 15px; display: inline-block; font-weight: bold; font-size: 0.9rem; }
    .btn-back:hover { text-decoration: underline; }
    h1 { margin-top: 0; font-size: 2rem; }
</style>
'''

# Шаблон сайдбара (теперь принимает show_install)
def get_sidebar(active_page, show_install=False):
    install_btn = f'''
    <a href="https://raw.githubusercontent.com/r1ze-r/HK/main/Wurst-Client1.21.11-nk.jar" class="btn-install" download>Установить .jar</a>
    ''' if show_install else ''
    
    return f'''
    <div class="sidebar">
        <div class="logo-container">
            <img src="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png" alt="HK">
        </div>
        <a href="/" class="nav-item {'active' if active_page == 'home' else ''}">Главная</a>
        <a href="/wurst" class="nav-item {'active' if active_page == 'wurst' else ''}">Wurst</a>
        <a href="#" class="nav-item">Настройки</a>
        {install_btn}
    </div>
    '''

@app.route('/')
def home():
    return render_template_string(f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <link rel="icon" href="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png" type="image/png">
            <title>HK - Главная</title>
            {STYLE}
        </head>
        <body>
            {get_sidebar('home', show_install=False)}
            <div class="main">
                <h1>Наши проекты</h1>
                <div class="grid">
                    <a href="/wurst" class="card">
                        <img src="https://raw.githubusercontent.com/r1ze-r/HK/main/123123.webp" class="card-img">
                        <div class="card-content">
                            <h3>Wurst</h3>
                            <p>Отличный клиент для выживания с друзьями и удобный интерфейс.</p>
                        </div>
                    </a>
                </div>
            </div>
        </body>
        </html>
    ''')

@app.route('/wurst')
def wurst_page():
    return render_template_string(f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <link rel="icon" href="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png" type="image/png">
            <title>HK - Wurst Client</title>
            {STYLE}
        </head>
        <body>
            {get_sidebar('wurst', show_install=True)}
            <div class="main">
                <a href="/" class="btn-back">← Назад на главную</a>
                <img src="https://raw.githubusercontent.com/r1ze-r/HK/main/123123.webp" class="project-header">
                <h1>Wurst Client</h1>
                <p style="color: var(--subtext); font-size: 1.1rem; line-height: 1.6;">
                    Wurst — это классика. Мы подготовили специальную сборку <b>1.21.11-nk</b>, 
                    чтобы твой опыт выживания был максимально комфортным и фановым.
                </p>
            </div>
        </body>
        </html>
    ''')

if __name__ == "__main__":
    app.run()
