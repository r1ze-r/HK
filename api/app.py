from flask import Flask, render_template_string

app = Flask(__name__)

STYLE = '''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    :root { --bg: #0a0a0a; --card: #161616; --accent: #ff4444; --green: #2ecc71; --tg: #24A1DE; --text: #ffffff; --subtext: #a1a1a1; --modal-bg: rgba(0,0,0,0.95); }
    
    body { background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; margin: 0; display: flex; min-height: 100vh; overflow-x: hidden; }
    
    /* SIDEBAR ПК */
    .sidebar { width: 250px; background: var(--card); height: 100vh; padding: 30px 20px; box-sizing: border-box; display: flex; flex-direction: column; border-right: 1px solid #222; position: fixed; z-index: 100; }
    .logo-area { text-align: center; margin-bottom: 40px; }
    .logo-area img { width: 90px; height: 90px; border-radius: 18px; filter: drop-shadow(0 0 5px var(--accent)); }
    
    .nav-item { padding: 14px 18px; border-radius: 12px; cursor: pointer; color: var(--subtext); transition: 0.3s; text-decoration: none; font-weight: 600; display: block; margin-bottom: 5px; }
    .nav-item:hover, .nav-item.active { background: #222; color: white; }
    
    .sidebar-bottom { margin-top: auto; display: flex; flex-direction: column; gap: 10px; }
    .btn-tg { background: var(--tg); color: white; padding: 14px; border-radius: 12px; text-decoration: none; font-weight: 800; text-align: center; font-size: 0.9rem; }
    .btn-dl-sidebar { background: var(--green); color: black; padding: 14px; border-radius: 12px; text-decoration: none; font-weight: 800; text-align: center; display: none; cursor: pointer; border: none; }

    .main { flex: 1; padding: 30px 50px; margin-left: 250px; width: calc(100% - 250px); box-sizing: border-box; position: relative; }

    /* HEADER & SEARCH */
    .header-home { display: flex; align-items: center; margin-bottom: 40px; position: relative; width: 100%; }
    .search-box { position: absolute; left: 45%; transform: translateX(-50%); }
    .search-box input { width: 250px; background: #1a1a1a; border: 1px solid #333; padding: 12px 18px; border-radius: 12px; color: white; outline: none; transition: 0.3s; }
    .search-box input:focus { border-color: var(--accent); box-shadow: 0 0 10px rgba(255, 68, 68, 0.2); }

    /* CARDS */
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
    .card { background: var(--card); border-radius: 18px; border: 1px solid #222; padding: 22px; transition: 0.3s; cursor: pointer; display: flex; flex-direction: column; position: relative; }
    .card:hover { border-color: #444; transform: translateY(-3px); }
    .card.selected-for-del { border-color: var(--accent) !important; }
    
    .card h3 { margin: 0; color: var(--accent); font-size: 1.3rem; font-weight: 800; }
    .card p { margin: 12px 0 18px 0; font-size: 0.9rem; color: var(--subtext); line-height: 1.5; }
    
    .card-footer { display: flex; align-items: center; gap: 10px; margin-top: auto; }
    .ver-badge { font-size: 0.7rem; color: #777; background: #111; padding: 3px 8px; border-radius: 6px; border: 1px solid #333; }
    .heart-mini { font-size: 1.1rem; color: #222; transition: 0.2s; cursor: pointer; }
    .heart-mini.liked { color: var(--accent); }

    /* FAVS CONTROLS */
    .fav-controls { display: flex; justify-content: center; gap: 10px; margin-bottom: 40px; width: 100%; }
    .btn-fav { padding: 12px 15px; border-radius: 10px; font-weight: 700; cursor: pointer; border: 1px solid #333; background: #1a1a1a; color: white; font-size: 0.8rem; flex: 1; text-align: center; }
    .btn-fav.active { background: var(--accent); border-color: var(--accent); }
    .btn-green { background: var(--green); color: black; border: none; display: none; }
    .empty-msg { position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); color: var(--subtext); font-size: 1.2rem; }

    /* MOBILE */
    @media (max-width: 850px) {
        .sidebar { display: none; }
        .main { margin-left: 0; padding: 15px; width: 100%; padding-bottom: 100px; }
        .mobile-nav { display: flex; justify-content: space-around; background: var(--card); padding: 15px; margin: -15px -15px 25px -15px; border-bottom: 1px solid #222; }
        .search-box { position: static; transform: none; width: 100%; margin-bottom: 20px; }
        .search-box input { width: 100%; }
        .pc-warn { background: #1a1a1a; color: #666; border: 2px dashed #444; padding: 10px; border-radius: 10px; font-size: 0.8rem; text-align: center; flex: 1; margin-left: 10px; font-weight: 800; }
        .mobile-footer-tg { position: fixed; bottom: 0; left: 0; right: 0; padding: 15px; background: rgba(10,10,10,0.9); z-index: 1000; }
    }

    .modal { display: none; position: fixed; z-index: 2000; left: 0; top: 0; width: 100%; height: 100%; background: var(--modal-bg); align-items: center; justify-content: center; }
    .modal-box { background: var(--card); padding: 30px; border-radius: 20px; border: 1px solid #333; text-align: center; width: 85%; }
</style>
'''

SCRIPTS = '''
<script>
    let mode = ""; 
    let selected = [];

    function toggleLike(id, name) {
        let f = JSON.parse(localStorage.getItem('hk_favs') || '[]');
        let i = f.findIndex(x => x.id === id);
        if(i > -1) f.splice(i, 1); else f.push({id, name});
        localStorage.setItem('hk_favs', JSON.stringify(f));
        location.reload();
    }

    function setMode(m) {
        mode = (mode === m) ? "" : m;
        document.querySelectorAll('.btn-fav').forEach(b => b.classList.remove('active'));
        document.getElementById('green-btn').style.display = (mode === 'del') ? 'block' : 'none';
        if(mode) event.target.classList.add('active');
        if(!mode) { selected = []; document.querySelectorAll('.card').forEach(c => c.classList.remove('selected-for-del')); }
    }

    function handleCard(id) {
        if(mode === 'one') toggleLike(id);
        else if(mode === 'del') {
            const c = document.getElementById('card-'+id);
            if(selected.includes(id)) {
                selected = selected.filter(x => x !== id);
                c.classList.remove('selected-for-del');
            } else {
                selected.push(id);
                c.classList.add('selected-for-del');
            }
        } else { window.location.href = '/' + id; }
    }

    function deleteSelected() {
        let f = JSON.parse(localStorage.getItem('hk_favs') || '[]');
        f = f.filter(x => !selected.includes(x.id));
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

DATA = {
    'wurst': {'n': 'Wurst Client', 'd': 'Классика для выживания. Удобный интерфейс и мощные функции.', 'v': '1.21.11'},
    'meteor': {'n': 'Meteor Client', 'd': 'Лучший выбор для PVP и анархии. Ждем новых обновлений!', 'v': '1.21.11'}
}

@app.route('/')
def home():
    cards = "".join([f'<div class="card" onclick="handleCard(\'{k}\')"><h3>{v["n"]}</h3><p>{v["d"]}</p><div class="card-footer"><span class="ver-badge">{v["v"]}</span></div></div>' for k,v in DATA.items()])
    return render_template_string(f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>HK</title>{STYLE}</head><body>
        <div class="sidebar"><div class="logo-area"><img src="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png"></div><a href="/" class="nav-item active">Главная</a><a href="/favs" class="nav-item">Понравившееся</a><div class="sidebar-bottom"><a href="https://t.me/hellokilaura" class="btn-tg">Telegram</a></div></div>
        <div class="main"><div class="mobile-nav"><a href="/" class="nav-item active">Главная</a><a href="/favs" class="nav-item">Понравившееся</a></div>
        <div class="header-home"><h1>Все читы</h1><div class="search-box"><input type="text" id="sInp" onkeyup="filter()" placeholder="Поиск читов..."></div></div>
        <div class="grid">{cards}</div></div><div class="mobile-footer-tg"><a href="https://t.me/hellokilaura" class="btn-tg" style="display:block;text-align:center;">Telegram</a></div>{SCRIPTS}</body></html>''')

@app.route('/<name>')
def cheat(name):
    i = DATA.get(name)
    if not i: return "404", 404
    return render_template_string(f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>{i['n']}</title>{STYLE}</head><body>
        <div class="sidebar"><div class="logo-area"><img src="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png"></div><a href="/" class="nav-item">Главная</a><a href="/favs" class="nav-item">Понравившееся</a><div class="sidebar-bottom"><button class="btn-dl-sidebar" style="display:block;">Скачать .jar</button><a href="https://t.me/hellokilaura" class="btn-tg">Telegram</a></div></div>
        <div class="main"><div style="display:flex;align-items:center;"><a href="/" style="color:var(--accent);text-decoration:none;font-weight:bold;">← НАЗАД</a><div class="pc-warn" id="pw" style="display:none;">СКАЧАТЬ МОЖНО ТОЛЬКО НА ПК</div><button class="heart-mini" id="h" onclick="toggleLike('{name}')" style="font-size:2.5rem;margin-left:auto;background:none;border:none;">❤</button></div>
        <div style="margin-top:20px;"><h1>{i['n']} <span class="ver-badge">{i['v']}</span></h1><p style="color:var(--subtext);max-width:600px;">{i['d']}</p></div></div>
        <script>if(window.innerWidth < 850) document.getElementById('pw').style.display='block';
        let f = JSON.parse(localStorage.getItem('hk_favs')||'[]'); if(f.some(x=>x.id==='{name}')) document.getElementById('h').classList.add('liked');</script>
        <div class="mobile-footer-tg"><a href="https://t.me/hellokilaura" class="btn-tg" style="display:block;text-align:center;">Telegram</a></div>{SCRIPTS}</body></html>''')

@app.route('/favs')
def favs():
    return render_template_string(f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Избранное</title>{STYLE}</head><body>
        <div class="sidebar"><div class="logo-area"><img src="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png"></div><a href="/" class="nav-item">Главная</a><a href="/favs" class="nav-item active">Понравившееся</a></div>
        <div class="main"><div class="mobile-nav"><a href="/" class="nav-item">Главная</a><a href="/favs" class="nav-item active">Понравившееся</a></div>
        <h1 style="text-align:center;margin-bottom:30px;">Понравившееся</h1>
        <div class="fav-controls"><button class="btn-fav" onclick="document.getElementById('m').style.display='flex'">Удалить всё</button><button class="btn-fav" onclick="setMode('del')">Удалить выбранное</button><button class="btn-fav" onclick="setMode('one')">Удалить одно</button><button class="btn-fav btn-green" id="green-btn" onclick="deleteSelected()">Убрать</button></div>
        <div id="fl" class="grid"></div><div id="m" class="modal"><div class="modal-box"><h3>Удалить всё?</h3><div style="display:flex;gap:10px;justify-content:center;margin-top:25px;"><button onclick="localStorage.setItem('hk_favs','[]');location.reload()" style="background:var(--accent);border:none;padding:10px 25px;border-radius:10px;color:white;font-weight:bold;">ДА</button><button onclick="document.getElementById('m').style.display='none'" style="background:none;border:1px solid #444;padding:10px 25px;border-radius:10px;color:white;">НЕТ</button></div></div></div></div>
        <script>let f = JSON.parse(localStorage.getItem('hk_favs')||'[]'); let l = document.getElementById('fl'); const d = {DATA};
        if(!f.length) l.innerHTML = '<div class="empty-msg">Тут пока пусто.</div>';
        else f.forEach(x => {{ let i = d[x.id]; l.innerHTML += `<div class="card" id="card-${{x.id}}" onclick="handleCard('${{x.id}}')"><h3>${{i.n}}</h3><p>${{i.d}}</p><div class="card-footer"><span class="ver-badge">${{i.v}}</span><span class="heart-mini liked" style="margin-left:auto;">❤</span></div></div>`; }});</script>{SCRIPTS}</body></html>''')
