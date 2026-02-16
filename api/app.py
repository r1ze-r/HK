from flask import Flask, render_template_string

app = Flask(__name__)

STYLE = '''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    :root { --bg: #0a0a0a; --card: #161616; --accent: #ff4444; --green: #2ecc71; --tg: #24A1DE; --text: #ffffff; --subtext: #a1a1a1; }
    
    body { background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; margin: 0; min-height: 100vh; overflow-x: hidden; }
    
    /* ВЕРХНЕЕ МЕНЮ */
    .top-nav { display: flex; justify-content: center; gap: 20px; padding: 30px 0 10px 0; background: var(--bg); }
    .nav-link { padding: 12px 24px; border-radius: 12px; color: var(--subtext); text-decoration: none; font-weight: 800; font-size: 1.1rem; transition: 0.3s; background: #111; border: 1px solid #222; }
    .nav-link:hover, .nav-link.active { color: white; background: #222; border-color: #444; }

    /* КНОПКА ТГ СЛЕВА ВНИЗУ */
    .tg-fixed { position: fixed; left: 30px; bottom: 30px; z-index: 1000; }
    .btn-tg { background: var(--tg); color: white; padding: 15px 25px; border-radius: 14px; text-decoration: none; font-weight: 800; display: block; transition: 0.3s; box-shadow: 0 5px 15px rgba(36, 161, 222, 0.3); }
    .btn-tg:hover { transform: translateY(-3px); filter: brightness(1.1); }

    .container { max-width: 1200px; margin: 0 auto; padding: 20px 40px 100px 40px; }

    /* HEADER */
    .header-area { display: flex; flex-direction: column; align-items: center; margin-bottom: 50px; text-align: center; }
    .header-area h1 { font-size: 2.5rem; margin-bottom: 20px; }
    .search-bar { width: 300px; background: #1a1a1a; border: 1px solid #333; padding: 14px 20px; border-radius: 14px; color: white; outline: none; text-align: center; }

    /* КАРТОЧКИ */
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 30px; }
    .card { background: var(--card); border-radius: 22px; border: 1px solid #222; padding: 30px; transition: 0.3s; cursor: pointer; display: flex; flex-direction: column; position: relative; }
    .card:hover { border-color: #444; transform: translateY(-5px); }
    .card.selected { border-color: var(--accent) !important; box-shadow: 0 0 20px rgba(255, 68, 68, 0.3); }
    
    .card h3 { margin: 0; color: var(--accent); font-size: 1.5rem; font-weight: 800; }
    .card p { margin: 15px 0 25px 0; font-size: 1rem; color: var(--subtext); line-height: 1.6; }
    
    .card-footer { display: flex; align-items: center; gap: 12px; margin-top: auto; }
    .v-tag { font-size: 0.8rem; color: #888; background: #222; padding: 5px 12px; border-radius: 8px; border: 1px solid #333; font-weight: 600; }
    .heart-btn { font-size: 1.4rem; color: #2a2a2a; transition: 0.2s; background: none; border: none; padding: 0; cursor: pointer; margin-left: auto; }
    .heart-btn.liked { color: var(--accent); filter: drop-shadow(0 0 5px var(--accent)); }

    /* ИЗБРАННОЕ УПРАВЛЕНИЕ */
    .fav-actions { display: flex; justify-content: center; gap: 12px; margin-bottom: 40px; position: relative; }
    .btn-f { padding: 12px 20px; border-radius: 12px; font-weight: 800; cursor: pointer; border: 1px solid #333; background: #111; color: white; font-size: 0.85rem; }
    .btn-f.active { background: var(--accent); border-color: var(--accent); }
    .btn-save { background: var(--green); color: black; border: none; display: none; position: absolute; right: 0; top: -50px; }

    @media (max-width: 850px) {
        .container { padding: 15px; }
        .tg-fixed { left: 15px; bottom: 15px; right: 15px; }
        .btn-tg { text-align: center; }
        .nav-link { font-size: 0.9rem; padding: 10px 15px; }
        .search-bar { width: 100%; }
        .btn-save { position: static; margin-top: 10px; width: 100%; }
    }
</style>
'''

SCRIPTS = '''
<script>
    let mode = ""; let selected = [];
    function toggleLike(id, name) {
        let f = JSON.parse(localStorage.getItem('hk_favs') || '[]');
        let i = f.findIndex(x => x.id === id);
        if(i > -1) f.splice(i, 1); else f.push({id, name});
        localStorage.setItem('hk_favs', JSON.stringify(f));
        location.reload();
    }
    function setMode(m) {
        mode = (mode === m) ? "" : m;
        document.querySelectorAll('.btn-f').forEach(b => b.classList.remove('active'));
        document.getElementById('save-btn').style.display = (mode === 'del') ? 'block' : 'none';
        if(mode) event.target.classList.add('active');
    }
    function handleCard(id) {
        if(mode === 'one') toggleLike(id);
        else if(mode === 'del') {
            document.getElementById('card-'+id).classList.toggle('selected');
            if(selected.includes(id)) selected = selected.filter(x => x !== id);
            else selected.push(id);
        } else window.location.href = '/' + id;
    }
    function deleteSelected() {
        let f = JSON.parse(localStorage.getItem('hk_favs') || '[]');
        f = f.filter(x => !selected.includes(x.id));
        localStorage.setItem('hk_favs', JSON.stringify(f));
        location.reload();
    }
</script>
'''

CHEATS = {
    'wurst': {'n': 'Wurst Client', 'd': 'Классика Minecraft. Лучший выбор для выживания и простого грифа.', 'v': '1.21.11'},
    'meteor': {'n': 'Meteor Client', 'd': 'Мощнейший софт для PVP и анархии. Куча настроек и модулей.', 'v': '1.21.11'}
}

@app.route('/')
def home():
    cards = "".join([f'<div class="card" onclick="handleCard(\'{k}\')"><h3>{v["n"]}</h3><p>{v["d"]}</p><div class="card-footer"><span class="v-tag">{v["v"]}</span></div></div>' for k,v in CHEATS.items()])
    return render_template_string(f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>HK - Главная</title><link rel="icon" type="image/png" href="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png">{STYLE}</head><body>
        <div class="top-nav"><a href="/" class="nav-link active">Главная</a><a href="/favs" class="nav-link">Понравившееся</a></div>
        <div class="tg-fixed"><a href="https://t.me/hellokilaura" class="btn-tg">Telegram</a></div>
        <div class="container">
            <div class="header-area"><h1>Все читы</h1><input type="text" class="search-bar" placeholder="Поиск..."></div>
            <div class="grid">{cards}</div>
        </div>{SCRIPTS}</body></html>''')

@app.route('/<name>')
def cheat_page(name):
    i = CHEATS.get(name)
    if not i: return "404", 404
    return render_template_string(f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>{i['n']}</title><link rel="icon" type="image/png" href="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png">{STYLE}</head><body>
        <div class="top-nav"><a href="/" class="nav-link">Главная</a><a href="/favs" class="nav-link">Понравившееся</a></div>
        <div class="tg-fixed"><a href="https://t.me/hellokilaura" class="btn-tg">Telegram</a></div>
        <div class="container">
            <div style="display:flex;align-items:center;margin-bottom:30px;"><a href="/" style="color:var(--accent);text-decoration:none;font-weight:800;font-size:1.2rem;">← НАЗАД</a><button class="heart-btn" id="h" onclick="toggleLike('{name}')" style="font-size:3rem;">❤</button></div>
            <h1 style="font-size:3.5rem;margin:0;">{i['n']} <span class="v-tag" style="font-size:1rem;">{i['v']}</span></h1>
            <p style="color:var(--subtext);font-size:1.2rem;max-width:800px;margin-top:20px;">{i['d']}</p>
            <button class="btn-tg" style="background:var(--green);color:black;margin-top:40px;display:inline-block;width:200px;text-align:center;">Скачать .jar</button>
        </div>
        <script>let f = JSON.parse(localStorage.getItem('hk_favs')||'[]'); if(f.some(x=>x.id==='{name}')) document.getElementById('h').classList.add('liked');</script>
        {SCRIPTS}</body></html>''')

@app.route('/favs')
def favs():
    return render_template_string(f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Избранное</title><link rel="icon" type="image/png" href="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png">{STYLE}</head><body>
        <div class="top-nav"><a href="/" class="nav-link">Главная</a><a href="/favs" class="nav-link active">Понравившееся</a></div>
        <div class="tg-fixed"><a href="https://t.me/hellokilaura" class="btn-tg">Telegram</a></div>
        <div class="container">
            <h1 style="text-align:center;margin-bottom:40px;">Понравившееся</h1>
            <div class="fav-actions">
                <button class="btn-f" onclick="localStorage.setItem('hk_favs','[]');location.reload()">Удалить всё</button>
                <button class="btn-f" onclick="setMode('del')">Удалить выбранное</button>
                <button class="btn-f" onclick="setMode('one')">Удалить одно</button>
                <button class="btn-f btn-save" id="save-btn" onclick="deleteSelected()">Убрать выбранное</button>
            </div>
            <div id="fl" class="grid"></div>
        </div>
        <script>let f = JSON.parse(localStorage.getItem('hk_favs')||'[]'); let g = document.getElementById('fl'); const d = {CHEATS};
        if(!f.length) g.innerHTML = '<div style="text-align:center;width:100%;font-size:1.5rem;color:#444;margin-top:50px;">Тут пока ничего нет...</div>';
        else f.forEach(x => {{ let i = d[x.id] || {{n:x.name, d:'...', v:''}};
        g.innerHTML += `<div class="card" id="card-${{x.id}}" onclick="handleCard('${{x.id}}')"><h3>${{i.n}}</h3><p>${{i.d}}</p><div class="card-footer"><span class="v-tag">${{i.v}}</span><button class="heart-btn liked">❤</button></div></div>`; }});</script>
        {SCRIPTS}</body></html>''')
