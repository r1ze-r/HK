from flask import Flask, render_template_string

app = Flask(__name__)

# Твой лютейший дизайн
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
    
    .btn-install { background: var(--green); color: black; padding: 12px; border: none; border-radius: 8px; font-weight: bold; text-align: center; font-size: 0.9rem; transition: 0.3s; cursor: pointer; width: 100%; display: block; }
    .btn-install:hover { transform: scale(1.02); box-shadow: 0 0 15px rgba(46, 204, 113, 0.3); }

    .main { flex: 1; padding: 20px 40px; margin-left: 240px; } 
    .top-bar { display: flex; align-items: center; justify-content: center; position: relative; margin-bottom: 25px; min-height: 45px; }
    .btn-back-abs { position: absolute; left: 0; color: var(--accent); text-decoration: none; font-weight: bold; }
    
    .heart-container { position: absolute; right: 0; }
    .heart-btn { cursor: pointer; font-size: 2rem; color: #333; transition: 0.3s; background: none; border: none; outline: none; }
    .heart-btn.liked { color: var(--accent); filter: drop-shadow(0 0 5px var(--accent)); }

    h1 { margin-top: 0; margin-bottom: 20px; font-size: 1.8rem; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
    
    .card { background: var(--card); border-radius: 15px; border: 1px solid #222; padding: 20px; transition: 0.2s; text-decoration: none; color: inherit; display: flex; flex-direction: column; cursor: pointer; min-height: 140px; }
    .card:hover { border-color: var(--accent); transform: translateY(-3px); }
    .card h3 { margin: 0 0 8px 0; color: var(--accent); }
    .card p { margin: 0 0 15px 0; font-size: 0.9rem; color: var(--subtext); line-height: 1.4; flex-grow: 1; }
    .card-footer { display: flex; align-items: center; margin-top: auto; }
    .card-version { background: #222; color: var(--subtext); padding: 2px 8px; border-radius: 5px; font-size: 0.7rem; font-weight: bold; border: 1px solid #333; }
</style>
'''

# Скрипты для лайков и ПРИНУДИТЕЛЬНОГО скачивания
SCRIPTS = '''
<script>
    async function forceDownload(url, filename) {
        try {
            const response = await fetch(url);
            const blob = await response.blob();
            const link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        } catch (e) {
            console.error("Download failed, falling back to link", e);
            window.location.href = url;
        }
    }

    function toggleLike(id, name) {
        let favs = JSON.parse(localStorage.getItem('hk_favs') || '[]');
        const index = favs.findIndex(item => item.id === id);
        if (index > -1) {
            favs.splice(index, 1);
            document.getElementById('heart-'+id).classList.remove('liked');
        } else {
            favs.push({id, name});
            document.getElementById('heart-'+id).classList.add('liked');
        }
        localStorage.setItem('hk_favs', JSON.stringify(favs));
    }

    function loadHeartState(id) {
        let favs = JSON.parse(localStorage.getItem('hk_favs') || '[]');
        if (favs.some(i => i.id === id)) document.getElementById('heart-'+id)?.classList.add('liked');
    }
</script>
'''

def get_sidebar(active_page, file_url=None):
    if file_url:
        filename = file_url.split('/')[-1]
        # Используем кнопку с JS функцией для скачивания
        install_btn = f'<button onclick="forceDownload(\'{file_url}\', \'{filename}\')" class="btn-install">Скачать .jar</button>'
    else:
        install_btn = ''
        
    return f'''
    <div class="sidebar">
        <div class="logo-container">
            <img src="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png" alt="HK">
        </div>
        <a href="/" class="nav-item {'active' if active_page == 'home' else ''}">Главная</a>
        <a href="/favs" class="nav-item {'active' if active_page == 'favs' else ''}">Понравившееся</a>
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
            <h1>Главное меню</h1>
            <div class="grid">
                <a href="/wurst" class="card">
                    <h3>Wurst</h3>
                    <p>Удобный клиент для выживания с друзьями.</p>
                    <div class="card-footer"><span class="card-version">1.21.11</span></div>
                </a>
                <a href="/meteor" class="card">
                    <h3>Meteor Client</h3>
                    <p>Стабильная сборка для совместного фана.</p>
                    <div class="card-footer"><span class="card-version">1.21.11</span></div>
                </a>
            </div>
        </div>{SCRIPTS}</body></html>
    ''')

@app.route('/wurst')
def wurst_page():
    file_url = 'https://raw.githubusercontent.com/r1ze-r/HK/main/Wurst-Client1.21.11-hk.jar'
    return render_template_string(f'''
        <!DOCTYPE html><html><head><meta charset="UTF-8"><link rel="icon" href="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png"><title>HK - Wurst</title>{STYLE}</head>
        <body onload="loadHeartState('wurst')">{get_sidebar('wurst', file_url)}
        <div class="main"><div class="top-bar"><a href="/" class="btn-back-abs">← Назад на главную</a>
        <div class="heart-container"><button id="heart-wurst" class="heart-btn" onclick="toggleLike('wurst', 'Wurst')">❤</button></div>
        </div><h1>Wurst Client 1.21.11-hk</h1>
        <p style="color:var(--subtext); font-size:1.1rem; line-height:1.6;">Легендарная классика для Minecraft 1.21.11. Чистый софт без лишнего мусора.</p></div>{SCRIPTS}</body></html>
    ''')

@app.route('/meteor')
def meteor_page():
    file_url = 'https://raw.githubusercontent.com/r1ze-r/HK/main/meteor-client-1.21.11-hk.jar'
    return render_template_string(f'''
        <!DOCTYPE html><html><head><meta charset="UTF-8"><link rel="icon" href="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png"><title>HK - Meteor</title>{STYLE}</head>
        <body onload="loadHeartState('meteor')">{get_sidebar('meteor', file_url)}
        <div class="main"><div class="top-bar"><a href="/" class="btn-back-abs">← Назад на главную</a>
        <div class="heart-container"><button id="heart-meteor" class="heart-btn" onclick="toggleLike('meteor', 'Meteor Client')">❤</button></div>
        </div><h1>Meteor Client 1.21.11-hk</h1>
        <p style="color:var(--subtext); font-size:1.1rem; line-height:1.6;">Топовый чит для PVP и анархии. Версия HK оптимизирована для быстрой загрузки.</p></div>{SCRIPTS}</body></html>
    ''')

@app.route('/favs')
def favs_page():
    return render_template_string(f'''
        <!DOCTYPE html><html><head><meta charset="UTF-8"><link rel="icon" href="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png"><title>HK - Понравившееся</title>{STYLE}</head>
        <body>{get_sidebar('favs')}<div class="main"><h1>Понравившееся</h1><div id="favs-list" class="grid"></div></div>
        {SCRIPTS}
        <script>
            let favs = JSON.parse(localStorage.getItem('hk_favs') || '[]');
            let list = document.getElementById('favs-list');
            if (favs.length === 0) {{
                list.innerHTML = '<p style="color:var(--subtext);">Тут пока пусто. Добавь что-нибудь!</p>';
            }} else {{
                favs.forEach(item => {{
                    list.innerHTML += `<a href="/${{item.id}}" class="card"><h3>${{item.name}}</h3><p>Твой любимый чит всегда под рукой.</p></a>`;
                }});
            }}
        </script>
        </body></html>
    ''')

if __name__ == "__main__":
    app.run()
