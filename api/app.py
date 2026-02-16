from flask import Flask, render_template_string

app = Flask(__name__)

STYLE = '''
<style>
    :root { --bg: #0a0a0a; --card: #161616; --accent: #ff4444; --green: #2ecc71; --tg: #24A1DE; --text: #ffffff; --subtext: #a1a1a1; }
    body { background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; margin: 0; display: flex; min-height: 100vh; }
    
    .sidebar { width: 240px; background: var(--card); height: 100vh; padding: 25px 15px; box-sizing: border-box; display: flex; flex-direction: column; border-right: 1px solid #222; position: fixed; z-index: 100; transition: 0.3s; }
    .logo-sidebar { text-align: center; margin-bottom: 30px; }
    .logo-sidebar img { width: 100px; height: 100px; border-radius: 15px; filter: drop-shadow(0 0 5px var(--accent)); }
    
    .nav-item { padding: 12px 15px; border-radius: 8px; cursor: pointer; color: var(--subtext); transition: 0.2s; text-decoration: none; margin-bottom: 5px; font-weight: 500; display: block; font-size: 0.95rem; }
    .nav-item:hover, .nav-item.active { background: #222; color: white; }
    
    .sidebar-bottom { margin-top: auto; display: flex; flex-direction: column; gap: 10px; }
    .btn-tg { background: var(--tg); color: white; padding: 12px; border-radius: 8px; text-decoration: none; font-weight: bold; text-align: center; font-size: 0.85rem; transition: 0.3s; }

    .main { flex: 1; padding: 20px 40px; margin-left: 240px; width: calc(100% - 240px); box-sizing: border-box; position: relative; } 

    /* ШАПКА */
    .header-home { display: flex; align-items: center; justify-content: space-between; margin-bottom: 30px; gap: 15px; }
    .search-box { width: 300px; position: relative; }
    .search-box input { width: 100%; background: var(--card); border: 1px solid #333; padding: 10px 15px; border-radius: 10px; color: white; outline: none; transition: 0.3s; }
    .search-box input:focus { border-color: var(--accent); }
    .mini-logo { width: 45px; height: 45px; border-radius: 8px; display: none; }

    /* КНОПКИ */
    .btn-install { background: var(--green); color: black; padding: 10px 20px; border: none; border-radius: 8px; font-weight: bold; text-align: center; font-size: 0.85rem; cursor: pointer; display: inline-block; text-decoration: none; transition: 0.2s; align-self: flex-start; }
    .btn-clear { background: #333; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-weight: bold; margin-bottom: 20px; font-size: 0.85rem; }
    .btn-clear:hover { background: var(--accent); }

    .top-bar-cheat { display: flex; align-items: center; justify-content: space-between; margin-bottom: 25px; }
    .btn-back { color: var(--accent); text-decoration: none; font-weight: bold; font-size: 1rem; }
    
    /* СЕРДЦЕ СПРАВА ВВЕРХУ */
    .heart-btn { cursor: pointer; font-size: 1.8rem; color: #333; background: none; border: none; transition: 0.3s; padding: 0; position: absolute; top: 20px; right: 20px; }
    .heart-btn.liked { color: var(--accent); filter: drop-shadow(0 0 5px var(--accent)); }

    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px; }
    .card { background: var(--card); border-radius: 15px; border: 1px solid #222; padding: 20px; transition: 0.2s; text-decoration: none; color: inherit; display: flex; flex-direction: column; position: relative; min-height: 160px; }
    .card h3 { margin: 0 0 10px 0; color: var(--accent); font-size: 1.3rem; padding-right: 40px; }
    .card p { margin: 0 0 20px 0; font-size: 0.9rem; color: var(--subtext); line-height: 1.4; }

    @media (max-width: 850px) {
        body { flex-direction: column; }
        .sidebar { width: 100%; height: auto; position: sticky; top: 0; border-right: none; border-bottom: 1px solid #222; padding: 10px; flex-direction: row; justify-content: space-around; }
        .logo-sidebar, .sidebar-bottom { display: none; }
        .main { margin-left: 0; padding: 20px; width: 100%; }
        .mini-logo { display: block; }
        .search-box { width: 100%; }
        .grid { grid-template-columns: 1fr; }
        .btn-install { display: none !important; }
        .mobile-no-download { display: block; background: #222; color: var(--subtext); padding: 12px; border-radius: 8px; text-align: center; font-size: 0.75rem; }
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
        if (idx > -1) { favs.splice(idx, 1); } 
        else { favs.push({id, name}); }
        localStorage.setItem('hk_favs', JSON.stringify(favs));
        
        let heart = document.getElementById('heart-'+id);
        if(heart) heart.classList.toggle('liked');
        if(window.location.pathname === '/favs') loadFavs();
    }

    function loadHeartState(id) {
        let favs = JSON.parse(localStorage.getItem('hk_favs') || '[]');
        if (favs.some(i => i.id === id)) document.getElementById('heart-'+id)?.classList.add('liked');
    }

    function clearAllFavs() {
        localStorage.setItem('hk_favs', '[]');
        loadFavs();
    }

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

CHEATS_DATA = {
    'wurst': {'title': 'Wurst Client', 'desc': 'Легендарная классика для Minecraft. Лучший выбор для выживания и грифа.', 'file': 'https://raw.githubusercontent.com/r1ze-r/HK/main/Wurst-Client1.21.11-hk.jar', 'ver': '1.21.1'},
    'meteor': {'title': 'Meteor Client', 'desc': 'Самый мощный софт для PVP и анархо-серверов. Огромное количество функций.', 'file': 'https://raw.githubusercontent.com/r1ze-r/HK/main/meteor-client-1.21.11-hk.jar', 'ver': '1.21.1'}
}

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
    cards_html = ""
    for id, info in CHEATS_DATA.items():
        cards_html += f'<div class="card"><button id="heart-{id}" class="heart-btn" onclick="toggleLike(\'{id}\', \'{info["title"]}\')">❤</button><a href="/{id}" style="text-decoration:none; color:inherit;"><h3>{info["title"]}</h3><p>{info["desc"]}</p></a><button onclick="forceDownload(\'{info["file"]}\', \'{id.capitalize()}_{info["ver"]}_HK.jar\')" class="btn-install">Скачать .jar</button><div class="mobile-no-download" style="display:none;">Только для ПК</div></div>'
    
    return render_template_string(f'''
        <!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>HK - Главная</title>{STYLE}</head>
        <body onload="{"; ".join([f"loadHeartState('{id}')" for id in CHEATS_DATA])}">{get_sidebar('home')}<div class="main">
            <div class="header-home">
                <h1>Все читы</h1>
                <div class="search-box"><input type="text" id="searchInput" onkeyup="filterCheats()" placeholder="Поиск читов..."></div>
            </div>
            <div class="grid" id="cheatGrid">{cards_html}</div>
        </div>{SCRIPTS}</body></html>''')

@app.route('/<name>')
def cheat_page(name):
    info = CHEATS_DATA.get(name)
    if not info: return "Страница не найдена", 404
    
    return render_template_string(f'''
        <!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>HK - {info['title']}</title>{STYLE}</head>
        <body onload="loadHeartState('{name}')">{get_sidebar(name)}
        <div class="main">
            <button id="heart-{name}" class="heart-btn" onclick="toggleLike('{name}', '{info['title']}')">❤</button>
            <div class="top-bar-cheat"><a href="/" class="btn-back">← Назад</a></div>
            <h1>{info['title']}</h1>
            <p style="color:var(--subtext); max-width: 600px;">{info['desc']}</p>
            <div style="margin-top:30px;">
                <button onclick="forceDownload('{info['file']}', '{name.capitalize()}_{info['ver']}_HK.jar')" class="btn-install">Скачать .jar</button>
                <div class="mobile-no-download" style="display:none;">Только для ПК</div>
            </div>
        </div>{SCRIPTS}</body></html>''')

@app.route('/favs')
def favs():
    return render_template_string(f'''
        <!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>HK - Избранное</title>{STYLE}</head>
        <body onload="loadFavs()">{get_sidebar('favs')}<div class="main">
            <h1>Понравившееся</h1>
            <button class="btn-clear" onclick="clearAllFavs()">Удалить всё</button>
            <div id="favs-list" class="grid"></div>
        </div>
        {SCRIPTS}<script>
            const cheatsData = {CHEATS_DATA};
            function loadFavs() {{
                let favs = JSON.parse(localStorage.getItem('hk_favs') || '[]');
                let list = document.getElementById('favs-list');
                list.innerHTML = '';
                if (favs.length === 0) {{
                    list.innerHTML = '<p style="color:var(--subtext);">Тут пока пусто.</p>';
                }} else {{
                    favs.forEach(i => {{
                        const info = cheatsData[i.id];
                        list.innerHTML += `
                            <div class="card">
                                <button id="heart-${{i.id}}" class="heart-btn liked" onclick="toggleLike('${{i.id}}', '${{i.name}}')">❤</button>
                                <a href="/${{i.id}}" style="text-decoration:none; color:inherit;">
                                    <h3>${{i.name}}</h3>
                                    <p>${{info ? info.desc : 'Твой выбор.'}}</p>
                                </a>
                                <button onclick="forceDownload('${{info.file}}', '${{i.id.charAt(0).toUpperCase() + i.id.slice(1)}}_${{info.ver}}_HK.jar')" class="btn-install">Скачать</button>
                            </div>`;
                    }});
                }}
            }}
        </script></body></html>''')
