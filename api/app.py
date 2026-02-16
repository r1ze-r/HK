from flask import Flask, render_template_string, request

app = Flask(__name__)

STYLE = '''
<style>
    :root { --bg: #0a0a0a; --card: #161616; --accent: #ff4444; --green: #2ecc71; --tg: #24A1DE; --text: #ffffff; --subtext: #a1a1a1; --modal-bg: rgba(0,0,0,0.85); }
    body { background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; margin: 0; display: flex; min-height: 100vh; overflow-x: hidden; }
    
    .sidebar { width: 240px; background: var(--card); height: 100vh; padding: 25px 15px; box-sizing: border-box; display: flex; flex-direction: column; border-right: 1px solid #222; position: fixed; z-index: 100; }
    .logo-sidebar { text-align: center; margin-bottom: 30px; }
    .logo-sidebar img { width: 100px; height: 100px; border-radius: 15px; filter: drop-shadow(0 0 5px var(--accent)); }
    
    .nav-item { padding: 12px 15px; border-radius: 8px; cursor: pointer; color: var(--subtext); transition: 0.2s; text-decoration: none; margin-bottom: 5px; font-weight: 500; display: block; font-size: 0.95rem; }
    .nav-item:hover, .nav-item.active { background: #222; color: white; }
    
    .sidebar-bottom { margin-top: auto; display: flex; flex-direction: column; gap: 10px; }
    .btn-tg { background: var(--tg); color: white; padding: 12px; border-radius: 8px; text-decoration: none; font-weight: bold; text-align: center; font-size: 0.85rem; }
    .btn-dl-sidebar { background: var(--green); color: black; padding: 12px; border-radius: 8px; text-decoration: none; font-weight: bold; text-align: center; font-size: 0.85rem; display: none; margin-bottom: 5px; cursor: pointer; border:none; width:100%; }

    .main { flex: 1; padding: 20px 40px; margin-left: 240px; width: calc(100% - 240px); box-sizing: border-box; } 

    /* ШАПКА И ПОИСК */
    .header-home { display: flex; flex-direction: column; align-items: center; margin-bottom: 40px; gap: 20px; }
    .search-box { width: 100%; max-width: 500px; }
    .search-box input { width: 100%; background: var(--card); border: 1px solid #333; padding: 12px 20px; border-radius: 12px; color: white; outline: none; text-align: center; font-size: 1rem; }
    .search-box input:focus { border-color: var(--accent); }

    .ver-badge { font-size: 0.7rem; color: var(--subtext); background: #222; padding: 2px 8px; border-radius: 5px; margin-top: 5px; display: inline-block; border: 1px solid #333; }

    /* КНОПКИ ИЗБРАННОГО */
    .fav-controls { display: flex; justify-content: center; gap: 15px; margin-bottom: 30px; flex-wrap: wrap; }
    .btn-fav { padding: 10px 20px; border-radius: 8px; font-weight: bold; cursor: pointer; border: 1px solid transparent; transition: 0.3s; font-size: 0.85rem; }
    .btn-fav.red { background: #333; color: white; }
    .btn-fav.red:hover, .btn-fav.red.active { background: var(--accent); border-color: var(--accent); }
    .btn-fav.green { background: var(--green); color: black; }

    /* КАРТОЧКИ */
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
    .card { background: var(--card); border-radius: 15px; border: 1px solid #222; padding: 20px; transition: 0.2s; text-decoration: none; color: inherit; display: flex; flex-direction: column; position: relative; cursor: pointer; }
    .card:hover { border-color: #444; }
    .card.selecting { border-color: var(--accent) !important; box-shadow: 0 0 10px rgba(255, 68, 68, 0.3); }
    .card h3 { margin: 0; color: var(--accent); font-size: 1.2rem; }
    .heart-abs { position: absolute; top: 15px; right: 15px; font-size: 1.5rem; color: #333; background:none; border:none; cursor:pointer; }
    .heart-abs.liked { color: var(--accent); }

    /* МОДАЛКА */
    .modal { display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background: var(--modal-bg); align-items: center; justify-content: center; }
    .modal-content { background: var(--card); padding: 30px; border-radius: 15px; border: 1px solid #333; text-align: center; max-width: 400px; width: 90%; }
    .modal-btns { display: flex; gap: 10px; justify-content: center; margin-top: 20px; }
    .btn-yes { background: var(--accent); color: white; border: none; padding: 10px 25px; border-radius: 8px; cursor: pointer; font-weight: bold; }
    .btn-no { background: #111; color: white; border: 1px solid #444; padding: 10px 25px; border-radius: 8px; cursor: pointer; font-weight: bold; }

    @media (max-width: 850px) {
        body { flex-direction: column; }
        .sidebar { width: 100%; height: auto; position: sticky; top: 0; border-right: none; border-bottom: 1px solid #222; padding: 10px; flex-direction: row; flex-wrap: wrap; justify-content: space-around; }
        .logo-sidebar, .sidebar-bottom { display: none; }
        .main { margin-left: 0; padding: 20px; width: 100%; }
        .search-box { width: 100%; }
        .fav-controls .btn-fav { flex: 1; min-width: 100px; padding: 10px 5px; font-size: 0.75rem; }
        .mobile-header { display: flex; justify-content: space-between; align-items: center; width: 100%; margin-bottom: 15px; }
    }
</style>
'''

SCRIPTS = '''
<script>
    let selectMode = false;
    let selectedIds = [];

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
        if (idx > -1) favs.splice(idx, 1);
        else favs.push({id, name});
        localStorage.setItem('hk_favs', JSON.stringify(favs));
        location.reload();
    }

    function openModal() { document.getElementById('confirmModal').style.display = 'flex'; }
    function closeModal() { document.getElementById('confirmModal').style.display = 'none'; }
    
    function clearAll() {
        localStorage.setItem('hk_favs', '[]');
        location.reload();
    }

    function toggleSelectMode() {
        selectMode = !selectMode;
        document.getElementById('btn-select').classList.toggle('active');
        if(!selectMode) {
            selectedIds = [];
            document.querySelectorAll('.card').forEach(c => c.classList.remove('selecting'));
        }
    }

    function handleCardClick(id, event) {
        if(selectMode) {
            event.preventDefault();
            const card = document.getElementById('card-'+id);
            if(selectedIds.includes(id)) {
                selectedIds = selectedIds.filter(i => i !== id);
                card.classList.remove('selecting');
            } else {
                selectedIds.push(id);
                card.classList.add('selecting');
            }
        } else {
            window.location.href = '/' + id;
        }
    }

    function deleteSelected() {
        if(selectedIds.length === 0) return;
        let favs = JSON.parse(localStorage.getItem('hk_favs') || '[]');
        favs = favs.filter(i => !selectedIds.includes(i.id));
        localStorage.setItem('hk_favs', JSON.stringify(favs));
        location.reload();
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
    'wurst': {'title': 'Wurst Client', 'desc': 'Удобный клиент для выживания. Классика.', 'file': 'https://raw.githubusercontent.com/r1ze-r/HK/main/Wurst-Client1.21.11-hk.jar', 'ver': '1.21.11'},
    'meteor': {'title': 'Meteor Client', 'desc': 'Популярный чит для PVP и анархии. Много настроек.', 'file': 'https://raw.githubusercontent.com/r1ze-r/HK/main/meteor-client-1.21.11-hk.jar', 'ver': '1.21.11'}
}

def get_sidebar(active, current_cheat=None):
    dl_btn = ""
    if current_cheat:
        info = CHEATS_DATA[current_cheat]
        dl_btn = f'<button onclick="forceDownload(\'{info["file"]}\', \'{current_cheat.capitalize()}_{info["ver"]}_HK.jar\')" class="btn-dl-sidebar" style="display:block;">Скачать .jar</button>'
    
    return f'''
    <div class="sidebar">
        <div class="logo-sidebar"><img src="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png"></div>
        <a href="/" class="nav-item {'active' if active=='home' else ''}">Главная</a>
        <a href="/favs" class="nav-item {'active' if active=='favs' else ''}">Понравившееся</a>
        <div class="sidebar-bottom">
            {dl_btn}
            <a href="https://t.me/hellokilaura" target="_blank" class="btn-tg">Наш Telegram</a>
        </div>
    </div>'''

@app.route('/')
def home():
    cards = ""
    for id, info in CHEATS_DATA.items():
        cards += f'''<div class="card" id="card-{id}" onclick="handleCardClick('{id}', event)">
            <h3>{info['title']}</h3>
            <p>{info['desc']}</p>
            <span class="ver-badge">{info['ver']}</span>
        </div>'''
    
    return render_template_string(f'''
        <!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>HK - Главная</title>{STYLE}</head>
        <body>{get_sidebar('home')}<div class="main">
            <div class="header-home">
                <div class="search-box"><input type="text" id="searchInput" onkeyup="filterCheats()" placeholder="Поиск читов..."></div>
                <h1>Все читы</h1>
            </div>
            <div class="grid">{cards}</div>
        </div>{SCRIPTS}</body></html>''')

@app.route('/<name>')
def cheat_page(name):
    info = CHEATS_DATA.get(name)
    if not info: return "404", 404
    return render_template_string(f'''
        <!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>HK - {info['title']}</title>{STYLE}</head>
        <body>{get_sidebar(name, current_cheat=name)}
        <div class="main">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <a href="/" style="color:var(--accent); text-decoration:none; font-weight:bold;">← Назад</a>
                <button class="heart-abs" id="heart-{name}" onclick="toggleLike('{name}', '{info['title']}')">❤</button>
            </div>
            <h1 style="margin-top:40px;">{info['title']} <span style="font-size:0.9rem; color:var(--subtext);">({info['ver']})</span></h1>
            <p style="color:var(--subtext); max-width:600px; line-height:1.6;">{info['desc']}</p>
        </div>
        {SCRIPTS}<script>
            let favs = JSON.parse(localStorage.getItem('hk_favs') || '[]');
            if(favs.some(i => i.id === '{name}')) document.getElementById('heart-{name}').classList.add('liked');
        </script></body></html>''')

@app.route('/favs')
def favs():
    return render_template_string(f'''
        <!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>HK - Избранное</title>{STYLE}</head>
        <body>{get_sidebar('favs')}<div class="main">
            <div class="mobile-header">
                <h1>Понравившееся</h1>
                <button class="btn-fav green" style="display:none;" id="btn-ubrat" onclick="location.href='/'">Убрать</button>
            </div>
            
            <div class="fav-controls">
                <button class="btn-fav red" onclick="openModal()">Удалить всё</button>
                <button class="btn-fav red" onclick="toggleSelectMode()" id="btn-select">Удалить выбранное</button>
                <button class="btn-fav red" onclick="deleteSelected()">Подтвердить удаление</button>
            </div>

            <div id="favs-list" class="grid"></div>

            <div id="confirmModal" class="modal">
                <div class="modal-content">
                    <h3>Вы подтверждаете удалить всё?</h3>
                    <div class="modal-btns">
                        <button class="btn-yes" onclick="clearAll()">Да</button>
                        <button class="btn-no" onclick="closeModal()">Нет</button>
                    </div>
                </div>
            </div>
        </div>
        {SCRIPTS}<script>
            if(window.innerWidth < 850) document.getElementById('btn-ubrat').style.display = 'block';
            
            let favs = JSON.parse(localStorage.getItem('hk_favs') || '[]');
            let list = document.getElementById('favs-list');
            if (favs.length === 0) list.innerHTML = '<p style="text-align:center; color:var(--subtext); width:100%;">Тут пока пусто.</p>';
            else favs.forEach(i => {{
                list.innerHTML += `<div class="card" id="card-${{i.id}}" onclick="handleCardClick('${{i.id}}', event)">
                    <h3>${{i.name}}</h3>
                    <p>Нажми, чтобы перейти к скачиванию.</p>
                </div>`;
            }});
        </script></body></html>''')
