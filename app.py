from flask import Flask, render_template_string
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


STYLE = '''<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* (оставил как у тебя — не трогал дизайн) */
</style>'''


# ✅ FIX: добавил SCRIPTS (у тебя его не было)
SCRIPTS = '''
<script>
function updateFavs(id, name) {
    let favs = JSON.parse(localStorage.getItem('hk_v3_favs') || '[]');

    const index = favs.findIndex(f => f.id === id);

    if (index === -1) {
        favs.push({id, name});
    } else {
        favs.splice(index, 1);
    }

    localStorage.setItem('hk_v3_favs', JSON.stringify(favs));
}

function search() {
    const input = document.getElementById("mainSearch").value.toLowerCase();
    const cards = document.querySelectorAll(".cheat-card");

    cards.forEach(card => {
        const text = card.innerText.toLowerCase();
        card.style.display = text.includes(input) ? "flex" : "none";
    });
}

function forceDownload(url, name) {
    fetch(url)
        .then(res => res.blob())
        .then(blob => {
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = name;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
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
        name = val.get('name', '')
        desc = val.get('desc', '')
        ver = val.get('ver', '')
        tags = val.get('tags', [])

        tags_html = "".join([f'<span class="tag">{t}</span>' for t in tags])

        cards_html += f'''
        <div class="cheat-card"
            onclick="window.location.href='/cheat/' + '{key}'">

            <div class="tag-container">{tags_html}</div>
            <h3>{name}</h3>
            <p style="color:var(--text-dim); margin-bottom:20px;">{desc}</p>

            <div class="card-meta">
                <span class="version-tag">{ver}</span>
                <button class="heart-btn"
                    onclick="event.stopPropagation(); updateFavs('{key}', '{name}')">
                    &#10084;
                </button>
            </div>
        </div>
        '''

    return render_template_string(f'''
    <html>
    <head>{STYLE}</head>
    <body>
        <div class="bg-glow"></div>

        {get_nav("home")}

        <div class="container">
            <div class="hero">
                <h1>Каталог HK Hub</h1>
                <div class="search-wrapper">
                    <input type="text" id="mainSearch"
                        class="search-input"
                        placeholder="Поиск читов..."
                        oninput="search()">
                </div>
            </div>

            <div class="cheat-grid">
                {cards_html}
            </div>
        </div>

        <div class="tg-anchor">
            <a href="https://t.me/kaelixdev" class="tg-btn">Telegram</a>
        </div>

        {SCRIPTS}
    </body>
    </html>
    ''')


@app.route('/favs')
def favs():
    db_json = json.dumps(DATABASE)

    return render_template_string(f'''
    <html>
    <head>{STYLE}</head>
    <body>
        <div class="bg-glow"></div>

        {get_nav("favs")}

        <div class="container">
            <h1 style="text-align:center; margin: 40px 0;">Понравившееся</h1>
            <div id="favs-list" class="cheat-grid"></div>
        </div>

        {SCRIPTS}

        <script>
        document.addEventListener('DOMContentLoaded', () => {{
            const favs = JSON.parse(localStorage.getItem('hk_v3_favs') || '[]');
            const container = document.getElementById('favs-list');
            const db = {db_json};

            if (favs.length === 0) {{
                container.innerHTML =
                '<p style="grid-column:1/-1;text-align:center;opacity:0.5;font-size:1.5rem;">Пусто</p>';
                return;
            }}

            let html = '';

            favs.forEach(fav => {{
                const item = db[fav.id];
                if (!item) return;

                html += `
                <div class="cheat-card"
                    onclick="window.location.href='/cheat/' + fav.id">

                    <div class="tag-container">
                        ${{item.tags.map(t => `<span class="tag">${{t}}</span>`).join('')}}
                    </div>

                    <h3>${{item.name}}</h3>
                    <p style="color:var(--text-dim); margin-bottom:20px;">${{item.desc}}</p>

                    <div class="card-meta">
                        <span class="version-tag">${{item.ver}}</span>

                        <button class="heart-btn liked"
                            onclick="event.stopPropagation(); updateFavs('${{fav.id}}','${{item.name}}'); location.reload();">
                            ♥
                        </button>
                    </div>
                </div>`;
            }});

            container.innerHTML = html;
        }});
        </script>

    </body>
    </html>
    ''')


@app.route('/cheat/<id>')
def detail(id):
    item = DATABASE.get(id)
    if not item:
        return "404", 404

    video_file = "2026-02-16-22-54-44.mp4"

    name = item.get('name')
    ver = item.get('ver')
    desc = item.get('desc')
    url = item.get('file_url')

    return render_template_string(f'''
    <html>
    <head>{STYLE}</head>
    <body>
        <div class="bg-glow"></div>

        {get_nav("detail")}

        <div class="container">

            <a href="/">← Назад</a>

            <h1>{name}</h1>

            <span class="version-tag">{ver}</span>

            <p>{desc}</p>

            <button onclick="forceDownload('{url}','{name}')">
                СКАЧАТЬ
            </button>

            <video controls width="100%">
                <source src="/static/{video_file}">
            </video>

        </div>

        {SCRIPTS}
    </body>
    </html>
    ''')


if __name__ == "__main__":
    app.run(debug=True)
