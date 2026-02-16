from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# --- CONFIG DATA (Твоя база, где ты сам добавляешь читы) ---
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
    'meteor': {
        'name': 'Meteor Client',
        'desc': 'Ультимативное решение для PVP и анархии. Гибкая настройка HUD и мощная система макросов.',
        'ver': '1.21.11',
        'tags': ['Anarchy', 'PVP', 'Cheat'],
        'color': '#2ecc71',
        'file_url': 'https://raw.githubusercontent.com/r1ze-r/HK/main/meteor-client-1.21.1-hk.jar'
    }
}


# --- FULL PORSCHE EDITION STYLES (Тот самый стиль) ---
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
        --glass: rgba(20, 20, 20, 0.7);
        --transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }

    * { 
        margin: 0; 
        padding: 0; 
        box-sizing: border-box; 
        -webkit-tap-highlight-color: transparent; 
    }

    body {
        background-color: var(--bg);
        color: var(--text-main);
        font-family: 'Inter', sans-serif;
        line-height: 1.6;
        overflow-x: hidden;
        min-height: 100vh;
        scrollbar-width: thin;
        scrollbar-color: var(--accent) var(--bg);
    }

    body::-webkit-scrollbar { width: 6px; }
    body::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 10px; }

    .bg-glow {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: radial-gradient(circle at 50% 50%, rgba(20, 20, 20, 1) 0%, rgba(5, 5, 5, 1) 100%);
        z-index: -1;
    }

    header {
        position: sticky; top: 0; z-index: 1000;
        background: var(--glass);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid var(--card-border);
        padding: 15px 0;
    }

    .nav-container {
        max-width: 1200px; margin: 0 auto;
        display: flex; justify-content: space-between; align-items: center;
        padding: 0 20px;
    }

    .logo {
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 15px;
        transition: var(--transition);
    }

    .logo:hover { transform: scale(1.02); }

    .logo-img {
        width: 45px;
        height: 45px;
        border-radius: 12px;
        object-fit: cover;
        box-shadow: 0 0 20px var(--accent-glow);
        border: 1px solid var(--card-border);
    }

    .logo-text {
        font-weight: 900;
        font-size: 1.6rem;
        letter-spacing: -1px;
        color: white;
    }

    .nav-links { display: flex; gap: 15px; }

    .nav-btn {
        padding: 12px 28px; border-radius: 14px;
        text-decoration: none; color: var(--text-dim);
        font-weight: 700; font-size: 1rem;
        background: #151515; border: 1px solid #252525;
        transition: var(--transition);
        display: flex; align-items: center; gap: 8px;
    }

    .nav-btn:hover, .nav-btn.active {
        color: white; background: #222; border-color: var(--accent);
        box-shadow: 0 0 20px var(--accent-glow);
        transform: translateY(-2px);
    }

    .container { max-width: 1200px; margin: 0 auto; padding: 60px 20px; }

    .hero { text-align: center; margin-bottom: 70px; }
    .hero h1 { 
        font-size: 4rem; font-weight: 900; letter-spacing: -2px; 
        margin-bottom: 15px; background: linear-gradient(to bottom, #fff 0%, #666 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }

    .search-wrapper { position: relative; width: 100%; max-width: 500px; margin: 30px auto; }
    .search-input {
        width: 100%; background: #111; border: 1px solid #222;
        padding: 18px 30px; border-radius: 20px; color: white;
        font-size: 1.1rem; outline: none; transition: var(--transition);
        text-align: center;
    }
    .search-input:focus { border-color: var(--accent); box-shadow: 0 0 30px var(--accent-glow); }

    .cheat-grid {
        display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
        gap: 30px; animation: fadeInUp 0.8s ease;
    }

    @keyframes fadeInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }

    .cheat-card {
        background: var(--card-bg); border: 1px solid var(--card-border);
        border-radius: 28px; padding: 35px; position: relative;
        transition: var(--transition); cursor: pointer;
        display: flex; flex-direction: column; overflow: hidden;
    }

    .cheat-card:hover {
        border-color: #444; transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }

    .cheat-card h3 { font-size: 1.8rem; font-weight: 800; color: var(--accent); margin-bottom: 12px; }
    
    .tag-container { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 20px; }
    .tag { font-size: 0.7rem; font-weight: 700; background: #1a1a1a; padding: 4px 12px; border-radius: 6px; color: #666; text-transform: uppercase; }

    .card-meta { display: flex; align-items: center; justify-content: space-between; margin-top: auto; }
    .version-tag { background: #000; padding: 5px 12px; border-radius: 10px; border: 1px solid #222; font-size: 0.8rem; color: #aaa; }

    .heart-btn {
        width: 45px; height: 45px; border-radius: 12px;
        background: #1a1a1a; border: none; color: #333;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.4rem; cursor: pointer; transition: 0.3s;
    }
    .heart-btn.liked { color: var(--accent); background: rgba(255,68,68,0.1); }

    .tg-anchor { position: fixed; left: 40px; bottom: 40px; z-index: 999; }
    .tg-btn {
        background: var(--tg-color); color: white; padding: 18px 30px; border-radius: 20px;
        text-decoration: none; font-weight: 900; display: flex; align-items: center; gap: 12px;
        box-shadow: 0 10px 30px rgba(36, 161, 222, 0.4); transition: 0.3s;
    }

    .detail-view { display: flex; flex-direction: column; gap: 40px; }
    .dl-section { width: 100%; padding: 40px; background: var(--card-bg); border-radius: 30px; border: 1px solid #222; }
    .big-dl-btn {
        background: var(--green); color: black; padding: 25px 60px;
        border-radius: 20px; text-decoration: none; font-weight: 900;
        font-size: 1.5rem; display: inline-block; cursor: pointer; border: none;
        transition: var(--transition);
    }
    .big-dl-btn:hover { transform: scale(1.05); box-shadow: 0 0 30px rgba(46, 204, 113, 0.4); }

    @media (max-width: 800px) {
        .nav-container { flex-direction: column; gap: 15px; }
        .hero h1 { font-size: 2.5rem; }
        .tg-anchor { left: 20px; bottom: 20px; right: 20px; }
        .tg-btn { justify-content: center; width: 100%; }
        .cheat-grid { grid-template-columns: 1fr; }
    }
</style>
'''

# --- ENGINE SCRIPTS ---
SCRIPTS = '''
<script>
    function getFavs() { return JSON.parse(localStorage.getItem('hk_v3_favs') || '[]'); }

    function updateFavs(id, name, isFavPage = false) {
        let favs = getFavs();
        let index = favs.findIndex(item => item.id === id);
        
        if (index > -1) {
            favs.splice(index, 1);
            if(isFavPage) {
                const card = document.getElementById(`card-fav-${id}`);
                if(card) {
                    card.style.transform = 'scale(0.8) translateY(20px)';
                    card.style.opacity = '0';
                    setTimeout(() => { 
                        card.remove();
                        if(getFavs().length === 0) location.reload();
                    }, 400);
                }
            }
        } else {
            favs.push({id: id, name: name});
        }
        
        localStorage.setItem('hk_v3_favs', JSON.stringify(favs));
        
        document.querySelectorAll(`.heart-btn[data-id="${id}"]`).forEach(btn => {
            btn.classList.toggle('liked');
        });
    }

    function search() {
        let query = document.getElementById('mainSearch').value.toLowerCase();
        document.querySelectorAll('.cheat-card').forEach(card => {
            card.style.display = card.innerText.toLowerCase().includes(query) ? 'flex' : 'none';
        });
    }

    function forceDownload(url, name) {
    // Эта магия сама вытягивает .jar или .zip из твоей прямой ссылки на GitHub
    const extension = url.split('.').pop(); 
    const fileName = "HK_" + name.replace(/\s+/g, '_') + "." + extension;
    
    fetch(url).then(t => t.blob()).then(b => {
        var a = document.createElement("a");
        a.href = URL.createObjectURL(b);
        a.setAttribute("download", fileName);
        a.click();
    });
}
    window.addEventListener('DOMContentLoaded', () => {
        let favs = getFavs();
        document.querySelectorAll('.heart-btn').forEach(btn => {
            if (favs.some(f => f.id === btn.dataset.id)) btn.classList.add('liked');
        });
    });
</script>
'''

def get_nav(page):
    return f'''
    <header>
        <div class="nav-container">
            <a href="/" class="logo">
                <img src="/static/HK.png" 
                     class="logo-img" 
                     alt="HK"
                     onerror="this.src='HK.png'; this.onerror=null;">
                <div class="logo-text">HK HUB</div>
            </a>
            <div class="nav-links">
                <a href="/" class="nav-btn {"active" if page == "home" else ""}">Главная</a>
                <a href="/favs" class="nav-btn {"active" if page == "favs" else ""}">Понравившееся</a>
            </div>
        </div>
    </header>
    '''

@app.route('/')
def home():
    cards_html = ""
    for key, val in DATABASE.items():
        tags = "".join([f'<span class="tag">{t}</span>' for t in val['tags']])
        cards_html += f'''
        <div class="cheat-card" onclick="window.location.href='/cheat/{key}'">
            <div class="tag-container">{tags}</div>
            <h3>{val['name']}</h3>
            <p style="color:var(--text-dim); margin-bottom:20px;">{val['desc']}</p>
            <div class="card-meta">
                <span class="version-tag">{val['ver']}</span>
                <button class="heart-btn" data-id="{key}" onclick="event.stopPropagation(); updateFavs('{key}', '{val['name']}')">❤</button>
            </div>
        </div>'''
    
    return render_template_string(f'''
    <html><head>{STYLE}</head><body>
        <div class="bg-glow"></div>
        {get_nav("home")}
        <div class="tg-anchor"><a href="https://t.me/hellokilaura" class="tg-btn">Telegram</a></div>
        <div class="container">
            <div class="hero">
                <h1>Каталог HK Hub</h1>
                <div class="search-wrapper">
                    <input type="text" id="mainSearch" class="search-input" onkeyup="search()" placeholder="Поиск читов...">
                </div>
            </div>
            <div class="cheat-grid">{cards_html}</div>
        </div>
        {SCRIPTS}
    </body></html>''')

@app.route('/cheat/<id>')
def detail(id):
    item = DATABASE.get(id)
    if not item: return "404", 404
    return render_template_string(f'''
    <html><head>{STYLE}</head><body>
        <div class="bg-glow"></div>
        {get_nav("detail")}
        <div class="container">
            <div class="detail-view">
                <a href="/" style="color:var(--accent); text-decoration:none; font-weight:900;">← Назад к списку</a>
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h1 style="font-size:4rem;">{item['name']}</h1>
                    <button class="heart-btn" data-id="{id}" onclick="updateFavs('{id}', '{item['name']}')">❤</button>
                </div>
                <div class="dl-section">
                    <span class="version-tag" style="padding:10px 20px; font-size:1.1rem; border-color:var(--accent); color:white;">Версия: {item['ver']}</span>
                    <p style="font-size:1.5rem; margin:30px 0; color:#ccc;">{item['desc']}</p>
                    <button onclick="forceDownload('{item['file_url']}', '{item['name']}')" class="big-dl-btn">СКАЧАТЬ ОТ HK</button>
                </div>
            </div>
        </div>
        {SCRIPTS}
    </body></html>''')

@app.route('/favs')
def favorites_page():
    return render_template_string(f'''
    <html><head>{STYLE}</head><body>
        <div class="bg-glow"></div>
        {get_nav("favs")}
        <div class="container">
            <div class="hero"><h1>Понравившееся</h1></div>
            <div id="fav-display" class="cheat-grid"></div>
        </div>
        {SCRIPTS}
        <script>
            const data = {DATABASE};
            let f = getFavs();
            let grid = document.getElementById('fav-display');
            if(!f.length) {{
                grid.innerHTML = '<h1 style="grid-column:1/-1; text-align:center; opacity:0.1; font-size:5rem; margin-top:100px;">ПУСТО</h1>';
            }} else {{
                f.forEach(item => {{
                    let c = data[item.id];
                    if(c) {{
                        let tags = c.tags.map(t => `<span class="tag">${{t}}</span>`).join('');
                        grid.innerHTML += `
                        <div class="cheat-card" id="card-fav-${{item.id}}" onclick="window.location.href='/cheat/${{item.id}}'">
                            <div class="tag-container">${{tags}}</div>
                            <h3>${{c.name}}</h3>
                            <p style="color:var(--text-dim); margin-bottom:20px;">${{c.desc}}</p>
                            <div class="card-meta">
                                <span class="version-tag">${{c.ver}}</span>
                                <button class="heart-btn liked" data-id="${{item.id}}" onclick="event.stopPropagation(); updateFavs('${{item.id}}', '${{c.name}}', true)">❤</button>
                            </div>
                        </div>`;
                    }}
                }});
            }}
        </script>
    </body></html>''')

if __name__ == '__main__':
    app.run(debug=True)
