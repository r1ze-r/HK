from flask import Flask, render_template_string

app = Flask(__name__)

STYLE = '''
<style>
    :root { --bg: #0a0a0a; --card: #161616; --accent: #ff4444; --green: #2ecc71; --tg: #24A1DE; --text: #ffffff; --subtext: #a1a1a1; --modal-bg: rgba(0,0,0,0.9); }
    body { background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; margin: 0; display: flex; min-height: 100vh; overflow-x: hidden; }
    
    /* САЙДБАР ПК */
    .sidebar { width: 240px; background: var(--card); height: 100vh; padding: 25px 15px; box-sizing: border-box; display: flex; flex-direction: column; border-right: 1px solid #222; position: fixed; z-index: 100; }
    .logo-sidebar { text-align: center; margin-bottom: 30px; }
    .logo-sidebar img { width: 100px; height: 100px; border-radius: 15px; filter: drop-shadow(0 0 5px var(--accent)); }
    .nav-item { padding: 12px 15px; border-radius: 8px; cursor: pointer; color: var(--subtext); transition: 0.2s; text-decoration: none; margin-bottom: 5px; font-weight: 500; display: block; }
    .nav-item:hover, .nav-item.active { background: #222; color: white; }
    
    /* ТГ СПРАВА ВВЕРХУ (ПК) */
    .tg-top-right { position: fixed; top: 20px; right: 40px; z-index: 1001; }
    .btn-tg { background: var(--tg); color: white; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 0.9rem; transition: 0.3s; }

    .main { flex: 1; padding: 20px 40px; margin-left: 240px; width: calc(100% - 240px); box-sizing: border-box; }

    /* ХЕДЕР */
    .header-home { display: flex; align-items: center; justify-content: space-between; margin-bottom: 40px; width: 100%; position: relative; }
    .search-container { position: absolute; left: 50%; transform: translateX(-50%); width: 270px; }
    .search-container input { width: 100%; background: var(--card); border: 1px solid #333; padding: 10px 15px; border-radius: 10px; color: white; outline: none; transition: 0.3s; }
    .search-container input:focus { border-color: var(--accent); }

    /* КАРТОЧКИ */
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px; }
    .card { background: var(--card); border-radius: 15px; border: 1px solid #222; padding: 20px; transition: 0.2s; cursor: pointer; position: relative; display: flex; flex-direction: column; }
    .card:hover { border-color: #444; }
    .card.selected-for-delete { border-color: var(--accent) !important; box-shadow: 0 0 10px rgba(255, 68, 68, 0.4); }
    
    .card-head { display: flex; align-items: baseline; gap: 10px; }
    .card-head h3 { margin: 0; color: var(--accent); font-size: 1.25rem; }
    .ver-tag { font-size: 0.75rem; color: #666; background: #1a1a1a; padding: 2px 8px; border-radius: 4px; border: 1px solid #333; }

    /* СТРАНИЦА ЧИТА */
    .heart-btn { font-size: 2.8rem; background: none; border: none; color: #222; cursor: pointer; transition: 0.3s; padding: 0; line-height: 1; margin-left: auto; }
    .heart-btn.liked { color: var(--accent); filter: drop-shadow(0 0 5px var(--accent)); }
    .btn-dl-sidebar { background: var(--green); color: black; padding: 12px; border-radius: 8px; text-decoration: none; font-weight: bold; text-align: center; display: none; margin-top: auto; cursor: pointer; border: none; }

    /* ИЗБРАННОЕ */
    .fav-btns { display: flex; justify-content: center; gap: 12px; margin-bottom: 30px; }
    .btn-act { padding: 10px 18px; border-radius: 8px; font-weight: bold; cursor: pointer; border: 1px solid #333; background: #1a1a1a; color: white; transition: 0.2s; }
    .btn-act.active { background: var(--accent); border-color: var(--accent); }
    .btn-confirm-delete { background: var(--green); color: black; display: none; }
    .empty-box { display: flex; justify-content: center; align-items: center; min-height: 200px; width: 100%; color: var(--subtext); font-size: 1.2rem; }

    /* МОБИЛКА */
    @media (max-width: 850px) {
        .sidebar, .tg-top-right { display: none; }
        .main { margin-left: 0; padding: 15px; width: 100%; padding-bottom: 100px; }
        .header-home { flex-direction: column; align-items: flex-start; gap: 20px; }
        .search-container { position: static; transform: none; width: 100%; }
        .card { padding: 12px; min-height: auto; }
        .card p { margin: 5px 0 10px 0; font-size: 0.85rem; }
        .mobile-tg { position: fixed; bottom: 15px; left: 15px; right: 15px; z-index: 1000; }
        .pc-warning-btn { background: #1a1a1a; color: #666; border: 1px dashed #444; padding: 12px 20px; border-radius: 10px; font-size: 0.9rem; font-weight: bold; flex-grow: 1; text-align: center; }
        .fav-btns { flex-direction: column; width: 100%; }
        .btn-act { width: 100%; }
    }

    /* МОДАЛКА */
    .modal { display: none; position: fixed; z-index: 2000; left: 0; top: 0; width: 100%; height: 100%; background: var(--modal-bg); align-items: center; justify-content: center; }
    .modal-box { background: var(--card); padding: 30px; border-radius: 15px; border: 1px solid #333; text-align: center; width: 90%; max-width: 400px; }
</style>
'''

SCRIPTS = '''
<script>
    let mode = ""; // "selected" or "one"
    let toDelete = [];

    function toggleLike(id, name) {
        let favs = JSON.parse(localStorage.getItem('hk_favs') || '[]');
        const idx = favs.findIndex(i => i.id === id);
        if (idx > -1) favs.splice(idx, 1);
        else favs.push({id, name});
        localStorage.setItem('hk_favs', JSON.stringify(favs));
        location.reload();
    }

    function setMode(m) {
        mode = (mode === m) ? "" : m;
        document.querySelectorAll('.btn-act').forEach(b => b.classList.remove('active'));
        document.getElementById('btn-confirm').style.display = 'none';
        if(mode) event.target.classList.add('active');
        if(mode === 'selected') document.getElementById('btn-confirm').style.display = 'block';
        if(!mode) { toDelete = []; document.querySelectorAll('.card').forEach(c => c.classList.remove('selected-for-delete')); }
    }

    function handleCard(id) {
        if(mode === "one") { toggleLike(id); }
        else if(mode === "selected") {
            const card = document.getElementById('card-'+id);
            if(toDelete.includes(id)) {
                toDelete = toDelete.filter(i => i !== id);
                card.classList.remove('selected-for-delete');
            } else {
                toDelete.push(id);
                card.classList.add('selected-for-delete');
            }
        } else { window.location.href = "/" + id; }
    }

    function deleteSelected() {
        let favs = JSON.parse(localStorage.getItem('hk_favs') || '[]');
        favs = favs.filter(i => !toDelete.includes(i.id));
        localStorage.setItem('hk_favs', JSON.stringify(favs));
        location.reload();
    }

    function filterCheats() {
        let val = document.getElementById('searchInp').value.toLowerCase();
        document.querySelectorAll('.card').forEach(c => {
            let h = c.querySelector('h3').innerText.toLowerCase();
            c.style.display = h.includes(val) ? "flex" : "none";
        });
    }

    async function forceDownload(url, filename) {
        const r = await fetch(url);
        const b = await r.blob();
        const a = document.createElement('a');
        a.href = window.URL.createObjectURL(b);
        a.download = filename;
        a.click();
    }
</script>
'''

CHEATS_DATA = {
    'wurst': {'title': 'Wurst Client', 'desc': 'Классика для выживания. Удобный и простой.', 'file': 'https://raw.githubusercontent.com/r1ze-r/HK/main/Wurst-Client1.21.11-hk.jar', 'ver': '1.21.11'},
    'meteor': {'title': 'Meteor Client', 'desc': 'Популярный чит для PVP и анархии. Ждем "самый жесткий" софт!', 'file': 'https://raw.githubusercontent.com/r1ze-r/HK/main/meteor-client-1.21.11-hk.jar', 'ver': '1.21.11'}
}

@app.route('/')
def home():
    cards = "".join([f'<div class="card" onclick="handleCard(\'{id}\')"><div class="card-head"><h3>{info["title"]}</h3><span class="ver-tag">{info["ver"]}</span></div><p>{info["desc"]}</p></div>' for id, info in CHEATS_DATA.items()])
    return render_template_string(f'''
        <!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>HK</title>{STYLE}</head>
        <body>
            <div class="sidebar"><div class="logo-sidebar"><img src="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png"></div><a href="/" class="nav-item active">Главная</a><a href="/favs" class="nav-item">Понравившееся</a></div>
            <div class="tg-top-right"><a href="https://t.me/hellokilaura" class="btn-tg">Наш Telegram</a></div>
            <div class="main">
                <div class="header-home"><h1>Все читы</h1><div class="search-container"><input type="text" id="searchInp" onkeyup="filterCheats()" placeholder="Поиск читов..."></div></div>
                <div class="grid">{cards}</div>
            </div>
            <div class="mobile-tg"><a href="https://t.me/hellokilaura" class="btn-tg" style="display:block;text-align:center;">Наш Telegram</a></div>
        {SCRIPTS}</body></html>''')

@app.route('/<name>')
def cheat_page(name):
    info = CHEATS_DATA.get(name)
    if not info: return "404", 404
    return render_template_string(f'''
        <!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>HK - {info['title']}</title>{STYLE}</head>
        <body>
            <div class="sidebar"><div class="logo-sidebar"><img src="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png"></div><a href="/" class="nav-item">Главная</a><a href="/favs" class="nav-item">Понравившееся</a><button onclick="forceDownload('{info['file']}', '{name.capitalize()}_{info['ver']}_HK.jar')" class="btn-dl-sidebar" style="display:block;">Скачать .jar</button></div>
            <div class="tg-top-right"><a href="https://t.me/hellokilaura" class="btn-tg">Наш Telegram</a></div>
            <div class="main">
                <div style="display:flex; align-items:center; gap:20px;">
                    <a href="/" style="color:var(--accent); text-decoration:none; font-weight:bold; font-size:1.2rem;">← Назад</a>
                    <div class="pc-warning-btn" id="mob-warn" style="display:none;">Скачать можно только на ПК</div>
                    <button class="heart-btn" id="h-{name}" onclick="toggleLike('{name}')">❤</button>
                </div>
                <h1 style="margin-top:40px; display:flex; align-items:center; gap:15px;">{info['title']} <span class="ver-tag">{info['ver']}</span></h1>
                <p style="color:var(--subtext); max-width:600px; line-height:1.6; font-size:1.1rem;">{info['desc']}</p>
            </div>
            <div class="mobile-tg"><a href="https://t.me/hellokilaura" class="btn-tg" style="display:block;text-align:center;">Наш Telegram</a></div>
            <script>
                if(window.innerWidth < 850) document.getElementById('mob-warn').style.display = 'block';
                let favs = JSON.parse(localStorage.getItem('hk_favs') || '[]');
                if(favs.some(i => i.id === '{name}')) document.getElementById('h-{name}').classList.add('liked');
            </script>
        {SCRIPTS}</body></html>''')

@app.route('/favs')
def favs():
    return render_template_string(f'''
        <!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>HK - Избранное</title>{STYLE}</head>
        <body>
            <div class="sidebar"><div class="logo-sidebar"><img src="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png"></div><a href="/" class="nav-item">Главная</a><a href="/favs" class="nav-item active">Понравившееся</a></div>
            <div class="tg-top-right"><a href="https://t.me/hellokilaura" class="btn-tg">Наш Telegram</a></div>
            <div class="main">
                <h1 style="text-align:center;">Понравившееся</h1>
                <div class="fav-btns">
                    <button class="btn-act" onclick="document.getElementById('md').style.display='flex'">Удалить всё</button>
                    <button class="btn-act" onclick="setMode('selected')">Удалить выбранное</button>
                    <button class="btn-act" onclick="setMode('one')">Удалить одно</button>
                    <button class="btn-act btn-confirm-delete" id="btn-confirm" onclick="deleteSelected()">Убрать выбранное</button>
                </div>
                <div id="fl" class="grid"></div>
                <div id="md" class="modal"><div class="modal-box"><h3>Удалить всё?</h3><div style="display:flex;gap:15px;justify-content:center;margin-top:20px;"><button onclick="localStorage.setItem('hk_favs','[]');location.reload()" style="background:var(--accent);color:white;border:none;padding:12px 25px;border-radius:8px;font-weight:bold;">Да</button><button onclick="document.getElementById('md').style.display='none'" style="background:none;color:white;border:1px solid #444;padding:12px 25px;border-radius:8px;font-weight:bold;">Нет</button></div></div></div>
            </div>
            <div class="mobile-tg"><a href="https://t.me/hellokilaura" class="btn-tg" style="display:block;text-align:center;">Наш Telegram</a></div>
            <script>
                let fs = JSON.parse(localStorage.getItem('hk_favs') || '[]');
                let l = document.getElementById('fl');
                const data = {CHEATS_DATA};
                if(!fs.length) l.innerHTML = '<div class="empty-box">Тут пока пусто.</div>';
                else fs.forEach(i => {{
                    const info = data[i.id] || {{desc:'Перейти к читу', ver:''}};
                    l.innerHTML += `<div class="card" id="card-${{i.id}}" onclick="handleCard('${{i.id}}')"><div class="card-head"><h3>${{i.name}}</h3><span class="ver-tag">${{info.ver}}</span></div><p>${{info.desc}}</p></div>`;
                }});
            </script>
        {SCRIPTS}</body></html>''')
