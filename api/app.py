from flask import Flask, render_template_string

app = Flask(__name__)

STYLE = '''
<style>
    :root { --bg: #0a0a0a; --card: #161616; --accent: #ff4444; --green: #2ecc71; --tg: #24A1DE; --text: #ffffff; --subtext: #a1a1a1; --modal-bg: rgba(0,0,0,0.9); }
    body { background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; margin: 0; display: flex; min-height: 100vh; }
    
    /* САЙДБАР */
    .sidebar { width: 240px; background: var(--card); height: 100vh; padding: 25px 15px; box-sizing: border-box; display: flex; flex-direction: column; border-right: 1px solid #222; position: fixed; z-index: 100; }
    .logo-sidebar { text-align: center; margin-bottom: 30px; }
    .logo-sidebar img { width: 100px; height: 100px; border-radius: 15px; filter: drop-shadow(0 0 5px var(--accent)); }
    .nav-item { padding: 12px 15px; border-radius: 8px; cursor: pointer; color: var(--subtext); transition: 0.2s; text-decoration: none; margin-bottom: 5px; font-weight: 500; display: block; }
    .nav-item:hover, .nav-item.active { background: #222; color: white; }
    .sidebar-bottom { margin-top: auto; }
    .btn-tg { background: var(--tg); color: white; padding: 12px; border-radius: 8px; text-decoration: none; font-weight: bold; text-align: center; display: block; }
    .btn-dl-sidebar { background: var(--green); color: black; padding: 12px; border-radius: 8px; text-decoration: none; font-weight: bold; text-align: center; display: none; margin-bottom: 10px; cursor: pointer; border: none; width: 100%; }

    .main { flex: 1; padding: 20px 40px; margin-left: 240px; width: calc(100% - 240px); } 

    /* ШАПКА */
    .header-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 40px; }
    .search-box { flex: 1; display: flex; justify-content: center; margin: 0 20px; }
    .search-box input { width: 280px; background: var(--card); border: 1px solid #333; padding: 10px 15px; border-radius: 10px; color: white; outline: none; }
    .search-box input:focus { border-color: var(--accent); }

    .ver-tag { font-size: 0.75rem; color: #777; background: #222; padding: 3px 10px; border-radius: 6px; display: inline-block; margin-top: 10px; border: 1px solid #333; }

    /* ИЗБРАННОЕ */
    .fav-header { text-align: center; margin-bottom: 30px; }
    .fav-btns { display: flex; justify-content: center; gap: 10px; margin-bottom: 20px; }
    .empty-msg { text-align: center; color: var(--subtext); margin-top: 50px; font-size: 1.1rem; width: 100%; }
    .btn-action { padding: 10px 20px; border-radius: 8px; cursor: pointer; font-weight: bold; border: 1px solid #333; background: #222; color: white; }
    .btn-action.active-red { background: var(--accent); border-color: var(--accent); }
    .btn-ubrat { background: var(--green); color: black; display: none; }

    /* КАРТОЧКИ */
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
    .card { background: var(--card); border-radius: 15px; border: 1px solid #222; padding: 20px; position: relative; cursor: pointer; transition: 0.2s; }
    .card.sel-mode { border-color: var(--accent); }
    .heart-btn { position: absolute; top: 15px; right: 15px; font-size: 2.2rem; background: none; border: none; color: #333; cursor: pointer; padding: 0; line-height: 1; }
    .heart-btn.liked { color: var(--accent); }

    /* МОБИЛКИ */
    @media (max-width: 850px) {
        .sidebar { display: none; }
        .main { margin-left: 0; padding: 15px; width: 100%; padding-bottom: 80px; }
        .header-row { flex-direction: column; align-items: flex-start; gap: 15px; }
        .search-box { width: 100%; margin: 0; }
        .search-box input { width: 100%; }
        .mobile-only-tg { position: fixed; bottom: 20px; left: 15px; right: 15px; z-index: 1000; }
        .pc-only-warning { display: inline-block; padding: 8px 12px; border: 1px dashed #555; border-radius: 8px; color: #888; font-size: 0.8rem; margin-left: 10px; }
        .heart-btn { display: none; }
    }

    .modal { display: none; position: fixed; z-index: 1000; left:0; top:0; width:100%; height:100%; background: var(--modal-bg); align-items:center; justify-content:center; }
    .modal-box { background: var(--card); padding: 30px; border-radius: 15px; text-align: center; border: 1px solid #333; }
</style>
'''

SCRIPTS = '''
<script>
    let mode = ''; // 'selected' or 'one'

    function toggleLike(id, name) {
        let favs = JSON.parse(localStorage.getItem('hk_favs') || '[]');
        const idx = favs.findIndex(i => i.id === id);
        if (idx > -1) favs.splice(idx, 1);
        else favs.push({id, name});
        localStorage.setItem('hk_favs', JSON.stringify(favs));
        location.reload();
    }

    function setMode(newMode) {
        if(mode === newMode) {
            mode = '';
            document.getElementById('btn-ubrat').style.display = 'none';
        } else {
            mode = newMode;
            if(mode === 'selected') document.getElementById('btn-ubrat').style.display = 'block';
        }
        document.querySelectorAll('.btn-action').forEach(b => b.classList.remove('active-red'));
        if(mode) event.target.classList.add('active-red');
    }

    function handleCard(id) {
        if (mode === 'one') {
            toggleLike(id);
        } else if (mode === 'selected') {
            document.getElementById('card-'+id).classList.toggle('sel-mode');
        } else {
            window.location.href = '/' + id;
        }
    }

    async function forceDownload(url, filename) {
        const response = await fetch(url);
        const blob = await response.blob();
        const link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = filename;
        link.click();
    }
</script>
'''

CHEATS_DATA = {
    'wurst': {'title': 'Wurst Client', 'desc': 'Удобный клиент для выживания. Классика.', 'file': 'https://raw.githubusercontent.com/r1ze-r/HK/main/Wurst-Client1.21.11-hk.jar', 'ver': '1.21.11'},
    'meteor': {'title': 'Meteor Client', 'desc': 'Популярный чит для PVP и анархии. Много настроек.', 'file': 'https://raw.githubusercontent.com/r1ze-r/HK/main/meteor-client-1.21.11-hk.jar', 'ver': '1.21.11'}
}

@app.route('/')
def home():
    cards = "".join([f'<div class="card" onclick="window.location.href=\'/{id}\'"><h3>{info["title"]}</h3><p>{info["desc"]}</p><span class="ver-tag">{info["ver"]}</span></div>' for id, info in CHEATS_DATA.items()])
    return render_template_string(f'''
        <!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>HK</title>{STYLE}</head>
        <body>
            <div class="sidebar"><div class="logo-sidebar"><img src="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png"></div><a href="/" class="nav-item active">Главная</a><a href="/favs" class="nav-item">Понравившееся</a><div class="sidebar-bottom"><a href="https://t.me/hellokilaura" class="btn-tg">Наш Telegram</a></div></div>
            <div class="main">
                <div class="header-row"><h1>Все читы</h1><div class="search-box"><input type="text" placeholder="Поиск читов..."></div><div style="width:100px;"></div></div>
                <div class="grid">{cards}</div>
            </div>
            <div class="mobile-only-tg"><a href="https://t.me/hellokilaura" class="btn-tg">Наш Telegram</a></div>
        {SCRIPTS}</body></html>''')

@app.route('/<name>')
def cheat_page(name):
    info = CHEATS_DATA.get(name)
    if not info: return "404", 404
    return render_template_string(f'''
        <!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>HK - {info['title']}</title>{STYLE}</head>
        <body>
            <div class="sidebar"><div class="logo-sidebar"><img src="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png"></div><a href="/" class="nav-item">Главная</a><a href="/favs" class="nav-item">Понравившееся</a><div class="sidebar-bottom"><button onclick="forceDownload('{info['file']}', '{name.capitalize()}_{info['ver']}_HK.jar')" class="btn-dl-sidebar" style="display:block;">Скачать .jar</button><a href="https://t.me/hellokilaura" class="btn-tg">Наш Telegram</a></div></div>
            <div class="main">
                <div style="display:flex; align-items:center;">
                    <a href="/" style="color:var(--accent); text-decoration:none; font-weight:bold;">← Назад</a>
                    <span class="pc-only-warning" style="display:none;">Скачать можно только на ПК</span>
                    <button class="heart-btn" id="h-{name}" onclick="toggleLike('{name}')">❤</button>
                </div>
                <h1 style="margin-top:30px;">{info['title']}</h1>
                <p style="color:var(--subtext);">{info['desc']}</p>
                <span class="ver-tag">{info['ver']}</span>
            </div>
            <div class="mobile-only-tg"><a href="https://t.me/hellokilaura" class="btn-tg">Наш Telegram</a></div>
            <script>
                if(window.innerWidth < 850) document.querySelector('.pc-only-warning').style.display = 'inline-block';
                let favs = JSON.parse(localStorage.getItem('hk_favs') || '[]');
                if(favs.some(i => i.id === '{name}')) document.getElementById('h-{name}').classList.add('liked');
            </script>
        {SCRIPTS}</body></html>''')

@app.route('/favs')
def favs():
    return render_template_string(f'''
        <!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>HK - Избранное</title>{STYLE}</head>
        <body>
            <div class="sidebar"><div class="logo-sidebar"><img src="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png"></div><a href="/" class="nav-item">Главная</a><a href="/favs" class="nav-item active">Понравившееся</a><div class="sidebar-bottom"><a href="https://t.me/hellokilaura" class="btn-tg">Наш Telegram</a></div></div>
            <div class="main">
                <div class="fav-header">
                    <h1>Понравившееся</h1>
                    <div class="fav-btns">
                        <button class="btn-action" onclick="document.getElementById('m').style.display='flex'">Удалить всё</button>
                        <button class="btn-action" onclick="setMode('selected')">Удалить выбранное</button>
                        <button class="btn-action" onclick="setMode('one')">Удалить одно</button>
                        <button class="btn-action btn-ubrat" id="btn-ubrat" onclick="location.reload()">Убрать</button>
                    </div>
                </div>
                <div id="fl" class="grid"></div>
                <div id="m" class="modal"><div class="modal-box"><h3>Удалить всё?</h3><div style="display:flex;gap:10px;margin-top:20px;"><button onclick="localStorage.setItem('hk_favs','[]');location.reload()" style="background:var(--accent);color:white;border:none;padding:10px 20px;border-radius:8px;cursor:pointer;">Да</button><button onclick="document.getElementById('m').style.display='none'" style="background:none;color:white;border:1px solid #444;padding:10px 20px;border-radius:8px;cursor:pointer;">Нет</button></div></div></div>
            </div>
            <div class="mobile-only-tg"><a href="https://t.me/hellokilaura" class="btn-tg">Наш Telegram</a></div>
            <script>
                let f = JSON.parse(localStorage.getItem('hk_favs') || '[]');
                let l = document.getElementById('fl');
                if(!f.length) l.innerHTML = '<div class="empty-msg">Тут пока пусто.</div>';
                else f.forEach(i => {{
                    l.innerHTML += `<div class="card" id="card-${{i.id}}" onclick="handleCard('${{i.id}}')"><h3>${{i.name}}</h3><p>Нажми для перехода</p></div>`;
                }});
            </script>
        {SCRIPTS}</body></html>''')
