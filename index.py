api/ from flask import Flask, render_template_string

index = Flask(__name__) 

STYLE = '''
<style>
    :root { --bg: #0a0a0a; --card: #161616; --accent: #ff4444; --green: #2ecc71; --tg: #24A1DE; --text: #ffffff; --subtext: #a1a1a1; }
    body { background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; margin: 0; display: flex; min-height: 100vh; }
    
    .sidebar { width: 240px; background: var(--card); height: 100vh; padding: 25px 15px; box-sizing: border-box; display: flex; flex-direction: column; border-right: 1px solid #222; position: fixed; z-index: 100; }
    .logo-sidebar { text-align: center; margin-bottom: 30px; }
    .logo-sidebar img { width: 100px; height: 100px; border-radius: 15px; filter: drop-shadow(0 0 5px var(--accent)); }
    
    .nav-item { padding: 10px 15px; border-radius: 8px; cursor: pointer; color: var(--subtext); transition: 0.2s; text-decoration: none; margin-bottom: 5px; font-weight: 500; display: block; font-size: 0.9rem; }
    .nav-item:hover, .nav-item.active { background: #222; color: white; }
    
    .sidebar-bottom { margin-top: auto; display: flex; flex-direction: column; gap: 10px; }
    .btn-tg { background: var(--tg); color: white; padding: 12px; border-radius: 8px; text-decoration: none; font-weight: bold; text-align: center; font-size: 0.85rem; transition: 0.3s; }
    .btn-install { background: var(--green); color: black; padding: 12px; border: none; border-radius: 8px; font-weight: bold; text-align: center; font-size: 0.9rem; cursor: pointer; width: 100%; display: block; }
    .mobile-no-download { display: none; background: #222; color: var(--subtext); padding: 12px; border-radius: 8px; font-weight: bold; text-align: center; font-size: 0.75rem; border: 1px dashed #444; }

    .main { flex: 1; padding: 20px 40px; margin-left: 240px; } 

    /* ВЕРХНЯЯ ПАНЕЛЬ С ПОИСКОМ */
    .header-home { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; gap: 20px; }
    .search-box { flex: 1; max-width: 400px; position: relative; }
    .search-box input { width: 100%; background: var(--card); border: 1px solid #333; padding: 10px 15px; border-radius: 10px; color: white; outline: none; transition: 0.3s; }
    .search-box input:focus { border-color: var(--accent); box-shadow: 0 0 10px rgba(255, 68, 68, 0.2); }
    .mini-logo { width: 40px; height: 40px; border-radius: 8px; }

    /* ТОП-БАР НА СТРАНИЦЕ ЧИТА */
    .top-bar-cheat { display: flex; align-items: center; gap: 20px; margin-bottom: 25px; }
    .btn-back { color: var(--accent); text-decoration: none; font-weight: bold; font-size: 0.9rem; }
    .heart-btn { cursor: pointer; font-size: 1.8rem; color: #333; background: none; border: none; transition: 0.3s; padding: 0; line-height: 1; }
    .heart-btn.liked { color: var(--accent); filter: drop-shadow(0 0 5px var(--accent)); }

    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
    .card { background: var(--card); border-radius: 15px; border: 1px solid #222; padding: 20px; transition: 0.2s; text-decoration: none; color: inherit; display: flex; flex-direction: column; }
    .card:hover { border-color: var(--accent); transform: translateY(-3px); }
    .card h3 { margin: 0 0 8px 0; color: var(--accent); }
    .card p { margin: 0 0 15px 0; font-size: 0.9rem; color: var(--subtext); }

    @media (max-width: 850px) {
        body { flex-direction: column; }
        .sidebar { width: 100%; height: auto; position: relative; border-right: none; border-bottom: 1px solid #222; padding: 15px; }
        .logo-sidebar { display: none; }
        .main { margin-left: 0; padding: 20px; }
        .header-home { flex-direction: row; flex-wrap: wrap; }
        .grid { grid-template-columns: 1fr; }
        .btn-install { display: none !important; }
        .mobile-no-download { display: block; }
    }
</style>
'''

SCRIPTS = '''
<script>
    async function forceDownload(url, filename) {
        try {
            const response = await fetch(url);
            const blob = await response.blob();
            const link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = filename;
            document.body.appendChild(link); link.click(); document.body.removeChild(link);
        } catch (e) { window.location.href = url; }
    }

    function toggleLike(id, name) {
        let favs = JSON.parse(localStorage.getItem('hk_favs') || '[]');
        const idx = favs.findIndex(i => i.id === id);
        if (idx > -1) { favs.splice(idx, 1); document.getElementById('heart-'+id).classList.remove('liked'); }
        else { favs.push({id, name}); document.getElementById('heart-'+id).classList.add('liked'); }
        localStorage.setItem('hk_favs', JSON.stringify(favs));
    }

    function loadHeartState(id) {
        let favs = JSON.parse(localStorage.getItem('hk_favs') || '[]');
        if (favs.some(i => i.id === id)) document.getElementById('heart-'+id)?.classList.add('liked');
    }

    // ЖИВОЙ ПОИСК
    function filterCheats() {
        let input = document.getElementById('searchInput').value.toLowerCase();
        let cards = document.getElementsByClassName('card');
        for (let card of cards) {
            let name = card.querySelector('h3').innerText.toLowerCase();
            card.style.display = name.includes(input) ? "flex" : "none";
        }
    }
</script>
'''

def get_sidebar(active):
    return f'''
    <div class="sidebar">
        <div class="logo-sidebar"><img src="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png"></div>
        <a href="/" class="nav-item {'active' if active=='home' else ''}">Главная</a>
        <a href="/favs" class="nav-item {'active' if active=='favs' else ''}">Понравившееся</a>
        <div class="sidebar-bottom"><a href="https://t.me/hellokilaura" target="_blank" class="btn-tg">Наш Telegram</a></div>
    </div>'''

@app.route('/')
def home():
    return render_template_string(f'''
        <!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>HK - Главная</title>{STYLE}</head>
        <body>{get_sidebar('home')}<div class="main">
            <div class="header-home">
                <img src="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png" class="mini-logo">
                <div class="search-box"><input type="text" id="searchInput" onkeyup="filterCheats()" placeholder="Поиск читов..."></div>
            </div>
            <h1>Все читы</h1>
            <div class="grid" id="cheatGrid">
                <a href="/wurst" class="card"><h3>Wurst</h3><p>Удобный клиент для выживания.</p></a>
                <a href="/meteor" class="card"><h3>Meteor Client</h3><p>Для PVP и анархии.</p></a>
            </div>
        </div>{SCRIPTS}</body></html>''')

@app.route('/<name>')
def cheat_page(name):
    # Упрощенная логика для страниц читов
    cheats = {
        'wurst': {'title': 'Wurst Client', 'desc': 'Легендарная классика.', 'file': 'https://raw.githubusercontent.com/r1ze-r/HK/main/Wurst-Client1.21.11-hk.jar'},
        'meteor': {'title': 'Meteor Client', 'desc': 'Топовый софт для PVP.', 'file': 'https://raw.githubusercontent.com/r1ze-r/HK/main/meteor-client-1.21.11-hk.jar'}
    }
    info = cheats.get(name)
    if not info: return "404", 404
    
    return render_template_string(f'''
        <!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>HK - {info['title']}</title>{STYLE}</head>
        <body onload="loadHeartState('{name}')">{get_sidebar(name)}
        <div class="main">
            <div class="top-bar-cheat">
                <a href="/" class="btn-back">← Назад</a>
                <button id="heart-{name}" class="heart-btn" onclick="toggleLike('{name}', '{info['title']}')">❤</button>
            </div>
            <h1>{info['title']}</h1>
            <p style="color:var(--subtext);">{info['desc']}</p>
            <div style="margin-top:30px; max-width:300px;">
                <button onclick="forceDownload('{info['file']}', '{name}.jar')" class="btn-install">Скачать .jar</button>
                <div class="mobile-no-download">Скачать можно только с ПК</div>
            </div>
        </div>{SCRIPTS}</body></html>''')

@app.route('/favs')
def favs():
    return render_template_string(f'''
        <!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>HK - Избранное</title>{STYLE}</head>
        <body>{get_sidebar('favs')}<div class="main"><h1>Понравившееся</h1><div id="favs-list" class="grid"></div></div>
        {SCRIPTS}<script>
            let favs = JSON.parse(localStorage.getItem('hk_favs') || '[]');
            let list = document.getElementById('favs-list');
            if (favs.length === 0) list.innerHTML = '<p>Тут пока пусто.</p>';
            else favs.forEach(i => list.innerHTML += `<a href="/${{i.id}}" class="card"><h3>${{i.name}}</h3><p>Твой выбор.</p></a>`);
        </script></body></html>''') # push to deploy 
# push to deploy # push to deploy
# push to deploy # push to deploy
