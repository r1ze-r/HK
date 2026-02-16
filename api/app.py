from flask import Flask, render_template_string

app = Flask(__name__)

STYLE = '''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    :root { --bg: #0a0a0a; --card: #161616; --accent: #ff4444; --green: #2ecc71; --tg: #24A1DE; --text: #ffffff; --subtext: #a1a1a1; }
    
    body { background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; margin: 0; display: flex; min-height: 100vh; overflow-x: hidden; }
    
    /* SIDEBAR ПК */
    .sidebar { width: 260px; background: var(--card); height: 100vh; padding: 30px 20px; box-sizing: border-box; display: flex; flex-direction: column; border-right: 1px solid #222; position: fixed; z-index: 100; }
    .logo-area { text-align: center; margin-bottom: 40px; }
    .logo-area img { width: 90px; height: 90px; border-radius: 20px; filter: drop-shadow(0 0 10px var(--accent)); }
    
    .nav-item { padding: 14px 18px; border-radius: 12px; cursor: pointer; color: var(--subtext); transition: 0.3s; text-decoration: none; font-weight: 600; display: block; margin-bottom: 8px; }
    .nav-item:hover, .nav-item.active { background: #222; color: white; }
    
    .sidebar-bottom { margin-top: auto; display: flex; flex-direction: column; gap: 12px; }
    .btn-tg { background: var(--tg); color: white; padding: 14px; border-radius: 12px; text-decoration: none; font-weight: 800; text-align: center; }

    .main { flex: 1; padding: 30px 50px; margin-left: 260px; width: calc(100% - 260px); position: relative; }

    /* HEADER & SEARCH */
    .header-home { display: flex; align-items: center; margin-bottom: 45px; position: relative; }
    .search-wrap { position: absolute; left: 50%; transform: translateX(-50%); }
    .search-wrap input { width: 260px; background: #1a1a1a; border: 1px solid #333; padding: 12px 20px; border-radius: 14px; color: white; outline: none; transition: 0.3s; }
    .search-wrap input:focus { border-color: var(--accent); box-shadow: 0 0 15px rgba(255, 68, 68, 0.2); }

    /* CARDS */
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(310px, 1fr)); gap: 25px; }
    .card { background: var(--card); border-radius: 20px; border: 1px solid #222; padding: 25px; transition: 0.3s; cursor: pointer; position: relative; display: flex; flex-direction: column; }
    .card:hover { border-color: #444; transform: translateY(-3px); }
    .card.selected-mode { border-color: var(--accent) !important; box-shadow: 0 0 15px rgba(255, 68, 68, 0.3); }
    
    .card h3 { margin: 0; color: var(--accent); font-size: 1.35rem; font-weight: 800; }
    .card p { margin: 15px 0 20px 0; font-size: 0.95rem; color: var(--subtext); line-height: 1.5; flex-grow: 1; }
    
    .card-meta { display: flex; align-items: center; gap: 10px; }
    .ver-badge { font-size: 0.75rem; color: #888; background: #222; padding: 4px 10px; border-radius: 8px; border: 1px solid #333; }
    .heart-icon { font-size: 1.2rem; color: #2a2a2a; transition: 0.2s; background: none; border: none; padding: 0; cursor: pointer; }
    .heart-icon.liked { color: var(--accent); }

    /* FAVS CONTROLS (SMALLER BUTTONS) */
    .fav-nav { display: flex; justify-content: center; gap: 8px; margin-bottom: 35px; position: relative; }
    .btn-ctrl { padding: 10px 14px; border-radius: 10px; font-weight: 700; cursor: pointer; border: 1px solid #333; background: #1a1a1a; color: white; font-size: 0.75rem; transition: 0.2s; }
    .btn-ctrl.active-red { background: var(--accent); border-color: var(--accent); }
    .btn-confirm-green { background: var(--green); color: black; border: none; display: none; position: absolute; right: 0; top: -45px; padding: 8px 15px; font-size: 0.8rem; }

    /* MOBILE */
    @media (max-width: 850px) {
        .sidebar { display: none; }
        .main { margin-left: 0; padding: 20px; width: 100%; padding-bottom: 90px; }
        .mobile-nav { display: flex; justify-content: space-around; background: var(--card); padding: 15px; margin: -20px -20px 25px -20px; border-bottom: 1px solid #222; }
        .search-wrap { position: static; transform: none; width: 100%; margin-bottom: 20px; }
        .search-wrap input { width: 100% !important; }
        .pc-warn { background: #1a1a1a; color: #555; border: 1px dashed #333; padding: 12px; border-radius: 12px; font-size: 0.8rem; flex: 1; margin-left: 10px; text-align: center; font-weight: 800; }
        .mobile-tg { position: fixed; bottom: 0; left: 0; right: 0; padding: 15px; background: rgba(10,10,10,0.95); z-index: 1000; }
        .btn-confirm-green { position: static; margin-top: 10px; width: 100%; }
    }
</style>
'''

SCRIPTS = '''
<script>
    let mode = ""; 
    let selectedList = [];

    function toggleLike(id, name) {
        let f = JSON.parse(localStorage.getItem('hk_favs') || '[]');
        let i = f.findIndex(x => x.id === id);
        if(i > -1) f.splice(i, 1); else f.push({id, name});
        localStorage.setItem('hk_favs', JSON.stringify(f));
        location.reload();
    }

    function setMode(m) {
        mode = (mode === m) ? "" : m;
        document.querySelectorAll('.btn-ctrl').forEach(b => b.classList.remove('active-red'));
        document.getElementById('btn-confirm-ubrat').style.display = (mode === 'del') ? 'block' : 'none';
        if(mode) event.target.classList.add('active-red');
        if(!mode) { selectedList = []; document.querySelectorAll('.card').forEach(c => c.classList.remove('selected-mode')); }
    }

    function handleCard(id) {
        if(mode === 'one') { toggleLike(id); }
        else if(mode === 'del') {
            const c = document.getElementById('card-'+id);
            if(selectedList.includes(id)) {
                selectedList = selectedList.filter(x => x !== id);
                c.classList.remove('selected-mode');
            } else {
                selectedList.push(id);
                c.classList.add('selected-mode');
            }
        } else { window.location.href = '/' + id; }
    }

    function deleteSelected() {
        let f = JSON.parse(localStorage.getItem('hk_favs') || '[]');
        f = f.filter(x => !selectedList.includes(x.id));
        localStorage.setItem('hk_favs', JSON.stringify(f));
        location.reload();
    }

    function filter() {
        let v = document.getElementById('sInp').value.toLowerCase();
        document.querySelectorAll('.card').forEach(c => {
            c.style.display = c.innerText.toLowerCase().includes(v) ? "flex" : "none";
        });
    }
</script>
'''

CHEATS = {
    'wurst': {'n': 'Wurst Client', 'd': 'Классика для выживания. Удобный интерфейс и проверенные временем функции.', 'v': '1.21.11'},
    'meteor': {'n': 'Meteor Client', 'd': 'Самый мощный софт для PVP и анархии. Постоянные обновления.', 'v': '1.21.11'}
}

@app.route('/')
def home():
    cards = "".join([f'<div class="card" onclick="handleCard(\'{k}\')"><h3>{v["n"]}</h3><p>{v["d"]}</p><div class="card-meta"><span class="ver-badge">{v["v"]}</span></div></div>' for k,v in CHEATS.items()])
    return render_template_string(f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>HK - Главная</title><link rel="icon" type="image/png" href="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png">{STYLE}</head><body>
        <div class="sidebar"><div class="logo-area"><img src="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png"></div><a href="/" class="nav-item active">Главная</a><a href="/favs" class="nav-item">Понравившееся</a><div class="sidebar-bottom"><a href="https://t.me/hellokilaura" class="btn-tg">Telegram</a></div></div>
        <div class="main"><div class="mobile-nav"><a href="/" class="nav-item active">Главная</a><a href="/favs" class="nav-item">Понравившееся</a></div>
        <div class="header-home"><h1>Все читы</h1><div class="search-wrap"><input type="text" id="sInp" onkeyup="filter()" placeholder="Поиск читов..."></div></div>
        <div class="grid">{cards}</div></div><div class="mobile-tg"><a href="https://t.me/hellokilaura" class="btn-tg" style="display:block;">Telegram</a></div>{SCRIPTS}</body></html>''')

@app.route('/<name>')
def cheat_p(name):
    i = CHEATS.get(name)
    if not i: return "404", 404
    return render_template_string(f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>{i['n']}</title><link rel="icon" type="image/png" href="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png">{STYLE}</head><body>
        <div class="sidebar"><div class="logo-area"><img src="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png"></div><a href="/" class="nav-item">Главная</a><a href="/favs" class="nav-item">Понравившееся</a><div class="sidebar-bottom"><button class="btn-tg" style="background:var(--green);color:black;margin-bottom:10px;">Скачать .jar</button><a href="https://t.me/hellokilaura" class="btn-tg">Telegram</a></div></div>
        <div class="main">
            <div style="display:flex;align-items:center;"><a href="/" style="color:var(--accent);text-decoration:none;font-weight:800;">← НАЗАД</a><div class="pc-warn" id="pw" style="display:none;">ТОЛЬКО ДЛЯ ПК</div><button class="heart-icon" id="h" onclick="toggleLike('{name}')" style="font-size:2.5rem;margin-left:auto;">❤</button></div>
            <div style="margin-top:20px;"><h1>{i['n']} <span class="ver-badge">{i['v']}</span></h1><p style="color:var(--subtext);max-width:600px;">{i['d']}</p></div>
        </div><div class="mobile-tg"><a href="https://t.me/hellokilaura" class="btn-tg" style="display:block;">Telegram</a></div>
        <script>if(window.innerWidth < 850) document.getElementById('pw').style.display='block';
        let f = JSON.parse(localStorage.getItem('hk_favs')||'[]'); if(f.some(x=>x.id==='{name}')) document.getElementById('h').classList.add('liked');</script>{SCRIPTS}</body></html>''')

@app.route('/favs')
def favorites():
    return render_template_string(f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>HK - Избранное</title><link rel="icon" type="image/png" href="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png">{STYLE}</head><body>
        <div class="sidebar"><div class="logo-area"><img src="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png"></div><a href="/" class="nav-item">Главная</a><a href="/favs" class="nav-item active">Понравившееся</a></div>
        <div class="main"><div class="mobile-nav"><a href="/" class="nav-item">Главная</a><a href="/favs" class="nav-item active">Понравившееся</a></div>
        <h1 style="text-align:center;margin-bottom:30px;">Избранное</h1>
        <div class="fav-nav">
            <button class="btn-ctrl" onclick="localStorage.setItem('hk_favs','[]');location.reload()">Удалить всё</button>
            <button class="btn-ctrl" onclick="setMode('del')">Удалить выбранное</button>
            <button class="btn-ctrl" onclick="setMode('one')">Удалить одно</button>
            <button class="btn-ctrl btn-confirm-green" id="btn-confirm-ubrat" onclick="deleteSelected()">Убрать выбранное</button>
        </div>
        <div id="fl" class="grid"></div></div><div class="mobile-tg"><a href="https://t.me/hellokilaura" class="btn-tg" style="display:block;">Telegram</a></div>
        <script>let f = JSON.parse(localStorage.getItem('hk_favs')||'[]'); let grid = document.getElementById('fl'); const d = {CHEATS};
        if(!f.length) grid.innerHTML = '<div style="text-align:center;width:100%;margin-top:100px;color:var(--subtext);">Пусто...</div>';
        else f.forEach(x => {{ let i = d[x.id] || {{n:x.name, d:'...', v:''}};
        grid.innerHTML += `<div class="card" id="card-${{x.id}}" onclick="handleCard('${{x.id}}')"><h3>${{i.n}}</h3><p>${{i.d}}</p><div class="card-meta"><span class="ver-badge">${{i.v}}</span><button class="heart-icon liked" style="margin-left:auto;">❤</button></div></div>`; }});</script>{SCRIPTS}</body></html>''')
