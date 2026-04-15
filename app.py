from flask import Flask, render_template_string, jsonify
import json

app = Flask(__name__)


DATABASE = {
    'wurst': {
        'name': 'Wurst Client',
        'desc': 'Король выживания. Включает в себя более 150 модулей: от AutoMine до KillAura. Идеально сбалансирован для игры на серверах без жесткого античита.',
        'ver': '1.21.11',
        'tags': ['Survival', 'Utility', 'Classic', 'Cheat'],
        'color': '#ff4444',
        'file_url': 'https://raw.githubusercontent.com/r1ze-r/HK/main/Wurst-Client1.21.11-hk.jar'
    },
    'xray': {
        'name': 'X-Ray Ultimate',
        'desc': 'Тот самый легендарный ресурспак. Подсвечивает руды и упрощает поиск алмазов. Идеально для тех, кто хочет результат без установки тяжелых читов.',
        'ver': '1.21',
        'tags': ['Resourcepack', 'Survival', 'Popular'],
        'color': '#ffffff',
        'file_url': 'https://raw.githubusercontent.com/r1ze-r/HK/main/Xray_Ultimate_1.21_v5.3.1.zip'
    },
    'coffee': {
        'name': 'Coffee Client',
        'desc': 'Любишь кофе? Тогда этот чит для тебя. Лучший дизайн, много функций и многое другое.',
        'ver': '1.20.1',
        'tags': ['Resourcepack', 'Survival', 'Popular'],
        'color': '#ffffff',
        'file_url': 'https://raw.githubusercontent.com/r1ze-r/HK/main/freecam-fabric1.21.11.jar'
    },
    'freecam': {
        'name': 'freecam',
        'desc': 'Этот мод тебе позволяет летать! (но только визуал) хорошо подойдет для просмотра вражеских баз',
        'ver': '1.21.11',
        'tags': ['Resourcepack', 'Survival', 'Popular'],
        'color': '#ffffff',
        'file_url': 'https://raw.githubusercontent.com/r1ze-r/HK/main/Coffee-Client-Fabric-1.20.1.jar'
    },
    'meteor': {
        'name': 'Meteor Client',
        'desc': 'Ультимативное решение для PVP и анархии. Гибкая настройка HUD и мощная система макросов.',
        'ver': '1.21.11',
        'tags': ['Anarchy', 'PVP', 'Cheat'],
        'color': '#2ecc71',
        'file_url': 'https://raw.githubusercontent.com/r1ze-r/HK/main/meteor-client-1.21.1-hk.jar'
    }
}


# ✅ ТВОЙ CSS ВЕРНУЛ ПОЛНОСТЬЮ (ничего не удалял)
STYLE = '''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    :root {
        --bg: #050505;
        --card-bg: #111111;
        --card-border: #222222;
        --accent: #ff4444;
        --accent-glow: rgba(255, 68, 68, 0.3);
        --text-main: #ffffff;
        --text-dim: #888888;
        --tg-color: #24A1DE;
        --green: #2ecc71;
        --transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }

    * { margin: 0; padding: 0; box-sizing: border-box; -webkit-tap-highlight-color: transparent; }

    body {
        background-color: var(--bg);
        color: var(--text-main);
        font-family: 'Inter', sans-serif;
        line-height: 1.6;
        overflow-x: hidden;
        min-height: 100vh;
    }

    .bg-glow {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: radial-gradient(circle at 50% 50%, rgba(20, 20, 20, 1) 0%, rgba(5, 5, 5, 1) 100%);
        z-index: -1;
    }

    header {
        position: relative;
        z-index: 1000;
        background: transparent;
        padding: 40px 0 20px 0;
    }

    .nav-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
    }

    .logo {
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 15px;
        transition: var(--transition);
    }

    .logo-img {
        width: 45px;
        height: 45px;
        border-radius: 12px;
        object-fit: cover;
        border: 1px solid var(--card-border);
    }

    .logo-text {
        font-weight: 900;
        font-size: 1.6rem;
        letter-spacing: -1px;
        color: white;
    }

    .nav-links {
        position: absolute;
        right: 0px;
        display: flex;
        gap: 25px;
    }

    .nav-btn {
        text-decoration: none;
        color: rgba(255, 255, 255, 0.5);
        font-weight: 500;
        font-size: 0.95rem;
        transition: 0.3s;
        background: transparent;
        border: none;
        padding: 0;
    }

    .nav-btn:hover, .nav-btn.active {
        color: white;
    }

    .container { max-width: 1200px; margin: 0 auto; padding: 40px 20px; }

    .hero { text-align: center; margin-bottom: 60px; }
    .hero h1 {
        font-size: 4rem;
        font-weight: 900;
        letter-spacing: -2px;
        margin-bottom: 15px;
        background: linear-gradient(to bottom, #fff 0%, #666 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .search-wrapper { position: relative; width: 100%; max-width: 500px; margin: 30px auto; }
    .search-input {
        width: 100%; background: #111; border: 1px solid #222;
        padding: 18px 30px; border-radius: 20px; color: white;
        font-size: 1.1rem; outline: none;
        text-align: center;
    }

    .cheat-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
        gap: 30px;
    }

    .cheat-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 28px;
        padding: 35px;
        display: flex;
        flex-direction: column;
    }

    .cheat-card h3 {
        font-size: 1.8rem;
        font-weight: 800;
        color: var(--accent);
        margin-bottom: 12px;
    }

    .tag { font-size: 0.7rem; font-weight: 700; background: #1a1a1a;
        padding: 4px 12px; border-radius: 6px; color: #666; }

    .version-tag {
        background: #000;
        padding: 5px 12px;
        border-radius: 10px;
        border: 1px solid #222;
        font-size: 0.8rem;
        color: #aaa;
    }

    .heart-btn {
        width: 45px; height: 45px;
        border-radius: 12px;
        background: #1a1a1a;
        border: none;
        cursor: pointer;
    }

    .tg-btn {
        background: var(--tg-color);
        color: white;
        padding: 18px 30px;
        border-radius: 20px;
        text-decoration: none;
        font-weight: 900;
    }
</style>
'''


# ✅ FIXED SCRIPTS (у тебя этого не было)
SCRIPTS = '''
<script>
function updateFavs(id, name) {
    let favs = JSON.parse(localStorage.getItem('hk_v3_favs') || '[]');

    const i = favs.findIndex(f => f.id === id);

    if (i === -1) favs.push({id, name});
    else favs.splice(i, 1);

    localStorage.setItem('hk_v3_favs', JSON.stringify(favs));
}

function search() {
    const input = document.getElementById("mainSearch").value.toLowerCase();
    document.querySelectorAll(".cheat-card").forEach(card => {
        card.style.display = card.innerText.toLowerCase().includes(input) ? "flex" : "none";
    });
}

function forceDownload(url, name) {
    fetch(url).then(r => r.blob()).then(b => {
        const a = document.createElement("a");
        a.href = URL.createObjectURL(b);
        a.download = name;
        a.click();
    });
}
</script>
'''


def get_nav(page):
    home_active = "active" if page == "home" else ""
    favs_active = "active" if page == "favs" else ""

    return f'''
    <header>
        <div class="nav-container">
            <a href="/" class="logo">
                <img src="/static/HK.png" class="logo-img">
                <span class="logo-text">HK HUB</span>
            </a>
            <div class="nav-links">
                <a href="/" class="nav-btn {home_active}">Главная</a>
                <a href="/favs" class="nav-btn {favs_active}">Понравившееся</a>
            </div>
        </div>
    </header>
    '''


@app.route('/')
def home():
    cards_html = ""

    for key, val in DATABASE.items():
        tags_html = "".join([f'<span class="tag">{t}</span>' for t in val['tags']])

        cards_html += f'''
        <div class="cheat-card"
            onclick="window.location.href='/cheat/{key}'">

            <div>{tags_html}</div>
            <h3>{val['name']}</h3>
            <p style="color:#888">{val['desc']}</p>

            <div>
                <span class="version-tag">{val['ver']}</span>
                <button class="heart-btn"
                    onclick="event.stopPropagation(); updateFavs('{key}', '{val['name']}')">
                    ♥
                </button>
            </div>
        </div>
        '''

    return render_template_string(f'''
    <html><head>{STYLE}</head>
    <body>
        <div class="bg-glow"></div>
        {get_nav("home")}

        <div class="container">
            <div class="hero">
                <h1>Каталог HK Hub</h1>
                <input id="mainSearch" class="search-input" oninput="search()" placeholder="Поиск...">
            </div>

            <div class="cheat-grid">{cards_html}</div>
        </div>

        {SCRIPTS}
    </body></html>
    ''')


@app.route('/favs')
def favs():
    db_json = json.dumps(DATABASE)

    return render_template_string(f'''
    <html><head>{STYLE}</head><body>
        <div class="bg-glow"></div>
        {get_nav("favs")}

        <div class="container">
            <h1 style="text-align:center;">Понравившееся</h1>
            <div id="favs-list" class="cheat-grid"></div>
        </div>

        {SCRIPTS}

        <script>
        document.addEventListener('DOMContentLoaded', () => {{
            const favs = JSON.parse(localStorage.getItem('hk_v3_favs') || '[]');
            const db = {db_json};
            const c = document.getElementById('favs-list');

            if (!favs.length) {{
                c.innerHTML = "<p style='color:#888'>Пусто</p>";
                return;
            }}

            let html = "";

            favs.forEach(f => {{
                const i = db[f.id];
                if (!i) return;

                html += `
                <div class="cheat-card"
                    onclick="window.location.href='/cheat/' + f.id">

                    <h3>${{i.name}}</h3>
                    <p>${{i.desc}}</p>
                </div>`;
            }});

            c.innerHTML = html;
        }});
        </script>
    </body></html>
    ''')


@app.route('/cheat/<id>')
def detail(id):
    item = DATABASE.get(id)
    if not item:
        return "404", 404

    return render_template_string(f'''
    <html><head>{STYLE}</head><body>
        <div class="bg-glow"></div>
        {get_nav("detail")}

        <div class="container">
            <h1>{item['name']}</h1>
            <p>{item['desc']}</p>
            <button onclick="forceDownload('{item['file_url']}', '{item['name']}')">
                Скачать
            </button>
        </div>

        {SCRIPTS}
    </body></html>
    ''')


if __name__ == "__main__":
    app.run(debug=True)
