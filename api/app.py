from flask import Flask, render_template_string

app = Flask(__name__)

# --- БАЗА (Только рабочие) ---
DATABASE = {
    'wurst': {
        'name': 'Wurst Client',
        'desc': 'Классика выживания. Удобный интерфейс и проверенные временем функции.',
        'ver': '1.21.1',
        'file_url': 'https://raw.githubusercontent.com/r1ze-r/HK/main/Wurst-Client1.21.11-hk.jar'
    },
    'meteor': {
        'name': 'Meteor Client',
        'desc': 'Самый мощный софт для PVP и анархии. Постоянные обновления и гибкая настройка.',
        'ver': '1.21.1',
        'file_url': 'https://raw.githubusercontent.com/r1ze-r/HK/main/meteor-client-1.21.11-hk.jar'
    }
}

STYLE = '''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    :root {
        --bg: #0a0a0a; --side: #111; --card: #151515; --border: #222; 
        --accent: #ff4444; --text: #fff; --dim: #888; --tg: #24A1DE;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; display: flex; min-height: 100vh; overflow-x: hidden; }

    /* SIDEBAR */
    .sidebar { width: 260px; background: var(--side); border-right: 1px solid var(--border); display: flex; flex-direction: column; padding: 30px 20px; position: fixed; height: 100vh; z-index: 100; }
    .logo-box { width: 80px; height: 80px; margin: 0 auto 40px; border-radius: 20px; overflow: hidden; box-shadow: 0 0 20px rgba(255,68,68,0.2); border: 1px solid var(--border); }
    .logo-box img { width: 100%; height: 100%; object-fit: cover; }
    
    .side-nav { display: flex; flex-direction: column; gap: 10px; }
    .side-link { padding: 15px 20px; border-radius: 12px; text-decoration: none; color: var(--dim); font-weight: 700; transition: 0.3s; }
    .side-link:hover, .side-link.active { background: #1a1a1a; color: #fff; box-shadow: inset 4px 0 0 var(--accent); }

    /* CONTENT AREA */
    .main-content { margin-left: 260px; flex: 1; padding: 40px; position: relative; }
    header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 50px; }
    
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
    .card { background: var(--card); border: 1px solid var(--border); border-radius: 20px; padding: 25px; cursor: pointer; transition: 0.3s; position: relative; display: flex; flex-direction: column; }
    .card:hover { transform: translateY(-5px); border-color: #333; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .card.selected { border-color: var(--accent); background: #1a1414; }

    .card h3 { color: var(--accent); margin-bottom: 10px; font-size: 1.4rem; }
    .card p { color: var(--dim); font-size: 0.9rem; margin-bottom: 20px; flex-grow: 1; }
    
    .card-footer { display: flex; justify-content: space-between; align-items: center; }
    .ver-badge { background: #000; padding: 4px 10px; border-radius: 8px; font-size: 0.75rem; border: 1px solid #222; color: #777; font-weight: 800; }
    
    .heart { width: 40px; height: 40px; border-radius: 10px; background: #1a1a1a; border: none; color: #333; cursor: pointer; transition: 0.3s; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; }
    .heart.liked { color: var(--accent); background: rgba(255,68,68,0.1); text-shadow: 0 0 10px var(--accent); }

    /* UI ELEMENTS */
    .tg-btn { background: var(--tg); color: #fff; padding: 15px 24px; border-radius: 14px; text-decoration: none; font-weight: 900; box-shadow: 0 5px 15px rgba(36,161,222,0.3); transition: 0.3s; }
    .tg-btn:hover { transform: scale(1.05); }
    
    .dl-btn { background: #2ecc71; color: #000; padding: 18px 35px; border-radius: 15px; text-decoration: none; font-weight: 900; display: inline-block; margin-top: 25px; transition: 0.3s; }
    .dl-btn:hover { transform: scale(1.02); box-shadow: 0 0 20px rgba(46,204,113,0.3); }

    .action-group { display: flex; gap: 10px; margin-bottom: 30px; justify-content: center; }
    .btn-action { padding: 10px 20px; border-radius: 10px; border: 1px solid #333; background: #151515; color: #fff; cursor: pointer; font-weight: 700; transition: 0.2s; }
    .btn-action.active { background: var(--accent); border-color: var(--accent); }
    .confirm-float { position: fixed; bottom: 30px; right: 30px; background: #2ecc71; color: #000; padding: 20px 40px; border-radius: 15px; font-weight: 900; cursor: pointer; border: none; display: none; z-index: 1000; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }

    @media (max-width: 800px) {
        .sidebar { width: 70px; padding: 20px 10px; }
        .side-link span { display: none; }
        .main-content { margin-left: 70px; }
        .logo-box { width: 40px; height: 40px; margin-bottom: 20px; }
    }
</style>
'''

JS = '''
<script>
    let mode = 'normal';
    let selected = [];

    function getFavs() { return JSON.parse(localStorage.getItem('hk_favs_final') || '[]'); }
    
    function toggleLike(e, id, name) {
        if(e) e.stopPropagation();
        let favs = getFavs();
        let idx = favs.findIndex(x => x.id === id);
        
        if(idx > -1) {
            favs.splice(idx, 1);
        } else {
            favs.push({id: id, name: name});
        }
        
        localStorage.setItem('hk_favs_final', JSON.stringify(favs));
        
        // Визуальное обновление без перезагрузки
        document.querySelectorAll(`.heart[data-id="${id}"]`).forEach(h => {
            h.classList.toggle('liked');
        });

        // Если мы на странице избранного и убрали лайк - удаляем карточку
        if(document.getElementById('fav-page-id') && idx > -1) {
            document.getElementById('card-'+id)?.remove();
        }
    }

    function handleCardClick(id) {
        if(mode === 'normal') window.location.href = '/cheat/' + id;
        else if(mode === 'single') toggleLike(null, id);
        else if(mode === 'multi') {
            const card = document.getElementById('card-' + id);
            card.classList.toggle('selected');
            if(selected.includes(id)) selected = selected.filter(x => x !== id);
            else selected.push(id);
        }
    }

    function setMode(m, btn) {
        mode = (mode === m) ? 'normal' : m;
        document.querySelectorAll('.btn-action').forEach(b => b.classList.remove('active'));
        if(mode !== 'normal') btn.classList.add('active');
        document.getElementById('confirm-btn').style.display = (mode === 'multi') ? 'block' : 'none';
        
        if(mode === 'normal') {
            document.querySelectorAll('.card').forEach(c => c.classList.remove('selected'));
            selected = [];
        }
    }

    function deleteSelected() {
        let favs = getFavs().filter(x => !selected.includes(x.id));
        localStorage.setItem('hk_favs_final', JSON.stringify(favs));
        selected.forEach(id => document.getElementById('card-'+id)?.remove());
        setMode('normal');
    }

    // Инициализация лайков при загрузке любой страницы
    document.addEventListener('DOMContentLoaded', () => {
        let favs = getFavs();
        document.querySelectorAll('.heart').forEach(h => {
            if(favs.some(f => f.id === h.dataset.id)) h.classList.add('liked');
        });
    });
</script>
'''

def get_sidebar(active_page):
    return f'''
    <div class="sidebar">
        <div class="logo-box">
            <img src="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png" alt="HK Logo">
        </div>
        <div class="side-nav">
            <a href="/" class="side-link {'active' if active_page=='home' else ''}"><span>Главная</span></a>
            <a href="/favs" class="side-link {'active' if active_page=='favs' else ''}"><span>Понравившееся</span></a>
        </div>
        <div style="margin-top:auto; padding-bottom: 20px;">
            <a href="https://t.me/hellokilaura" class="tg-btn" target="_blank" style="display:block; text-align:center;">Telegram</a>
        </div>
    </div>
    '''

@app.route('/')
def home():
    cards = ""
    for k, v in DATABASE.items():
        cards += f'''
        <div class="card" id="card-{k}" onclick="handleCardClick('{k}')">
            <h3>{v['name']}</h3>
            <p>{v['desc']}</p>
            <div class="card-footer">
                <span class="ver-badge">{v['ver']}</span>
                <button class="heart" data-id="{k}" onclick="toggleLike(event, '{k}', '{v['name']}')">❤</button>
            </div>
        </div>'''
    return render_template_string(f'''
    <html><head><title>HK Hub</title>{STYLE}</head><body>
        {get_sidebar('home')}
        <div class="main-content">
            <header><h1>Все читы</h1></header>
            <div class="grid">{cards}</div>
        </div>{JS}
    </body></html>''')

@app.route('/cheat/<id>')
def cheat(id):
    item = DATABASE.get(id)
    if not item: return "404", 404
    return render_template_string(f'''
    <html><head><title>{item['name']}</title>{STYLE}</head><body>
        {get_sidebar('home')}
        <div class="main-content">
            <a href="/" style="color:var(--accent); text-decoration:none; font-weight:800; font-size:0.9rem;">← НАЗАД В КАТАЛОГ</a>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:30px;">
                <h1 style="font-size:3.5rem; font-weight:900; margin:0;">{item['name']}</h1>
                <button class="heart" data-id="{id}" onclick="toggleLike(event, '{id}', '{item['name']}')" style="width:70px; height:70px; font-size:2rem;">❤</button>
            </div>
            <div style="background:var(--card); padding:40px; border-radius:25px; border:1px solid var(--border); margin-top:40px;">
                <span class="ver-badge" style="padding:6px 15px;">Версия: {item['ver']}</span>
                <p style="font-size:1.3rem; margin:25px 0; color:#ccc; line-height:1.6;">{item['desc']}</p>
                <a href="{item['file_url']}" class="dl-btn">Скачать .JAR Клиент</a>
            </div>
        </div>{JS}
    </body></html>''')

@app.route('/favs')
def favs():
    return render_template_string(f'''
    <html><head><title>Избранное</title>{STYLE}</head><body>
        <div id="fav-page-id"></div>
        {get_sidebar('favs')}
        <div class="main-content">
            <button id="confirm-btn" class="confirm-float" onclick="deleteSelected()">Убрать выбранное</button>
            <header><h1>Твоя Коллекция</h1></header>
            <div class="action-group">
                <button class="btn-action" onclick="localStorage.setItem('hk_favs_final','[]'); location.reload();">Удалить всё</button>
                <button class="btn-action" onclick="setMode('multi', this)">Выбрать несколько</button>
                <button class="btn-action" onclick="setMode('single', this)">Удалять по одному</button>
            </div>
            <div id="fav-grid" class="grid"></div>
        </div>{JS}
        <script>
            const db = {DATABASE};
            let favs = getFavs();
            let g = document.getElementById('fav-grid');
            if(!favs.length) g.innerHTML = '<div style="grid-column:1/-1; text-align:center; font-size:2rem; color:#222; font-weight:900; margin-top:100px;">ПУСТО</div>';
            else favs.forEach(f => {{
                let item = db[f.id] || {{name: f.name, desc: 'Нажми для просмотра', ver: '?'}};
                g.innerHTML += `<div class="card" id="card-${{f.id}}" onclick="handleCardClick('${{f.id}}')"><h3>${{item.name}}</h3><p>${{item.desc}}</p><div class="card-footer"><span class="ver-badge">${{item.ver}}</span><button class="heart liked" data-id="${{f.id}}" onclick="toggleLike(event, '${{f.id}}')">❤</button></div></div>`;
            }});
        </script>
    </body></html>''')

if __name__ == '__main__':
    app.run(debug=True)
