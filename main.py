from flask import Flask, render_template_string

app = Flask(__name__)

# Стили (добавил анимацию и стили для пустых избранных)
STYLE = '''
<style>
    :root { --bg: #0a0a0a; --card: #161616; --accent: #ff4444; --green: #2ecc71; --text: #ffffff; --subtext: #a1a1a1; }
    body { background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; margin: 0; display: flex; min-height: 100vh; }
    .sidebar { width: 240px; background: var(--card); height: 100vh; padding: 25px 15px; box-sizing: border-box; display: flex; flex-direction: column; border-right: 1px solid #222; position: fixed; z-index: 100; }
    .logo-container { text-align: center; margin-bottom: 30px; }
    .logo-container img { width: 120px; height: 120px; border-radius: 18px; filter: drop-shadow(0 0 8px var(--accent)); }
    .nav-item { padding: 10px 15px; border-radius: 8px; cursor: pointer; color: var(--subtext); transition: 0.2s; text-decoration: none; margin-bottom: 5px; font-weight: 500; display: block; font-size: 0.9rem; }
    .nav-item:hover, .nav-item.active { background: #222; color: white; }
    .btn-install { background: var(--green); color: black; padding: 12px; border-radius: 8px; text-decoration: none; font-weight: bold; text-align: center; margin-top: auto; transition: 0.3s; font-size: 0.9rem; }
    .btn-install:hover { transform: scale(1.05); box-shadow: 0 0 20px rgba(46, 204, 113, 0.4); }
    .main { flex: 1; padding: 40px; margin-left: 240px; }
    .top-bar { display: flex; align-items: center; justify-content: space-between; margin-bottom: 30px; }
    .control-btns { display: flex; gap: 10px; }
    .ctrl-btn { background: #222; color: var(--subtext); border: 1px solid #333; padding: 5px 15px; border-radius: 5px; cursor: pointer; font-size: 0.8rem; transition: 0.2s; }
    .ctrl-btn:hover { background: var(--accent); color: white; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
    .card { background: var(--card); border-radius: 15px; border: 1px solid #222; padding: 20px; transition: 0.3s; text-decoration: none; color: inherit; position: relative; }
    .card:hover { border-color: var(--accent); transform: translateY(-5px); }
    .card h3 { margin: 0 0 10px 0; color: var(--accent); }
    .heart-btn { cursor: pointer; font-size: 2rem; color: #333; transition: 0.3s; background: none; border: none; outline: none; padding: 0; line-height: 1; }
    .heart-btn.liked { color: var(--accent); filter: drop-shadow(0 0 5px var(--accent)); }
    .empty-msg { color: var(--subtext); text-align: center; grid-column: 1 / -1; margin-top: 50px; }
</style>
'''

# JavaScript для работы с избранным
SCRIPTS = '''
<script>
    function toggleLike(id, name, desc) {
        let favs = JSON.parse(localStorage.getItem('hk_favs') || '[]');
        const index = favs.findIndex(item => item.id === id);
        
        if (index > -1) {
            favs.splice(index, 1);
            document.getElementById('heart-' + id)?.classList.remove('liked');
        } else {
            favs.push({id, name, desc});
            document.getElementById('heart-' + id)?.classList.add('liked');
        }
        localStorage.setItem('hk_favs', JSON.stringify(favs));
    }

    function loadHeart(id) {
        let favs = JSON.parse(localStorage.getItem('hk_favs') || '[]');
        if (favs.some(item => item.id === id)) {
            document.getElementById('heart-' + id)?.classList.add('liked');
        }
    }

    function renderFavs() {
        const grid = document.getElementById('fav-grid');
        if (!grid) return;
        let favs = JSON.parse(localStorage.getItem('hk_favs') || '[]');
        
        if (favs.length === 0) {
            grid.innerHTML = '<div class="empty-msg">Тут пока пусто... Лайкни что-нибудь!</div>';
            return;
        }
        
        grid.innerHTML = favs.map(item => `
            <a href="/${item.id}" class="card">
                <h3>${item.name}</h3>
                <p>${item.desc}</p>
            </a>
        `).join('');
    }

    function clearAllFavs() {
        localStorage.setItem('hk_favs', '[]');
        renderFavs();
    }
</script>
'''

def get_sidebar(active_page, show_install=False):
    install_btn = f'''<a href="https://raw.githubusercontent.com/r1ze-r/HK/main/Wurst-Client1.21.11-nk.jar" class="btn-install" download>Установить .jar</a>''' if show_install else ''
    return f'''
    <div class="sidebar">
        <div class="logo-container"><img src="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png" alt="HK"></div>
        <a href="/" class="nav-item {'active' if active_page == 'home' else ''}">Главная</a>
        <a href="/favs" class="nav-item {'active' if active_page == 'favs' else ''}">Понравившееся</a>
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
            {get_sidebar('home')}
            <div class="main">
                <h1>Наши проекты</h1>
                <div class="grid">
                    <a href="/wurst" class="card">
                        <h3>Wurst</h3>
                        <p>Отличный клиент для выживания с друзьями и удобный интерфейс.</p>
                    </a>
                </div>
            </div>
            {SCRIPTS}
        </body>
        </html>
    ''')

@app.route('/favs')
def favs():
    return render_template_string(f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <link rel="icon" href="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png" type="image/png">
            <title>HK - Понравившееся</title>
            {STYLE}
        </head>
        <body onload="renderFavs()">
            {get_sidebar('favs')}
            <div class="main">
                <div class="top-bar">
                    <a href="/" style="color: var(--accent); text-decoration: none; font-weight: bold;">← Назад</a>
                    <div class="control-btns">
                        <button class="ctrl-btn" onclick="clearAllFavs()">Убрать всё</button>
                    </div>
                </div>
                <h1>Понравившееся</h1>
                <div class="grid" id="fav-grid"></div>
            </div>
            {SCRIPTS}
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
        <body onload="loadHeart('wurst')">
            {get_sidebar('wurst', show_install=True)}
            <div class="main">
                <div class="top-bar">
                    <a href="/" style="color: var(--accent); text-decoration: none; font-weight: bold;">← Назад на главную</a>
                    <button id="heart-wurst" class="heart-btn" onclick="toggleLike('wurst', 'Wurst', 'Отличный клиент для выживания.')">❤</button>
                </div>
                <h1>Wurst Client</h1>
                <p style="color: var(--subtext); font-size: 1.1rem;">Сборка <b>1.21.11-nk</b>.</p>
            </div>
            {SCRIPTS}
        </body>
        </html>
    ''')

if __name__ == "__main__":
    app.run()
