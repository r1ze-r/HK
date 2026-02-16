from flask import Flask, render_template_string

app = Flask(__name__)

# МАКСИМАЛЬНО ПОЛНЫЙ КОНФИГ СТИЛЕЙ
STYLE = '''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&display=swap');
    :root { --bg: #0a0a0a; --card: #161616; --accent: #ff4444; --green: #2ecc71; --tg: #24A1DE; --text: #ffffff; --subtext: #a1a1a1; --modal-bg: rgba(0,0,0,0.95); }
    
    body { background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; margin: 0; display: flex; min-height: 100vh; overflow-x: hidden; }
    
    /* SIDEBAR (КНОПКИ СЛЕВА ВНИЗУ) */
    .sidebar { width: 260px; background: var(--card); height: 100vh; padding: 30px 20px; box-sizing: border-box; display: flex; flex-direction: column; border-right: 1px solid #222; position: fixed; z-index: 100; }
    .logo-sidebar { text-align: center; margin-bottom: 40px; }
    .logo-sidebar img { width: 100px; height: 100px; border-radius: 20px; filter: drop-shadow(0 0 8px var(--accent)); transition: 0.3s; }
    .logo-sidebar img:hover { transform: scale(1.05); }
    
    .nav-group { display: flex; flex-direction: column; gap: 10px; }
    .nav-item { padding: 14px 18px; border-radius: 12px; cursor: pointer; color: var(--subtext); transition: 0.3s; text-decoration: none; font-weight: 600; font-size: 1rem; }
    .nav-item:hover, .nav-item.active { background: #222; color: white; transform: translateX(5px); }
    
    .sidebar-bottom { margin-top: auto; display: flex; flex-direction: column; gap: 12px; }
    .btn-tg { background: var(--tg); color: white; padding: 14px; border-radius: 12px; text-decoration: none; font-weight: 800; text-align: center; font-size: 0.9rem; transition: 0.3s; border: none; }
    .btn-tg:hover { filter: brightness(1.1); transform: translateY(-2px); }
    .btn-dl-sidebar { background: var(--green); color: black; padding: 14px; border-radius: 12px; text-decoration: none; font-weight: 800; text-align: center; display: none; cursor: pointer; border: none; }

    .main { flex: 1; padding: 30px 50px; margin-left: 260px; width: calc(100% - 260px); box-sizing: border-box; position: relative; }

    /* HEADER & ПОИСК ПО ЦЕНТРУ */
    .header-home { display: flex; align-items: center; margin-bottom: 50px; position: relative; width: 100%; }
    .search-container { position: absolute; left: 45%; transform: translateX(-50%); }
    .search-container input { width: 240px; background: #1a1a1a; border: 1px solid #333; padding: 12px 20px; border-radius: 12px; color: white; outline: none; transition: 0.3s; }
    .search-container input:focus { border-color: var(--accent); width: 280px; box-shadow: 0 0 15px rgba(255, 68, 68, 0.2); }

    /* ГРИД И КАРТОЧКИ */
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 25px; }
    .card { background: var(--card); border-radius: 20px; border: 1px solid #222; padding: 25px; transition: 0.3s; cursor: pointer; position: relative; display: flex; flex-direction: column; }
    .card:hover { border-color: #444; transform: translateY(-5px); }
    .card.selected-for-del { border-color: var(--accent) !important; box-shadow: 0 0 15px rgba(255, 68, 68, 0.4); }
    
    .card h3 { margin: 0; color: var(--accent); font-size: 1.3rem; font-weight: 800; }
    .card p { margin: 15px 0 20px 0; font-size: 0.95rem; color: var(--subtext); line-height: 1.5; min-height: 40px; }
    
    .card-footer { display: flex; align-items: center; gap: 12px; margin-top: auto; }
    .ver-badge { font-size: 0.75rem; color: #888; background: #1a1a1a; padding: 3px 10px; border-radius: 6px; border: 1px solid #333; font-weight: 600; }
    .heart-mini { font-size: 1.2rem; color: #2a2a2a; transition: 0.2s; background: none; border: none; cursor: pointer; padding: 0; }
    .heart-mini.liked { color: var(--accent); filter: drop-shadow(0 0 5px var(--accent)); }

    /* ИЗБРАННОЕ УПРАВЛЕНИЕ */
    .fav-controls { display: flex; justify-content: center; gap: 12px; margin-bottom: 40px; }
    .btn-fav-act { padding: 12px 20px; border-radius: 12px; font-weight: 800; cursor: pointer; border: 1px solid #333; background: #1a1a1a; color: white; font-size: 0.85rem; transition: 0.2s; flex: 1; max-width: 200px; }
    .btn-fav-act.active-red { background: var(--accent); border-color: var(--accent); }
    .btn-green-confirm { background: var(--green); color: black; border: none; display: none; }
    .empty-msg { position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); color: var(--subtext); font-size: 1.4rem; font-weight: 600; }

    /* MOBILE ВЕРСТКА */
    @media (max-width: 850px) {
        .sidebar { display: none; }
        .main { margin-left: 0; padding: 20px; width: 100%; padding-bottom: 100px; }
        .mobile-nav-top { display: flex; justify-content: space-around; background: var(--card); padding: 15px; margin: -20px -20px 25px -20px; border-bottom: 1px solid #222; position: sticky; top: 0; z-index: 1000; }
        .search-container { position: static; transform: none; width: 100%; margin-bottom: 25px; }
        .search-container input { width: 100% !important; }
        .pc-warn-dotted { background: #1a1a1a; color: #666; border: 2px dashed #444; padding: 12px; border-radius: 12px; font-size: 0.85rem; text-align: center; flex: 1; margin-left: 15px; font-weight: 800; }
        .fav-controls { flex-direction: row; gap: 8px; }
        .btn-fav-act { padding: 10px 5px; font-size: 0.75rem; }
        .mobile-tg-fix { position: fixed; bottom: 0; left: 0; right: 0; padding: 20px; background: linear-gradient(transparent, var(--bg)); z-index: 1000; }
    }

    /* MODAL */
    .modal { display: none; position: fixed; z-index: 2000; left: 0; top: 0; width: 100%; height: 100%; background: var(--modal-bg); align-items: center; justify-content: center; backdrop-filter: blur(4px); }
    .modal-box { background: var(--card); padding: 35px; border-radius: 20px; border: 1px solid #333; text-align: center; width: 90%; max-width: 400px; }
    .modal-btns { display: flex; gap: 15px; justify-content: center; margin-top: 25px; }
</style>
'''

SCRIPTS = '''
<script>
    let currentMode = ""; 
    let selectedForDeletion = [];

    function forceDownload(url, filename) {
        fetch(url).then(t => t.blob()).then(b => {
            const a = document.createElement("a");
            a.href = window.URL.createObjectURL(b);
            a.download = filename;
            a.click();
        });
    }

    function toggleLike(id, name) {
        let favs = JSON.parse(localStorage.getItem('hk_favs') || '[]');
        let idx = favs.findIndex(x => x.id === id);
        if(idx > -1) favs.splice(idx, 1); else favs.push({id, name});
        localStorage.setItem('hk_favs', JSON.stringify(favs));
        location.reload();
    }

    function setFavMode(m) {
        currentMode = (currentMode === m) ? "" : m;
        document.querySelectorAll('.btn-fav-act').forEach(b => b.classList.remove('active-red'));
        document.getElementById('confirm-ubrat-btn').style.display = (currentMode === 'del') ? 'block' : 'none';
        if(currentMode) event.target.classList.add('active-red');
        if(!currentMode) { 
            selectedForDeletion = []; 
            document.querySelectorAll('.card').forEach(c => c.classList.remove('selected-for-del')); 
        }
    }

    function handleCardClick(id) {
        if(currentMode === 'one') {
            toggleLike(id);
        } else if(currentMode === 'del') {
            const cardEl = document.getElementById('card-'+id);
            if(selectedForDeletion.includes(id)) {
                selectedForDeletion = selectedForDeletion.filter(x => x !== id);
                cardEl.classList.remove('selected-for-del');
            } else {
                selectedForDeletion.push(id);
                cardEl.classList.add('selected-for-del');
            }
        } else {
            window.location.href = '/' + id;
        }
    }

    function applyDeleteSelected() {
        let favs = JSON.parse(localStorage.getItem('hk_favs') || '[]');
        favs = favs.filter(x => !selectedForDeletion.includes(x.id));
        localStorage.setItem('hk_favs', JSON.stringify(favs));
        location.reload();
    }

    function liveSearch() {
        let val = document.getElementById('searchBox').value.toLowerCase();
        document.querySelectorAll('.card').forEach(c => {
            let text = c.innerText.toLowerCase();
            c.style.display = text.includes(val) ? "flex" : "none";
        });
    }
</script>
'''

CHEATS_DATABASE = {
    'wurst': {'name': 'Wurst Client', 'desc': 'Легендарный чит для выживания. Огромный функционал и простота.', 'ver': '1.21.11', 'url': 'https://raw.githubusercontent.com/r1ze-r/HK/main/Wurst-Client1.21.11-hk.jar'},
    'meteor': {'name': 'Meteor Client', 'desc': 'Самый популярный чит для PVP и анархии. Постоянные обновления.', 'ver': '1.21.11', 'url': 'https://raw.githubusercontent.com/r1ze-r/HK/main/meteor-client-1.21.11-hk.jar'}
}

@app.route('/')
def home():
    cards_html = "".join([f'<div class="card" onclick="handleCardClick(\'{k}\')"><h3>{v["name"]}</h3><p>{v["desc"]}</p><div class="card-footer"><span class="ver-badge">{v["ver"]}</span></div></div>' for k,v in CHEATS_DATABASE.items()])
    return render_template_string(f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>HK - Главная</title>{STYLE}</head><body>
        <div class="sidebar"><div class="logo-sidebar"><img src="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png"></div><div class="nav-group"><a href="/" class="nav-item active">Главная</a><a href="/favs" class="nav-item">Понравившееся</a></div><div class="sidebar-bottom"><a href="https://t.me/hellokilaura" class="btn-tg">Telegram</a></div></div>
        <div class="main"><div class="mobile-nav-top"><a href="/" class="nav-item active">Главная</a><a href="/favs" class="nav-item">Понравившееся</a></div>
        <div class="header-home"><h1>Все читы</h1><div class="search-container"><input type="text" id="searchBox" onkeyup="liveSearch()" placeholder="Поиск читов..."></div></div>
        <div class="grid">{cards_html}</div></div><div class="mobile-tg-fix"><a href="https://t.me/hellokilaura" class="btn-tg" style="display:block;text-align:center;">Telegram</a></div>{SCRIPTS}</body></html>''')

@app.route('/<name>')
def detail(name):
    item = CHEATS_DATABASE.get(name)
    if not item: return "404", 404
    return render_template_string(f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>{item['name']}</title>{STYLE}</head><body>
        <div class="sidebar"><div class="logo-sidebar"><img src="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png"></div><div class="nav-group"><a href="/" class="nav-item">Главная</a><a href="/favs" class="nav-item">Понравившееся</a></div><div class="sidebar-bottom"><button onclick="forceDownload('{item['url']}', '{name.capitalize()}_HK.jar')" class="btn-dl-sidebar" style="display:block;">Скачать .jar</button><a href="https://t.me/hellokilaura" class="btn-tg">Telegram</a></div></div>
        <div class="main">
            <div style="display:flex;align-items:center;">
                <a href="/" style="color:var(--accent);text-decoration:none;font-weight:800;font-size:1.1rem;">← НАЗАД</a>
                <div class="pc-warn-dotted" id="pcd" style="display:none;">СКАЧАТЬ МОЖНО ТОЛЬКО НА ПК</div>
                <button class="heart-mini" id="heartBtn" onclick="toggleLike('{name}')" style="font-size:2.5rem;margin-left:auto;">❤</button>
            </div>
            <div style="margin-top:30px;">
                <h1 style="font-size:2.5rem;margin-bottom:10px;">{item['name']} <span class="ver-badge" style="font-size:0.9rem;">{item['ver']}</span></h1>
                <p style="color:var(--subtext);max-width:700px;font-size:1.1rem;line-height:1.7;">{item['desc']}</p>
            </div>
        </div>
        <script>if(window.innerWidth < 850) document.getElementById('pcd').style.display='block';
        let favs = JSON.parse(localStorage.getItem('hk_favs')||'[]'); if(favs.some(x=>x.id==='{name}')) document.getElementById('heartBtn').classList.add('liked');</script>
        <div class="mobile-tg-fix"><a href="https://t.me/hellokilaura" class="btn-tg" style="display:block;text-align:center;">Telegram</a></div>{SCRIPTS}</body></html>''')

@app.route('/favs')
def favorites():
    return render_template_string(f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>HK - Избранное</title>{STYLE}</head><body>
        <div class="sidebar"><div class="logo-sidebar"><img src="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png"></div><div class="nav-group"><a href="/" class="nav-item">Главная</a><a href="/favs" class="nav-item active">Понравившееся</a></div></div>
        <div class="main"><div class="mobile-nav-top"><a href="/" class="nav-item">Главная</a><a href="/favs" class="nav-item active">Понравившееся</a></div>
        <h1 style="text-align:center;margin-bottom:30px;">Понравившееся</h1>
        <div class="fav-controls">
            <button class="btn-fav-act" onclick="document.getElementById('modalAll').style.display='flex'">Удалить всё</button>
            <button class="btn-fav-act" onclick="setFavMode('del')">Удалить выбранное</button>
            <button class="btn-fav-act" onclick="setFavMode('one')">Удалить одно</button>
            <button class="btn-fav-act btn-green-confirm" id="confirm-ubrat-btn" onclick="applyDeleteSelected()">Убрать выбранное</button>
        </div>
        <div id="favGrid" class="grid"></div>
        <div id="modalAll" class="modal"><div class="modal-box"><h3>Удалить всё из избранного?</h3><div class="modal-btns">
            <button onclick="localStorage.setItem('hk_favs','[]');location.reload()" style="background:var(--accent);color:white;border:none;padding:12px 30px;border-radius:10px;font-weight:800;cursor:pointer;">ДА</button>
            <button onclick="document.getElementById('modalAll').style.display='none'" style="background:none;border:1px solid #444;color:white;padding:12px 30px;border-radius:10px;font-weight:800;cursor:pointer;">НЕТ</button>
        </div></div></div></div>
        <div class="mobile-tg-fix"><a href="https://t.me/hellokilaura" class="btn-tg" style="display:block;text-align:center;">Telegram</a></div>
        <script>
            let f = JSON.parse(localStorage.getItem('hk_favs')||'[]');
            let grid = document.getElementById('favGrid');
            const data = {CHEATS_DATABASE};
            if(!f.length) grid.innerHTML = '<div class="empty-msg">Тут пока пусто.</div>';
            else f.forEach(x => {{
                let info = data[x.id] || {{name:x.name, desc:'Просмотр чита', ver:''}};
                grid.innerHTML += `<div class="card" id="card-${{x.id}}" onclick="handleCardClick('${{x.id}}')">
                    <h3>${{info.name}}</h3><p>${{info.desc}}</p>
                    <div class="card-footer"><span class="ver-badge">${{info.ver}}</span><span class="heart-mini liked" style="margin-left:auto;">❤</span></div>
                </div>`;
            }});
        </script>{SCRIPTS}</body></html>''')
