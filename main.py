from flask import Flask, render_template_string

app = Flask(__name__)

STYLE = '''
<style>
    :root { --bg: #0a0a0a; --card: #161616; --accent: #ff4444; --green: #2ecc71; --tg: #24A1DE; --text: #ffffff; --subtext: #a1a1a1; }
    body { background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; margin: 0; display: flex; min-height: 100vh; }
    
    .sidebar { width: 240px; background: var(--card); height: 100vh; padding: 25px 15px; box-sizing: border-box; display: flex; flex-direction: column; border-right: 1px solid #222; position: fixed; z-index: 100; }
    .logo-container { text-align: center; margin-bottom: 30px; }
    .logo-container img { width: 120px; height: 120px; border-radius: 18px; filter: drop-shadow(0 0 8px var(--accent)); }
    .nav-item { padding: 10px 15px; border-radius: 8px; cursor: pointer; color: var(--subtext); transition: 0.2s; text-decoration: none; margin-bottom: 5px; font-weight: 500; display: block; font-size: 0.9rem; }
    .nav-item:hover, .nav-item.active { background: #222; color: white; }
    
    .sidebar-bottom { margin-top: auto; display: flex; flex-direction: column; gap: 10px; }
    .btn-tg { background: var(--tg); color: white; padding: 12px; border-radius: 8px; text-decoration: none; font-weight: bold; text-align: center; font-size: 0.85rem; transition: 0.3s; }
    .btn-tg:hover { filter: brightness(1.2); transform: translateY(-2px); }
    .btn-install { background: var(--green); color: black; padding: 12px; border-radius: 8px; text-decoration: none; font-weight: bold; text-align: center; font-size: 0.9rem; transition: 0.3s; }
    .btn-install:hover { transform: scale(1.02); box-shadow: 0 0 15px rgba(46, 204, 113, 0.3); }

    .main { flex: 1; padding: 20px 40px; margin-left: 240px; } /* Уменьшил padding сверху */
    .top-bar { display: flex; align-items: center; justify-content: center; position: relative; margin-bottom: 20px; min-height: 40px; } /* Поднял выше */
    .search-bar { background: #1a1a1a; border: 1px solid #333; padding: 10px 20px; border-radius: 12px; width: 400px; color: white; outline: none; transition: 0.3s; font-size: 0.9rem; }
    .search-bar:focus { border-color: var(--accent); box-shadow: 0 0 15px rgba(255, 68, 68, 0.15); }
    
    .btn-back-abs { position: absolute; left: 0; color: var(--accent); text-decoration: none; font-weight: bold; }
    .heart-container { position: absolute; right: 0; }
    .heart-btn { cursor: pointer; font-size: 2rem; color: #333; transition: 0.3s; background: none; border: none; outline: none; }
    .heart-btn.liked { color: var(--accent); filter: drop-shadow(0 0 5px var(--accent)); }

    .control-btns { display: flex; gap: 10px; }
    .ctrl-btn { background: #222; color: var(--subtext); border: 1px solid #333; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 0.8rem; transition: 0.2s; }
    .ctrl-btn.active-mode { background: var(--accent); color: white; border-color: white; }
    .btn-delete-multi { position: absolute; right: 0; background: var(--accent); color: white; border: none; padding: 10px 20px; border-radius: 8px; font-weight: bold; cursor: pointer; display: none; }

    h1 { margin-top: 0; margin-bottom: 20px; font-size: 1.8rem; } /* Поднял заголовок */

    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
    .card { background: var(--card); border-radius: 15px; border: 1px solid #222; padding: 20px; transition: 0.2s; text-decoration: none; color: inherit; display: block; position: relative; cursor: pointer; }
    .card:hover { border-color: var(--accent); transform: translateY(-3px); }
    .card.selected { border: 2px solid var(--accent) !important; box-shadow: 0 0 10px rgba(255, 68, 68, 0.2); }
    .card h3 { margin: 0 0 8px 0; color: var(--accent); }
    .card p { margin: 0; font-size: 0.9rem; color: var(--subtext); line-height: 1.4; }
</style>
'''

SCRIPTS = '''
<script>
    let mode = 'none';
    let selectedItems = new Set();

    function filterCheats() {
        let input = document.getElementById('search').value.toLowerCase();
        let cards = document.querySelectorAll('.grid .card');
        cards.forEach(card => {
            let title = card.querySelector('h3').innerText.toLowerCase();
            card.style.display = title.includes(input) ? 'block' : 'none';
        });
    }

    function toggleLike(id, name) {
        let favs = JSON.parse(localStorage.getItem('hk_favs') || '[]');
        const index = favs.findIndex(item => item.id === id);
        if (index > -1) {
            favs.splice(index, 1);
            document.getElementById('heart-'+id)?.classList.remove('liked');
        } else {
            favs.push({id, name});
            document.getElementById('heart-'+id)?.classList.add('liked');
        }
        localStorage.setItem('hk_favs', JSON.stringify(favs));
    }

    function setMode(newMode) {
        mode = (mode === newMode) ? 'none' : newMode;
        selectedItems.clear();
        document.querySelectorAll('.ctrl-btn').forEach(b => b.classList.remove('active-mode'));
        if (mode !== 'none') document.getElementById('mode-' + mode).classList.add('active-mode');
        renderFavs();
    }

    function handleCardClick(id, event) {
        if (mode === 'one') {
            removeOne(id);
        } else if (mode === 'multi') {
            event.preventDefault();
            if (selectedItems.has(id)) selectedItems.delete(id);
            else selectedItems.add(id);
            renderFavs();
        } else {
            window.location.href = '/' + id;
        }
    }

    function removeOne(id) {
        let favs = JSON.parse(localStorage.getItem('hk_favs') || '[]');
        localStorage.setItem('hk_favs', JSON.stringify(favs.filter(i => i.id !== id)));
        renderFavs();
    }

    function deleteSelected() {
        let favs = JSON.parse(localStorage.getItem('hk_favs') || '[]');
        localStorage.setItem('hk_favs', JSON.stringify(favs.filter(i => !selectedItems.has(i.id))));
        selectedItems.clear();
        setMode('none');
        renderFavs();
    }

    function renderFavs() {
        const grid = document.getElementById('fav-grid');
        if (!grid) return;
        let favs = JSON.parse(localStorage.getItem('hk_favs') || '[]');
        document.getElementById('btn-delete-all').style.display = (mode === 'multi' && selectedItems.size > 0) ? 'block' : 'none';
        
        if (favs.length === 0) {
            grid.innerHTML = '<div style="color:var(--subtext); grid-column:1/-1; text-align:center; margin-top:40px;">В списке пока ничего нет...</div>';
            return;
        }
        grid.innerHTML = favs.map(item => `
            <div class="card ${selectedItems.has(item.id) ? 'selected' : ''}" onclick="handleCardClick('${item.id}', event)">
                <h3>${item.name}</h3>
            </div>
        `).join('');
    }

    function loadHeartState(id) {
        let favs = JSON.parse(localStorage.getItem('hk_favs') || '[]');
        if (favs.some(i => i.id === id)) document.getElementById('heart-'+id)?.classList.add('liked');
    }
</script>
'''

def get_sidebar(active_page, file_url=None):
    install_btn = f'<a href="{file_url}" class="btn-install" download>Скачать .jar</a>' if file_url else ''
    return f'''
    <div class="sidebar">
        <div class="logo-container">
            <img src="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png" alt="HK">
        </div>
        <a href="/" class="nav-item {'active' if active_page == 'home' else ''}">Главная</a>
        <a href="/favs" class="nav-item {'active' if active_page == 'favs' else ''}">Понравившееся</a>
        <a href="#" class="nav-item">Настройки</a>
        
        <div class="sidebar-bottom">
            <a href="https://t.me/hellokilaura" target="_blank" class="btn-tg">Наш Telegram</a>
            {install_btn}
        </div>
    </div>
    '''

@app.route('/')
def home():
    return render_template_string(f'''
        <!DOCTYPE html><html><head><meta charset="UTF-8"><link rel="icon" href="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png"><title>HK - Главная</title>{STYLE}</head>
        <body>{get_sidebar('home')}<div class="main">
            <div class="top-bar"><input type="text" id="search" class="search-bar" placeholder="Поиск читов..." onkeyup="filterCheats()"></div>
            <h1>Главное меню</h1>
            <div class="grid">
                <a href="/wurst" class="card"><h3>Wurst</h3><p>Удобный клиент для выживания с друзьями.</p></a>
                <a href="/meteor" class="card"><h3>Meteor Client</h3><p>Стабильная сборка для совместного фана.</p></a>
            </div>
        </div>{SCRIPTS}</body></html>
    ''')

@app.route('/favs')
def favs():
    return render_template_string(f'''
        <!DOCTYPE html><html><head><meta charset="UTF-8"><link rel="icon" href="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png"><title>HK - Понравившееся</title>{STYLE}</head>
        <body onload="renderFavs()">{get_sidebar('favs')}<div class="main">
            <div class="top-bar"><a href="/" class="btn-back-abs">← Назад</a>
                <div class="control-btns">
                    <button class="ctrl-btn" onclick="localStorage.setItem('hk_favs', '[]'); renderFavs()">Убрать всё</button>
                    <button id="mode-one" class="ctrl-btn" onclick="setMode('one')">Убрать одно</button>
                    <button id="mode-multi" class="ctrl-btn" onclick="setMode('multi')">Убрать выделенное</button>
                </div>
                <button id="btn-delete-all" class="btn-delete-multi" onclick="deleteSelected()">Убрать</button>
            </div>
            <h1>Понравившееся</h1><div class="grid" id="fav-grid"></div>
        </div>{SCRIPTS}</body></html>
    ''')

@app.route('/wurst')
def wurst_page():
    return render_template_string(f'''
        <!DOCTYPE html><html><head><meta charset="UTF-8"><link rel="icon" href="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png"><title>HK - Wurst</title>{STYLE}</head>
        <body onload="loadHeartState('wurst')">{get_sidebar('wurst', 'https://raw.githubusercontent.com/r1ze-r/HK/main/Wurst-Client1.21.11-nk.jar')}
        <div class="main"><div class="top-bar"><a href="/" class="btn-back-abs">← Назад на главную</a>
        <div class="heart-container"><button id="heart-wurst" class="heart-btn" onclick="toggleLike('wurst', 'Wurst')">❤</button></div>
        </div><h1>Wurst Client 1.21.11-nk</h1><p style="color:var(--subtext); font-size:1.1rem; line-height:1.6;">Легендарная классика для тех, кто любит проводить время в Minecraft с друзьями. Понятный интерфейс и стабильная работа.</p></div>{SCRIPTS}</body></html>
    ''')

@app.route('/meteor')
def meteor_page():
    return render_template_string(f'''
        <!DOCTYPE html><html><head><meta charset="UTF-8"><link rel="icon" href="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png"><title>HK - Meteor</title>{STYLE}</head>
        <body onload="loadHeartState('meteor')">{get_sidebar('meteor', 'https://raw.githubusercontent.com/r1ze-r/HK/main/meteor-client-1.21.11-nk.jar')}
        <div class="main"><div class="top-bar"><a href="/" class="btn-back-abs">← Назад на главную</a>
        <div class="heart-container"><button id="heart-meteor" class="heart-btn" onclick="toggleLike('meteor', 'Meteor Client')">❤</button></div>
        </div><h1>Meteor Client 1.21.11-nk</h1><p style="color:var(--subtext); font-size:1.1rem; line-height:1.6;">Отличный инструмент для совместных PVP-потасовок и выживания. Сбалансированный набор функций и высокая производительность.</p></div>{SCRIPTS}</body></html>
    ''')

if __name__ == "__main__":
    app.run()
