from flask import Flask, render_template_string

app = Flask(__name__)

# --- ENGINE DATABASE (Только рабочие) ---
DATABASE = {
    'wurst': {
        'name': 'Wurst Client',
        'desc': 'Король выживания. Включает в себя более 150 модулей: от AutoMine до KillAura. Идеально сбалансирован для игры на серверах без жесткого античита.',
        'ver': '1.21.1',
        'tags': ['Survival', 'Utility', 'Classic'],
        'color': '#ff4444',
        'file_url': 'https://raw.githubusercontent.com/r1ze-r/HK/main/Wurst-Client1.21.11-hk.jar'
    },
    'meteor': {
        'name': 'Meteor Client',
        'desc': 'Ультимативное решение для PVP и анархии. Лучший CrystalAura на рынке, гибкая настройка HUD и мощная система макросов.',
        'ver': '1.21.1',
        'tags': ['Anarchy', 'PVP', 'Modern'],
        'color': '#2ecc71',
        'file_url': 'https://raw.githubusercontent.com/r1ze-r/HK/main/meteor-client-1.21.11-hk.jar'
    }
}

# --- THEMES & CSS (250+ Lines) ---
STYLE = '''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    :root {
        --bg: #050505; --side: #0a0a0a; --card: #111111; --border: #222222;
        --accent: #ff4444; --accent-glow: rgba(255, 68, 68, 0.2);
        --text: #ffffff; --dim: #888888; --tg: #24A1DE; --green: #2ecc71;
        --transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }

    * { margin: 0; padding: 0; box-sizing: border-box; -webkit-tap-highlight-color: transparent; }

    body {
        background-color: var(--bg); color: var(--text);
        font-family: 'Inter', sans-serif; line-height: 1.6;
        display: flex; min-height: 100vh; overflow-x: hidden;
    }

    /* SIDEBAR SYSTEM */
    .sidebar {
        width: 280px; background: var(--side); border-right: 1px solid var(--border);
        display: flex; flex-direction: column; padding: 40px 25px;
        position: fixed; height: 100vh; z-index: 1000;
        transition: var(--transition);
    }

    .logo-container {
        width: 100px; height: 100px; margin: 0 auto 50px;
        border-radius: 25px; overflow: hidden;
        border: 1px solid var(--border); background: #000;
        position: relative; transition: var(--transition);
    }
    
    .logo-container:hover {
        border-color: var(--accent);
        box-shadow: 0 0 30px var(--accent-glow);
        transform: scale(1.05) rotate(3deg);
    }

    .logo-container img { width: 100%; height: 100%; object-fit: cover; }

    .nav-group { display: flex; flex-direction: column; gap: 12px; }
    
    .nav-item {
        padding: 16px 20px; border-radius: 16px;
        text-decoration: none; color: var(--dim);
        font-weight: 700; font-size: 1rem;
        transition: var(--transition);
        display: flex; align-items: center; gap: 12px;
        border: 1px solid transparent;
    }

    .nav-item:hover, .nav-item.active {
        color: white; background: #151515;
        border-color: var(--border);
    }

    .nav-item.active {
        border-left: 4px solid var(--accent);
        background: linear-gradient(90deg, #151515 0%, transparent 100%);
    }

    .sidebar-footer { margin-top: auto; }

    .tg-btn {
        background: var(--tg); color: white;
        padding: 18px; border-radius: 18px;
        text-decoration: none; font-weight: 900;
        display: flex; align-items: center; justify-content: center;
        gap: 10px; transition: var(--transition);
        box-shadow: 0 10px 30px rgba(36, 161, 222, 0.2);
    }

    .tg-btn:hover { transform: translateY(-5px); filter: brightness(1.1); }

    /* MAIN CONTENT */
    .main {
        margin-left: 280px; flex: 1; padding: 60px;
        background: radial-gradient(circle at 50% 0%, #111 0%, #050505 50%);
    }

    header { margin-bottom: 60px; }
    header h1 { font-size: 3.5rem; font-weight: 900; letter-spacing: -2px; }

    /* SEARCH */
    .search-box {
        position: relative; max-width: 450px; margin-top: 20px;
    }

    .search-input {
        width: 100%; background: #000; border: 1px solid var(--border);
        padding: 15px 25px; border-radius: 15px; color: white;
        font-size: 1rem; outline: none; transition: var(--transition);
    }

    .search-input:focus { border-color: var(--accent); box-shadow: 0 0 20px var(--accent-glow); }

    /* GRID & CARDS */
    .grid {
        display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
        gap: 30px;
    }

    .card {
        background: var(--card); border: 1px solid var(--border);
        border-radius: 30px; padding: 40px; cursor: pointer;
        transition: var(--transition); position: relative;
        display: flex; flex-direction: column; overflow: hidden;
    }

    .card::after {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: radial-gradient(600px circle at var(--x) var(--y), rgba(255,255,255,0.05), transparent 40%);
        pointer-events: none;
    }

    .card:hover {
        transform: translateY(-10px); border-color: #444;
        box-shadow: 0 20px 40px rgba(0,0,0,0.6);
    }

    .card.selected { border-color: var(--accent); background: #1a1111; }

    .card h3 { font-size: 1.8rem; font-weight: 800; color: var(--accent); margin-bottom: 15px; }
    .card p { color: var(--dim); font-size: 1rem; margin-bottom: 30px; line-height: 1.6; flex-grow: 1; }

    .card-footer { display: flex; justify-content: space-between; align-items: center; }
    
    .badge {
        background: #000; padding: 6px 14px; border-radius: 10px;
        font-size: 0.8rem; font-weight: 800; border: 1px solid #222; color: #aaa;
    }

    .heart-btn {
        width: 50px; height: 50px; border-radius: 15px;
        background: #1a1a1a; border: none; color: #333;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.5rem; transition: var(--transition); cursor: pointer;
    }

    .heart-btn:hover { transform: scale(1.1); background: #222; }
    .heart-btn.liked { color: var(--accent); background: rgba(255,68,68,0.1); text-shadow: 0 0 15px var(--accent); }

    /* DETAIL VIEW */
    .detail-container { animation: slideIn 0.5s ease; }
    @keyframes slideIn { from { opacity: 0; transform: translateX(20px); } }

    .dl-btn {
        background: var(--green); color: black; padding: 25px 50px;
        border-radius: 20px; text-decoration: none; font-weight: 900;
        font-size: 1.4rem; display: inline-block; margin-top: 30px;
        transition: var(--transition);
    }
    .dl-btn:hover { transform: scale(1.05); box-shadow: 0 0 40px rgba(46,204,113,0.3); }

    /* FAVS PAGE ACTIONS */
    .fav-controls { display: flex; justify-content: center; gap: 15px; margin-bottom: 50px; }
    .btn-act {
        padding: 15px 30px; border-radius: 15px; border: 1px solid #333;
        background: #111; color: white; font-weight: 700; cursor: pointer; transition: 0.2s;
    }
    .btn-act.active { background: var(--accent); border-color: var(--accent); }
    
    .confirm-pop {
        position: fixed; bottom: 40px; right: 40px;
        background: var(--green); color: black; padding: 25px 50px;
        border-radius: 25px; font-weight: 900; font-size: 1.2rem;
        border: none; cursor: pointer; box-shadow: 0 20px 50px rgba(0,0,0,0.8);
        display: none; z-index: 2000; animation: bounce 0.4s ease;
    }
    @keyframes bounce { 0% { transform: scale(0.5); } 80% { transform: scale(1.1); } 100% { transform: scale(1); } }

    @media (max-width: 1000px) {
        .sidebar { width: 90px; padding: 25px 15px; }
        .sidebar span { display: none; }
        .main { margin-left: 90px; padding: 30px; }
        .logo-container { width: 60px; height: 60px; }
    }
</style>
'''

# --- ENGINE SCRIPTS (150+ Lines) ---
JS = '''
<script>
    let mode = "normal";
    let selected = [];

    // Глобальное хранилище без релоадов
    const STORAGE_KEY = 'hk_911_v7';
    function getFavs() { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); }

    function toggleLike(e, id, name) {
        if(e) e.stopPropagation();
        let favs = getFavs();
        const idx = favs.findIndex(x => x.id === id);
        
        if(idx > -1) favs.splice(idx, 1);
        else favs.push({id, name});
        
        localStorage.setItem(STORAGE_KEY, JSON.stringify(favs));
        
        // Реактивное обновление сердечек
        document.querySelectorAll(`.heart-btn[data-id="${id}"]`).forEach(btn => {
            btn.classList.toggle('liked');
        });

        // Если в избранном - удаляем карточку плавно
        if(document.getElementById('is-fav-page') && idx > -1) {
            const card = document.getElementById('card-'+id);
            if(card) {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                setTimeout(() => card.remove(), 400);
            }
        }
    }

    function handleCard(id) {
        if(mode === 'normal') window.location.href = '/cheat/' + id;
        else if(mode === 'one') toggleLike(null, id);
        else if(mode === 'multi') {
            const card = document.getElementById('card-' + id);
            if(selected.includes(id)) {
                selected = selected.filter(x => x !== id);
                card.classList.remove('selected');
            } else {
                selected.push(id);
                card.classList.add('selected');
            }
        }
    }

    function setMode(m, btn) {
        mode = (mode === m) ? 'normal' : m;
        document.querySelectorAll('.btn-act').forEach(b => b.classList.remove('active'));
        if(mode !== 'normal') btn.classList.add('active');
        
        document.getElementById('confirm-btn').style.display = (mode === 'multi') ? 'block' : 'none';
        
        if(mode === 'normal') {
            document.querySelectorAll('.card').forEach(c => c.classList.remove('selected'));
            selected = [];
        }
    }

    function applyDelete() {
        let favs = getFavs().filter(x => !selected.includes(x.id));
        localStorage.setItem(STORAGE_KEY, JSON.stringify(favs));
        selected.forEach(id => document.getElementById('card-'+id)?.remove());
        setMode('normal');
    }

    function search() {
        let q = document.getElementById('sInp').value.toLowerCase();
        document.querySelectorAll('.card').forEach(c => {
            c.style.display = c.innerText.toLowerCase().includes(q) ? 'flex' : 'none';
        });
    }

    // Эффект следования мыши
    document.addEventListener('mousemove', e => {
        document.querySelectorAll('.card').forEach(card => {
            const r = card.getBoundingClientRect();
            card.style.setProperty('--x', `${e.clientX - r.left}px`);
            card.style.setProperty('--y', `${e.clientY - r.top}px`);
        });
    });

    // Инит лайков
    window.addEventListener('DOMContentLoaded', () => {
        const favs = getFavs();
        document.querySelectorAll('.heart-btn').forEach(b => {
            if(favs.some(f => f.id === b.dataset.id)) b.classList.add('liked');
        });
    });
</script>
'''

def get_base(content, active='home'):
    return render_template_string(f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>HK HUB</title>
        <link rel="icon" type="image/png" href="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png">
        {STYLE}
    </head>
    <body>
        <div class="sidebar">
            <div class="logo-container">
                <img src="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png">
            </div>
            <div class="nav-group">
                <a href="/" class="nav-item {'active' if active=='home' else ''}"><span>Главная</span></a>
                <a href="/favs" class="nav-item {'active' if active=='favs' else ''}"><span>Избранное</span></a>
            </div>
            <div class="sidebar-footer">
                <a href="https://t.me/hellokilaura" class="tg-btn" target="_blank">Telegram</a>
            </div>
        </div>
        <div class="main">{content}</div>
        {JS}
    </body>
    </html>
    ''')

@app.route('/')
def home():
    cards = ""
    for k, v in DATABASE.items():
        cards += f'''
        <div class="card" id="card-{k}" onclick="handleCard('{k}')">
            <h3>{v['name']}</h3>
            <p>{v['desc']}</p>
            <div class="card-footer">
                <span class="badge">{v['ver']}</span>
                <button class="heart-btn" data-id="{k}" onclick="toggleLike(event, '{k}', '{v['name']}')">❤</button>
            </div>
        </div>'''
    content = f'''
        <header>
            <h1>Все читы</h1>
            <div class="search-box">
                <input type="text" id="sInp" class="search-input" onkeyup="search()" placeholder="Поиск по названию...">
            </div>
        </header>
        <div class="grid">{cards}</div>
    '''
    return get_base(content, 'home')

@app.route('/cheat/<id>')
def cheat(id):
    item = DATABASE.get(id)
    if not item: return "404", 404
    content = f'''
        <div class="detail-container">
            <a href="/" style="color:var(--accent); text-decoration:none; font-weight:900;">← В КАТАЛОГ</a>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:40px;">
                <h1 style="font-size:4.5rem;">{item['name']}</h1>
                <button class="heart-btn" data-id="{id}" onclick="toggleLike(event, '{id}', '{item['name']}')" style="width:80px; height:80px; font-size:2.5rem;">❤</button>
            </div>
            <div style="background:var(--card); padding:50px; border-radius:40px; border:1px solid var(--border); margin-top:50px; position:relative;">
                <span class="badge" style="font-size:1rem; padding:10px 20px;">Версия: {item['ver']}</span>
                <p style="font-size:1.6rem; color:#bbb; margin:40px 0; line-height:1.7;">{item['desc']}</p>
                <a href="{item['file_url']}" class="dl-btn">СКАЧАТЬ КЛИЕНТ (.JAR)</a>
            </div>
        </div>
    '''
    return get_base(content, 'home')

@app.route('/favs')
def favs():
    content = f'''
        <div id="is-fav-page"></div>
        <button id="confirm-btn" class="confirm-pop" onclick="applyDelete()">Убрать выбранное</button>
        <header><h1>Избранное</h1></header>
        <div class="fav-controls">
            <button class="btn-act" onclick="localStorage.setItem('hk_911_v7','[]'); location.reload();">Очистить всё</button>
            <button class="btn-act" onclick="setMode('multi', this)">Выбрать несколько</button>
            <button class="btn-act" onclick="setMode('one', this)">Удалить одним кликом</button>
        </div>
        <div id="fGrid" class="grid"></div>
        <script>
            const db = {DATABASE};
            const f = JSON.parse(localStorage.getItem('hk_911_v7') || '[]');
            const g = document.getElementById('fGrid');
            if(!f.length) g.innerHTML = '<h2 style="grid-column:1/-1; text-align:center; opacity:0.1; font-size:5rem; margin-top:100px;">ПУСТО</h2>';
            else f.forEach(x => {{
                const i = db[x.id] || {{name: x.name, desc: 'Нажмите для просмотра', ver: '?'}};
                g.innerHTML += `
                <div class="card" id="card-${{x.id}}" onclick="handleCard('${{x.id}}')">
                    <h3>${{i.name}}</h3><p>${{i.desc}}</p>
                    <div class="card-footer">
                        <span class="badge">${{i.ver}}</span>
                        <button class="heart-btn liked" data-id="${{x.id}}" onclick="toggleLike(event, '${{x.id}}')">❤</button>
                    </div>
                </div>`;
            }});
        </script>
    '''
    return get_base(content, 'favs')

if __name__ == '__main__':
    app.run(debug=True)
