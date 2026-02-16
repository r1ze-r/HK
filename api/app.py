from flask import Flask, render_template_string

app = Flask(__name__)

# Тот самый жирный и красивый конфиг
STYLE = '''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    :root { --bg: #0a0a0a; --card: #161616; --accent: #ff4444; --green: #2ecc71; --tg: #24A1DE; --text: #ffffff; --subtext: #a1a1a1; --modal-bg: rgba(0,0,0,0.95); }
    
    body { background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; margin: 0; display: flex; min-height: 100vh; overflow-x: hidden; }
    
    /* SIDEBAR ПК */
    .sidebar { width: 260px; background: var(--card); height: 100vh; padding: 30px 20px; box-sizing: border-box; display: flex; flex-direction: column; border-right: 1px solid #222; position: fixed; z-index: 100; }
    .logo-area { text-align: center; margin-bottom: 40px; }
    .logo-area img { width: 100px; height: 100px; border-radius: 22px; filter: drop-shadow(0 0 10px var(--accent)); transition: 0.3s; }
    
    .nav-group { display: flex; flex-direction: column; gap: 8px; }
    .nav-item { padding: 14px 18px; border-radius: 12px; cursor: pointer; color: var(--subtext); transition: 0.3s; text-decoration: none; font-weight: 600; font-size: 0.95rem; }
    .nav-item:hover, .nav-item.active { background: #222; color: white; transform: translateX(5px); }
    
    .sidebar-bottom { margin-top: auto; display: flex; flex-direction: column; gap: 12px; }
    .btn-tg { background: var(--tg); color: white; padding: 14px; border-radius: 12px; text-decoration: none; font-weight: 800; text-align: center; transition: 0.3s; border: none; cursor: pointer; }
    .btn-dl-sidebar { background: var(--green); color: black; padding: 14px; border-radius: 12px; text-decoration: none; font-weight: 800; text-align: center; display: none; cursor: pointer; border: none; }

    .main { flex: 1; padding: 30px 50px; margin-left: 260px; width: calc(100% - 260px); position: relative; }

    /* HEADER & SEARCH */
    .header-home { display: flex; align-items: center; margin-bottom: 50px; width: 100%; position: relative; }
    .search-wrap { position: absolute; left: 45%; transform: translateX(-50%); }
    .search-wrap input { width: 240px; background: #1a1a1a; border: 1px solid #333; padding: 12px 20px; border-radius: 14px; color: white; outline: none; transition: 0.3s; }
    .search-wrap input:focus { border-color: var(--accent); width: 280px; box-shadow: 0 0 15px rgba(255, 68, 68, 0.2); }

    /* GRID & CARDS */
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 25px; }
    .card { background: var(--card); border-radius: 20px; border: 1px solid #222; padding: 25px; transition: 0.3s; cursor: pointer; position: relative; display: flex; flex-direction: column; }
    .card:hover { border-color: #444; transform: translateY(-5px); }
    .card.selected-mode { border-color: var(--accent) !important; box-shadow: 0 0 20px rgba(255, 68, 68, 0.3); }
    
    .card h3 { margin: 0; color: var(--accent); font-size: 1.4rem; font-weight: 800; }
    .card p { margin: 15px 0 20px 0; font-size: 0.95rem; color: var(--subtext); line-height: 1.6; min-height: 45px; }
    
    .card-meta { display: flex; align-items: center; gap: 12px; margin-top: auto; }
    .ver-badge { font-size: 0.75rem; color: #888; background: #222; padding: 4px 10px; border-radius: 8px; border: 1px solid #333; font-weight: 600; }
    .heart-icon { font-size: 1.2rem; color: #2a2a2a; transition: 0.3s; cursor: pointer; background: none; border: none; padding: 0; }
    .heart-icon.liked { color: var(--accent); filter: drop-shadow(0 0 5px var(--accent)); }

    /* FAVS CONTROLS */
    .fav-nav { display: flex; justify-content: center; gap: 10px; margin-bottom: 40px; flex-wrap: nowrap; overflow-x: auto; }
    .btn-ctrl { padding: 12px 18px; border-radius: 12px; font-weight: 800; cursor: pointer; border: 1px solid #333; background: #1a1a1a; color: white; transition: 0.2s; font-size: 0.85rem; flex: 1; text-align: center; white-space: nowrap; }
    .btn-ctrl.active-red { background: var(--accent); border-color: var(--accent); }
    .btn-confirm-green { background: var(--green); color: black; border: none; display: none; }

    /* MOBILE DESIGN */
    @media (max-width: 850px) {
        .sidebar { display: none; }
        .main { margin-left: 0; padding: 20px; width: 100%; padding-bottom: 100px; }
        .mobile-top-bar { display: flex; justify-content: space-around; background: var(--card); padding: 15px; margin: -20px -20px 25px -20px; border-bottom: 1px solid #222; position: sticky; top: 0; z-index: 1000; }
        .search-wrap { position: static; transform: none; width: 100%; margin-bottom: 25px; }
        .search-wrap input { width: 100% !important; }
        .pc-only-box { background: #1a1a1a; color: #666; border: 2px dashed #333; padding: 12px; border-radius: 12px; font-size: 0.85rem; font-weight: 800; text-align: center; flex: 1; margin-left: 15px; }
        .mobile-footer-tg { position: fixed; bottom: 0; left: 0; right: 0; padding: 20px; background: linear-gradient(transparent, var(--bg)); z-index: 1000; }
    }

    .modal { display: none; position: fixed; z-index: 2000; left: 0; top: 0; width: 100%; height: 100%; background: var(--modal-bg); align-items: center; justify-content: center; backdrop-filter: blur(5px); }
    .modal-box { background: var(--card); padding: 40px; border-radius: 25px; border: 1px solid #333; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.8); }
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
        let v = document.getElementById('searchInp').value.toLowerCase();
        document.querySelectorAll('.card').forEach(c => {
            let t = c.querySelector('h3').innerText.toLowerCase();
            c.style.display = t.includes(v) ? "flex" : "none";
        });
    }
</script>
'''

CHEATS = {
    'wurst': {'n': 'Wurst Client', 'd': 'Классика Minecraft. Самый удобный клиент для выживания и грифа.', 'v': '1.21.11', 'f': 'https://raw.githubusercontent.com/r1ze-r/HK/main/Wurst-Client1.21.11-hk.jar'},
    'meteor': {'n': 'Meteor Client', 'd': 'Популярный чит для PVP и анархии. Постоянные обновления и мощные функции.', 'v': '1.21.11', 'f': 'https://raw.githubusercontent.com/r1ze-r/HK/main/meteor-client-1.21.11-hk.jar'}
}

@app.route('/')
def home():
    cards = "".join([f'<div class="card" onclick="handleCard(\'{k}\')"><h3>{v["n"]}</h3><p>{v["d"]}</p><div class="card-meta"><span class="ver-badge">{v["v"]}</span></div></div>' for k,v in CHEATS.items()])
    return render_template_string(f'''
        <!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>HK - Главная</title><link rel="icon" type="image/png" href="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png">{STYLE}</head><body>
        <div class="sidebar"><div class="logo-area"><img src="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png"></div><div class="nav-group"><a href="/" class="nav-item active">Главная</a><a href="/favs" class="nav-item">Понравившееся</a></div><div class="sidebar-bottom"><a href="https://t.me/hellokilaura" class="btn-tg">Telegram</a></div></div>
        <div class="main"><div class="mobile-top-bar"><a href="/" class="nav-item active">Главная</a><a href="/favs" class="nav-item">Понравившееся</a></div>
        <div class="header-home"><h1>Все читы</h1><div class="search-wrap"><input type="text" id="searchInp" onkeyup="filter()" placeholder="Поиск читов..."></div></div>
        <div class="grid">{cards}</div></div><div class="mobile-footer-tg"><a href="https://t.me/hellokilaura" class="btn-tg" style="display:block;">Наш Telegram</a></div>{SCRIPTS}</body></html>''')

@app.route('/<name>')
def cheat_page(name):
    i = CHEATS.get(name)
    if not i: return "404", 404
    return render_template_string(f'''
        <!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{i['n']}</title><link rel="icon" type="image/png" href="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png">{STYLE}</head><body>
        <div class="sidebar"><div class="logo-area"><img src="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png"></div><div class="nav-group"><a href="/" class="nav-item">Главная</a><a href="/favs" class="nav-item">Понравившееся</a></div><div class="sidebar-bottom"><button onclick="forceDownload('{i['f']}', '{name.capitalize()}_HK.jar')" class="btn-dl-sidebar" style="display:block;">Скачать .jar</button><a href="https://t.me/hellokilaura" class="btn-tg">Telegram</a></div></div>
        <div class="main">
            <div style="display:flex; align-items:center;">
                <a href="/" style="color:var(--accent); text-decoration:none; font-weight:800;">← НАЗАД</a>
                <div class="pc-only-box" id="pcw" style="display:none;">СКАЧАТЬ МОЖНО ТОЛЬКО НА ПК</div>
                <button class="heart-icon" id="heartMain" onclick="toggleLike('{name}')" style="font-size:3rem; margin-left:auto;">❤</button>
            </div>
            <h1 style="margin-top:40px; font-size:3rem;">{i['n']} <span class="ver-badge" style="font-size:1rem;">{i['v']}</span></h1>
            <p style="color:var(--subtext); max-width:700px; font-size:1.2rem;">{i['d']}</p>
        </div>
        <div class="mobile-footer-tg"><a href="https://t.me/hellokilaura" class="btn-tg" style="display:block;">Наш Telegram</a></div>
        <script>if(window.innerWidth < 850) document.getElementById('pcw').style.display = 'block';
        let favs = JSON.parse(localStorage.getItem('hk_favs') || '[]');
        if(favs.some(x => x.id === '{name}')) document.getElementById('heartMain').classList.add('liked');</script>{SCRIPTS}</body></html>''')

@app.route('/favs')
def favs():
    return render_template_string(f'''
        <!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Избранное</title><link rel="icon" type="image/png" href="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png">{STYLE}</head><body>
        <div class="sidebar"><div class="logo-area"><img src="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png"></div><div class="nav-group"><a href="/" class="nav-item">Главная</a><a href="/favs" class="nav-item active">Понравившееся</a></div></div>
        <div class="main"><div class="mobile-top-bar"><a href="/" class="nav-item">Главная</a><a href="/favs" class="nav-item active">Понравившееся</a></div>
            <h1 style="text-align:center; margin-bottom:30px;">Понравившееся</h1>
            <div class="fav-nav">
                <button class="btn-ctrl" onclick="document.getElementById('confirmAll').style.display='flex'">Удалить всё</button>
                <button class="btn-ctrl" onclick="setMode('del')">Удалить выбранное</button>
                <button class="btn-ctrl" onclick="setMode('one')">Удалить одно</button>
                <button class="btn-ctrl btn-confirm-green" id="btn-confirm-ubrat" onclick="deleteSelected()">Убрать выбранное</button>
            </div>
            <div id="favList" class="grid"></div>
            <div id="confirmAll" class="modal"><div class="modal-box"><h3>Вы подтверждаете удалить всё?</h3><div style="display:flex;gap:15px;justify-content:center;margin-top:20px;">
                <button onclick="localStorage.setItem('hk_favs','[]');location.reload()" style="background:var(--accent);color:white;border:none;padding:12px 30px;border-radius:12px;font-weight:800;cursor:pointer;">ДА</button>
                <button onclick="document.getElementById('confirmAll').style.display='none'" style="background:none;border:1px solid #444;color:white;padding:12px 30px;border-radius:12px;font-weight:800;cursor:pointer;">НЕТ</button>
            </div></div></div>
        </div>
        <div class="mobile-footer-tg"><a href="https://t.me/hellokilaura" class="btn-tg" style="display:block;">Наш Telegram</a></div>
        <script>
            let f = JSON.parse(localStorage.getItem('hk_favs') || '[]');
            let l = document.getElementById('favList');
            const d = {CHEATS};
            if(!f.length) l.innerHTML = '<div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);color:var(--subtext);font-size:1.5rem;">Тут пока пусто.</div>';
            else f.forEach(x => {{
                let info = d[x.id] || {{n:x.name, d:'Просмотр...', v:''}};
                l.innerHTML += `<div class="card" id="card-${{x.id}}" onclick="handleCard('${{x.id}}')"><h3>${{info.n}}</h3><p>${{info.d}}</p><div class="card-meta"><span class="ver-badge">${{info.v}}</span><button class="heart-icon liked" style="margin-left:auto;">❤</button></div></div>`;
            }});
        </script>{SCRIPTS}</body></html>''')
