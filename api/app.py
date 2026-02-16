from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# --- CONFIG DATA ---
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
    },
    'impact': {
        'name': 'Impact Client',
        'desc': 'Легендарный клиент для старых версий и анархии. Знаменит своим Baritone-интеграцией и удобным ClickGUI.',
        'ver': '1.12.2',
        'tags': ['Oldschool', 'Anarchy', 'Baritone'],
        'color': '#3498db',
        'file_url': '#'
    },
    'aristois': {
        'name': 'Aristois',
        'desc': 'Универсальный чит с поддержкой всех версий Minecraft. Имеет встроенный менеджер аддонов и активное сообщество.',
        'ver': '1.20.4',
        'tags': ['Universal', 'Addons', 'UI'],
        'color': '#9b59b6',
        'file_url': '#'
    }
}

# --- THEMES & CSS (250+ Lines of Styling) ---
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

    * { margin: 0; padding: 0; box-sizing: border-box; -webkit-tap-highlight-color: transparent; }

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

    /* BACKGROUND ANIMATION */
    .bg-glow {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: radial-gradient(circle at 50% 50%, rgba(20, 20, 20, 1) 0%, rgba(5, 5, 5, 1) 100%);
        z-index: -1;
    }

    /* TOP NAVIGATION */
    header {
        position: sticky; top: 0; z-index: 1000;
        background: var(--glass);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid var(--card-border);
        padding: 20px 0;
    }

    .nav-container {
        max-width: 1200px; margin: 0 auto;
        display: flex; justify-content: center; align-items: center; gap: 15px;
        padding: 0 20px;
    }

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

    /* MAIN CONTENT */
    .container { max-width: 1200px; margin: 0 auto; padding: 60px 20px; }

    .hero { text-align: center; margin-bottom: 70px; }
    .hero h1 { 
        font-size: 4rem; font-weight: 900; letter-spacing: -2px; 
        margin-bottom: 15px; background: linear-gradient(to bottom, #fff 0%, #666 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }

    .search-wrapper {
        position: relative; width: 100%; max-width: 500px; margin: 30px auto;
    }

    .search-input {
        width: 100%; background: #111; border: 1px solid #222;
        padding: 18px 30px; border-radius: 20px; color: white;
        font-size: 1.1rem; font-weight: 500; outline: none;
        transition: var(--transition);
        text-align: center;
    }

    .search-input:focus {
        border-color: var(--accent); box-shadow: 0 0 30px var(--accent-glow);
        width: 110%; transform: translateX(-4.5%);
    }

    /* GRID & CARDS */
    .cheat-grid {
        display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
        gap: 30px; animation: fadeInUp 0.8s ease;
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .cheat-card {
        background: var(--card-bg); border: 1px solid var(--card-border);
        border-radius: 28px; padding: 35px; position: relative;
        transition: var(--transition); cursor: pointer;
        display: flex; flex-direction: column; overflow: hidden;
    }

    .cheat-card::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: radial-gradient(800px circle at var(--x) var(--y), rgba(255,255,255,0.06), transparent 40%);
        pointer-events: none;
    }

    .cheat-card:hover {
        border-color: #444; transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }

    .cheat-card.selected { border-color: var(--accent); box-shadow: 0 0 20px var(--accent-glow); }

    .cheat-card h3 { font-size: 1.8rem; font-weight: 800; color: var(--accent); margin-bottom: 12px; }
    .cheat-card p { color: var(--text-dim); font-size: 0.95rem; margin-bottom: 25px; min-height: 60px; }

    .tag-container { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 20px; }
    .tag { font-size: 0.7rem; font-weight: 700; text-transform: uppercase; background: #1a1a1a; padding: 4px 12px; border-radius: 6px; color: #666; }

    .card-meta { display: flex; align-items: center; justify-content: space-between; margin-top: auto; }
    .version-tag { background: #000; padding: 5px 12px; border-radius: 10px; border: 1px solid #222; font-size: 0.8rem; font-weight: 700; color: #aaa; }

    .heart-btn {
        width: 45px; height: 45px; border-radius: 12px;
        background: #1a1a1a; border: none; color: #333;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.4rem; cursor: pointer; transition: 0.3s;
    }
    .heart-btn.liked { color: var(--accent); background: rgba(255,68,68,0.1); }

    /* TELEGRAM FIXED */
    .tg-anchor {
        position: fixed; left: 40px; bottom: 40px; z-index: 999;
    }

    .tg-btn {
        background: var(--tg-color); color: white;
        padding: 18px 30px; border-radius: 20px;
        text-decoration: none; font-weight: 900;
        display: flex; align-items: center; gap: 12px;
        box-shadow: 0 10px 30px rgba(36, 161, 222, 0.4);
        transition: var(--transition);
    }

    .tg-btn:hover { transform: scale(1.05) rotate(-2deg); }

    /* FAVORITES LOGIC UI */
    .fav-header { display: flex; justify-content: center; gap: 15px; margin-bottom: 50px; position: relative; }
    .action-btn {
        padding: 14px 25px; border-radius: 15px; border: 1px solid #333;
        background: #111; color: white; font-weight: 700; cursor: pointer;
        transition: 0.2s; font-size: 0.9rem;
    }
    .action-btn.danger { border-color: var(--accent); color: var(--accent); }
    .action-btn.danger:hover { background: var(--accent); color: white; }
    .action-btn.active { background: var(--accent); border-color: var(--accent); }
    
    .floating-confirm {
        position: fixed; bottom: 40px; right: 40px;
        background: var(--green); color: black;
        padding: 20px 40px; border-radius: 20px;
        font-weight: 900; font-size: 1.1rem;
        cursor: pointer; display: none; z-index: 1001;
        box-shadow: 0 10px 40px rgba(46, 204, 113, 0.4);
        border: none; animation: pop 0.3s ease;
    }

    @keyframes pop { from { transform: scale(0.8); opacity: 0; } }

    /* DETAIL PAGE */
    .detail-view { display: flex; flex-direction: column; align-items: flex-start; gap: 40px; }
    .back-btn { font-weight: 900; color: var(--accent); text-decoration: none; font-size: 1.1rem; display: flex; align-items: center; gap: 10px; }
    .dl-section { width: 100%; padding: 40px; background: var(--card-bg); border-radius: 30px; border: 1px solid #222; }
    .big-dl-btn {
        background: var(--green); color: black; padding: 25px 60px;
        border-radius: 20px; text-decoration: none; font-weight: 900;
        font-size: 1.5rem; display: inline-block; transition: var(--transition);
    }
    .big-dl-btn:hover { transform: scale(1.03); box-shadow: 0 0 40px rgba(46,204,113,0.3); }

    /* MOBILE OPTIMIZATION */
    @media (max-width: 800px) {
        .hero h1 { font-size: 2.5rem; }
        .tg-anchor { left: 20px; bottom: 20px; right: 20px; }
        .tg-btn { justify-content: center; width: 100%; }
        .cheat-grid { grid-template-columns: 1fr; }
        .nav-container { gap: 8px; }
        .nav-btn { padding: 10px 15px; font-size: 0.8rem; }
        .search-input:focus { width: 100%; transform: none; }
        .floating-confirm { left: 20px; right: 20px; bottom: 100px; text-align: center; }
    }
</style>
'''

# --- ENGINE SCRIPTS (150+ Lines of JavaScript) ---
SCRIPTS = '''
<script>
    // --- State Management ---
    let currentMode = "normal";
    let selectedCheats = [];

    // --- Core Functions ---
    function updateFavs(id, name) {
        let favs = JSON.parse(localStorage.getItem('hk_v3_favs') || '[]');
        let index = favs.findIndex(item => item.id === id);
        
        if (index > -1) {
            favs.splice(index, 1);
        } else {
            favs.push({id: id, name: name});
        }
        localStorage.setItem('hk_v3_favs', JSON.stringify(favs));
        refreshUI();
    }

    function refreshUI() {
        if (window.location.pathname === '/favs') location.reload();
        // Update heart icons on main page
        let favs = JSON.parse(localStorage.getItem('hk_v3_favs') || '[]');
        document.querySelectorAll('.heart-btn').forEach(btn => {
            let id = btn.getAttribute('data-id');
            if (favs.some(f => f.id === id)) btn.classList.add('liked');
            else btn.classList.remove('liked');
        });
    }

    function setFavMode(mode) {
        currentMode = (currentMode === mode) ? "normal" : mode;
        
        // Reset styles
        document.querySelectorAll('.action-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.cheat-card').forEach(c => c.classList.remove('selected'));
        selectedCheats = [];
        
        if (currentMode !== "normal") {
            event.target.classList.add('active');
        }
        
        document.getElementById('confirm-float').style.display = (currentMode === 'delete_multi') ? 'block' : 'none';
    }

    function handleCheatClick(id) {
        if (currentMode === "normal") {
            window.location.href = '/cheat/' + id;
        } else if (currentMode === "delete_single") {
            updateFavs(id);
        } else if (currentMode === "delete_multi") {
            const card = document.getElementById('card-' + id);
            if (selectedCheats.includes(id)) {
                selectedCheats = selectedCheats.filter(i => i !== id);
                card.classList.remove('selected');
            } else {
                selectedCheats.push(id);
                card.classList.add('selected');
            }
        }
    }

    function applyMultiDelete() {
        let favs = JSON.parse(localStorage.getItem('hk_v3_favs') || '[]');
        favs = favs.filter(item => !selectedCheats.includes(item.id));
        localStorage.setItem('hk_favs', JSON.stringify(favs)); // Sync with old keys if needed
        localStorage.setItem('hk_v3_favs', JSON.stringify(favs));
        location.reload();
    }

    function search() {
        let query = document.getElementById('mainSearch').value.toLowerCase();
        document.querySelectorAll('.cheat-card').forEach(card => {
            let content = card.innerText.toLowerCase();
            card.style.display = content.includes(query) ? 'flex' : 'none';
        });
    }

    // --- Visual FX ---
    document.addEventListener('mousemove', e => {
        document.querySelectorAll('.cheat-card').forEach(card => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            card.style.setProperty('--x', `${x}px`);
            card.style.setProperty('--y', `${y}px`);
        });
    });

    // --- Init ---
    window.onload = refreshUI;
</script>
'''

@app.route('/')
def home():
    cards_html = ""
    for key, val in DATABASE.items():
        tags = "".join([f'<span class="tag">{t}</span>' for t in val['tags']])
        cards_html += f'''
        <div class="cheat-card" id="card-{key}" onclick="handleCheatClick('{key}')">
            <div class="tag-container">{tags}</div>
            <h3>{val['name']}</h3>
            <p>{val['desc']}</p>
            <div class="card-meta">
                <span class="version-tag">{val['ver']}</span>
                <button class="heart-btn" data-id="{key}" onclick="event.stopPropagation(); updateFavs('{key}', '{val['name']}')">❤</button>
            </div>
        </div>
        '''
    
    return render_template_string(f'''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>HK Hub | Porsche Edition</title>
        <link rel="icon" type="image/png" href="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png">
        {STYLE}
    </head>
    <body>
        <div class="bg-glow"></div>
        <header>
            <div class="nav-container">
                <a href="/" class="nav-btn active">Главная</a>
                <a href="/favs" class="nav-btn">Понравившееся</a>
            </div>
        </header>

        <div class="tg-anchor">
            <a href="https://t.me/hellokilaura" class="tg-btn">
                <span>Наш Telegram</span>
            </a>
        </div>

        <div class="container">
            <div class="hero">
                <h1>Все Читы</h1>
                <div class="search-wrapper">
                    <input type="text" id="mainSearch" class="search-input" onkeyup="search()" placeholder="Поиск по названию или версии...">
                </div>
            </div>
            
            <div class="cheat-grid">
                {cards_html}
            </div>
        </div>

        {SCRIPTS}
    </body>
    </html>
    ''')

@app.route('/cheat/<id>')
def detail(id):
    item = DATABASE.get(id)
    if not item: return "Cheat Not Found", 404
    
    return render_template_string(f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{item['name']} - HK</title>
        {STYLE}
    </head>
    <body>
        <header><div class="nav-container"><a href="/" class="nav-btn">Главная</a><a href="/favs" class="nav-btn">Понравившееся</a></div></header>
        <div class="tg-anchor"><a href="https://t.me/hellokilaura" class="tg-btn">Telegram</a></div>
        
        <div class="container">
            <div class="detail-view">
                <a href="/" class="back-btn">← Назад в каталог</a>
                
                <div style="display:flex; justify-content:space-between; width:100%; align-items:center;">
                    <h1 style="font-size:4rem; font-weight:900;">{item['name']}</h1>
                    <button class="heart-btn liked" style="width:80px; height:80px; font-size:2.5rem;">❤</button>
                </div>

                <div class="dl-section">
                    <span class="version-tag" style="font-size:1.2rem; padding:10px 20px; border-color:var(--accent); color:white;">Версия: {item['ver']}</span>
                    <p style="font-size:1.5rem; margin:30px 0; color:#ccc;">{item['desc']}</p>
                    <a href="{item['file_url']}" class="big-dl-btn">Скачать .JAR Клиент</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    ''')

@app.route('/favs')
def favorites_page():
    return render_template_string(f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Избранное - HK</title>
        {STYLE}
    </head>
    <body>
        <div class="bg-glow"></div>
        <header><div class="nav-container"><a href="/" class="nav-btn">Главная</a><a href="/favs" class="nav-btn active">Понравившееся</a></div></header>
        <div class="tg-anchor"><a href="https://t.me/hellokilaura" class="tg-btn">Telegram</a></div>

        <button id="confirm-float" class="floating-confirm" onclick="applyMultiDelete()">Убрать выбранное</button>

        <div class="container">
            <div class="hero">
                <h1>Твоя Коллекция</h1>
                <div class="fav-header">
                    <button class="action-btn danger" onclick="localStorage.setItem('hk_v3_favs', '[]'); location.reload();">Удалить всё</button>
                    <button class="action-btn" onclick="setMode('delete_multi')">Удалить выбранное</button>
                    <button class="action-btn" onclick="setMode('delete_single')">Удалить по одному</button>
                </div>
            </div>

            <div id="fav-display" class="cheat-grid">
                </div>
        </div>

        {SCRIPTS}
        <script>
            const data = {DATABASE};
            let f = JSON.parse(localStorage.getItem('hk_v3_favs') || '[]');
            let grid = document.getElementById('fav-display');

            if(f.length === 0) {{
                grid.innerHTML = '<div style="grid-column:1/-1; text-align:center; padding:100px; color:#333; font-size:2rem; font-weight:900;">ПУСТО</div>';
            }} else {{
                f.forEach(item => {{
                    let c = data[item.id] || {{name: item.name, desc: 'Нажмите для просмотра', ver: '?', tags: ['Fav']}};
                    let tags = c.tags.map(t => `<span class="tag">${{t}}</span>`).join('');
                    grid.innerHTML += `
                        <div class="cheat-card" id="card-${{item.id}}" onclick="handleCheatClick('${{item.id}}')">
                            <div class="tag-container">${{tags}}</div>
                            <h3>${{c.name}}</h3>
                            <p>${{c.desc}}</p>
                            <div class="card-meta">
                                <span class="version-tag">${{c.ver}}</span>
                                <button class="heart-btn liked">❤</button>
                            </div>
                        </div>`;
                }});
            }}
        </script>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
