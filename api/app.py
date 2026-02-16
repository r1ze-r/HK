from flask import Flask, render_template_string

app = Flask(__name__)

# --- ТОЛЬКО МЕТЕОР И ВУРСТ ---
DATABASE = {
    'wurst': {
        'name': 'Wurst Client',
        'desc': 'Король выживания. Включает в себя более 150 модулей: от AutoMine до KillAura. Идеально сбалансирован для игры на серверах без жесткого античита.',
        'ver': '1.21.1',
        'tags': ['Survival', 'Utility', 'Classic'],
        'file_url': 'https://raw.githubusercontent.com/r1ze-r/HK/main/Wurst-Client1.21.11-hk.jar'
    },
    'meteor': {
        'name': 'Meteor Client',
        'desc': 'Ультимативное решение для PVP и анархии. Лучший CrystalAura на рынке, гибкая настройка HUD и мощная система макросов.',
        'ver': '1.21.1',
        'tags': ['Anarchy', 'PVP', 'Modern'],
        'file_url': 'https://raw.githubusercontent.com/r1ze-r/HK/main/meteor-client-1.21.11-hk.jar'
    }
}

STYLE = '''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    :root {
        --bg: #050505; --card-bg: #111111; --card-border: #222222;
        --accent: #ff4444; --accent-glow: rgba(255, 68, 68, 0.3);
        --text-main: #ffffff; --text-dim: #888888; --tg-color: #24A1DE;
        --green: #2ecc71; --glass: rgba(20, 20, 20, 0.8);
        --transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background-color: var(--bg); color: var(--text-main); font-family: 'Inter', sans-serif; min-height: 100vh; }
    
    header {
        position: sticky; top: 0; z-index: 1000; background: var(--glass);
        backdrop-filter: blur(20px); border-bottom: 1px solid var(--card-border); padding: 15px 0;
    }
    .nav-container { max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; padding: 0 20px; }
    .logo-side { display: flex; align-items: center; gap: 15px; text-decoration: none; color: white; font-weight: 900; }
    .logo-side img { width: 45px; height: 45px; border-radius: 12px; }
    
    .nav-links { display: flex; gap: 10px; }
    .nav-btn {
        padding: 10px 20px; border-radius: 12px; text-decoration: none; 
        color: var(--text-dim); font-weight: 700; background: #151515;
        border: 1px solid #252525; transition: var(--transition);
    }
    .nav-btn.active { color: white; border-color: var(--accent); box-shadow: 0 0 15px var(--accent-glow); }

    .container { max-width: 1200px; margin: 0 auto; padding: 40px 20px; }
    .hero { text-align: center; margin-bottom: 50px; }
    .hero h1 { font-size: 3.5rem; font-weight: 900; background: linear-gradient(to bottom, #fff, #666); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

    .cheat-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 25px; }
    .cheat-card {
        background: var(--card-bg); border: 1px solid var(--card-border);
        border-radius: 24px; padding: 30px; cursor: pointer; transition: var(--transition);
        display: flex; flex-direction: column; position: relative;
    }
    .cheat-card:hover { transform: translateY(-8px); border-color: #444; }

    .tag-container { display: flex; gap: 6px; margin-bottom: 15px; }
    .tag { font-size: 0.65rem; font-weight: 800; background: #1a1a1a; padding: 4px 10px; border-radius: 6px; color: #777; }
    .cheat-card h3 { font-size: 1.6rem; color: var(--accent); margin-bottom: 10px; }
    .cheat-card p { color: var(--text-dim); font-size: 0.9rem; flex-grow: 1; margin-bottom: 20px; }

    .heart-btn {
        width: 42px; height: 42px; border-radius: 10px; background: #1a1a1a;
        border: none; color: #333; font-size: 1.2rem; cursor: pointer; transition: 0.3s;
    }
    .heart-btn.liked { color: var(--accent); text-shadow: 0 0 10px var(--accent); }

    .big-dl-btn {
        background: var(--green); color: black; padding: 20px 50px; border-radius: 15px;
        text-decoration: none; font-weight: 900; font-size: 1.3rem; display: inline-block;
        transition: 0.3s; border: none; cursor: pointer;
    }
    .big-dl-btn:hover { transform: scale(1.05); filter: brightness(1.1); }
</style>
'''

SCRIPTS = '''
<script>
    function getFavs() { return JSON.parse(localStorage.getItem('hk_v4_favs') || '[]'); }
    
    function toggleFav(e, id, name) {
        if(e) e.stopPropagation();
        let favs = getFavs();
        let idx = favs.findIndex(x => x.id === id);
        if(idx > -1) favs.splice(idx, 1);
        else favs.push({id, name});
        localStorage.setItem('hk_v4_favs', JSON.stringify(favs));
        document.querySelectorAll(`.heart-btn[data-id="${id}"]`).forEach(btn => btn.classList.toggle('liked'));
        if(window.location.pathname === '/favs') location.reload();
    }

    // ФИКС СКАЧИВАНИЯ ДЛЯ GITHUB
    function forceDownload(url, filename) {
        fetch(url).then(t => t.blob().then(b => {
            var a = document.createElement("a");
            a.href = URL.createObjectURL(b);
            a.setAttribute("download", filename);
            a.click();
        }));
    }

    document.addEventListener('DOMContentLoaded', () => {
        let favs = getFavs();
        document.querySelectorAll('.heart-btn').forEach(btn => {
            if(favs.some(f => f.id === btn.dataset.id)) btn.classList.add('liked');
        });
    });
</script>
'''

def get_header(active):
    return f'''
    <header>
        <div class="nav-container">
            <a href="/" class="logo-side"><span>HK HUB</span></a>
            <div class="nav-links">
                <a href="/" class="nav-btn {'active' if active=='home' else ''}">Главная</a>
                <a href="/favs" class="nav-btn {'active' if active=='favs' else ''}">Понравившееся</a>
            </div>
        </div>
    </header>
    '''

@app.route('/')
def home():
    cards = ""
    for k, v in DATABASE.items():
        tags = "".join([f'<span class="tag">{t}</span>' for t in v['tags']])
        cards += f'''
        <div class="cheat-card" onclick="window.location.href='/cheat/{k}'">
            <div class="tag-container">{tags}</div>
            <h3>{v['name']}</h3>
            <p>{v['desc']}</p>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="color:#555">{v['ver']}</span>
                <button class="heart-btn" data-id="{k}" onclick="toggleFav(event, '{k}', '{v['name']}')">❤</button>
            </div>
        </div>'''
    return render_template_string(f'<html><head>{STYLE}</head><body>{get_header("home")}<div class="container"><div class="hero"><h1>Все Читы</h1></div><div class="cheat-grid">{cards}</div></div>{SCRIPTS}</body></html>')

@app.route('/cheat/<id>')
def detail(id):
    item = DATABASE.get(id)
    if not item: return "404", 404
    return render_template_string(f'''
    <html><head>{STYLE}</head><body>
        {get_header("home")}
        <div class="container">
            <h1 style="font-size:3rem; margin-bottom:20px;">{item['name']}</h1>
            <div style="background:#111; padding:40px; border-radius:25px; border:1px solid #222;">
                <p style="font-size:1.2rem; color:#888; margin-bottom:30px;">{item['desc']}</p>
                <button onclick="forceDownload('{item['file_url']}', '{id}.jar')" class="big-dl-btn">СКАЧАТЬ .JAR КЛИЕНТ</button>
            </div>
        </div>{SCRIPTS}
    </body></html>''')

@app.route('/favs')
def favs():
    return render_template_string(f'''
    <html><head>{STYLE}</head><body>
        {get_header("favs")}
        <div class="container">
            <div class="hero"><h1>Твоя Коллекция</h1></div>
            <div id="fav-grid" class="cheat-grid"></div>
        </div>
        {SCRIPTS}
        <script>
            const db = {DATABASE};
            const favs = getFavs();
            const grid = document.getElementById('fav-grid');
            if(!favs.length) grid.innerHTML = "<h1>ПУСТО</h1>";
            favs.forEach(f => {{
                const c = db[f.id];
                if(c) grid.innerHTML += `<div class="cheat-card" onclick="window.location.href='/cheat/${{f.id}}'"><h3>${{c.name}}</h3><p>${{c.desc}}</p><button class="heart-btn liked" onclick="toggleFav(event, '${{f.id}}')">❤</button></div>`;
            }});
        </script>
    </body></html>''')

if __name__ == '__main__':
    app.run(debug=True)
