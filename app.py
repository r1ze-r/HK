from flask import Flask, render_template, render_template_string, jsonify
import json

app = Flask(__name__)

[project.scripts]
app = "app:app"

# --- CONFIG DATA (Твоя база, где ты сам добавляешь читы) ---
DATABASE = {
    'wurst': {
        'name': 'Wurst Client',
        'desc': 'Король выживания. Включает в себя более 150 модулей: от AutoMine до KillAura. Идеально сбалансирован для игры на серверах без жесткого античита.',
        'ver': '1.21.11',
        'tags': ['Survival', 'Utility', 'Classic', 'Cheat'],
        'color': '#ff4444',
        'file_url': 'https://raw.githubusercontent.com/r1ze-r/HK/main/Wurst-Client1.21.11-hk.jar'
    },
    'xray': {
        'name': 'X-Ray Ultimate',
        'desc': 'Тот самый легендарный ресурспак. Подсвечивает руды и упрощает поиск алмазов. Идеально для тех, кто хочет результат без установки тяжелых читов.',
        'ver': '1.21',
        'tags': ['Resourcepack', 'Survival', 'Popular'],
        'color': '#ffffff',
        'file_url': 'https://raw.githubusercontent.com/r1ze-r/HK/main/Xray_Ultimate_1.21_v5.3.1.zip'
    },
    'coffee': {
        'name': 'Coffee Client',
        'desc': 'Любишь кофе? Тогда этот чит для тебя. Лучший дизайн, много функций и многое другое.',
        'ver': '1.20.1',
        'tags': ['Resourcepack', 'Survival', 'Popular'],
        'color': '#ffffff',
        'file_url': 'https://raw.githubusercontent.com/r1ze-r/HK/main/freecam-fabric1.21.11.jar'
    },
     'freecam': {
        'name': 'freecam',
        'desc': 'Этот мод тебе позволяет летать! (но только визуал) хорошо подойдет для просмотра вражеских баз',
        'ver': '1.21.11',
        'tags': ['Resourcepack', 'Survival', 'Popular'],
        'color': '#ffffff',
        'file_url': 'https://raw.githubusercontent.com/r1ze-r/HK/main/Coffee-Client-Fabric-1.20.1.jar'
    },
    'meteor': {
        'name': 'Meteor Client',
        'desc': 'Ультимативное решение для PVP и анархии. Гибкая настройка HUD и мощная система макросов.',
        'ver': '1.21.11',
        'tags': ['Anarchy', 'PVP', 'Cheat'],
        'color': '#2ecc71',
        'file_url': 'https://raw.githubusercontent.com/r1ze-r/HK/main/meteor-client-1.21.1-hk.jar'
    }
}





def get_nav(page):
    return f'''
    <nav style="display: flex; justify-content: center; align-items: center; padding: 20px 50px; position: relative;">
        <a href="/" style="display: flex; align-items: center; text-decoration: none; color: white;">
            <img src="/static/HK.png" style="height: 50px; width: auto; border-radius: 8px;">
            <span style="margin-left: 15px; font-size: 1.8rem; font-weight: 900; letter-spacing: -1px;">HK HUB</span>

@app.route('/')
def home():
    cards_html = ""
    for key, val in DATABASE.items():
        tags = "".join([f'<span class="tag">{t}</span>' for t in val['tags']])
        cards_html += f'''
        <div class="cheat-card" onclick="window.location.href='/cheat/{key}'">
            <div class="tag-container">{tags}</div>
            <h3>{val['name']}</h3>
            <p style="color:var(--text-dim); margin-bottom:20px;">{val['desc']}</p>
            <div class="card-meta">
                <span class="version-tag">{val['ver']}</span>
                <button class="heart-btn" data-id="{key}" onclick="event.stopPropagation(); updateFavs('{key}', '{val['name']}')">❤</button>
            </div>
        </div>'''
    
    return render_template_string(f'''
    <html><head>{STYLE}</head><body>
        <div class="bg-glow"></div>
        {get_nav("home")}
        <div class="tg-anchor"><a href="https://t.me/hellokilaura" class="tg-btn">Telegram</a></div>
        <div class="container">
            <div class="hero">
                
                <h1>Каталог HK Hub</h1>
                <div class="search-wrapper">
                    <input type="text" id="mainSearch" class="search-input" onkeyup="search()" placeholder="Поиск читов...">
                </div>
            </div>
            <div class="cheat-grid">{cards_html}</div>
        </div>
        {SCRIPTS}
    </body></html>''')

@app.route('/favs')
def favs():
    import json
    db_json = json.dumps(DATABASE)
    
    return render_template_string(f'''
    <html><head>{STYLE}</head><body>
        <div class="bg-glow"></div>
        {get_nav("favs")}
        <div class="container">
            <h1 style="text-align:center; margin: 40px 0;">Понравившееся</h1>
            <div id="favs-list" class="cheat-grid">
                </div>
        </div>
        {SCRIPTS}
        <script>
            document.addEventListener('DOMContentLoaded', () => {{
                // Используем ключ hk_v3_favs, как в твоих основных скриптах
                const favs = JSON.parse(localStorage.getItem('hk_v3_favs') || '[]');
                const container = document.getElementById('favs-list');
                const db = {db_json};

                if (favs.length === 0) {{
                    container.innerHTML = '<p style="grid-column: 1/-1; text-align:center; opacity:0.5; font-size:1.5rem; margin-top:50px;">Тут пока пусто... Добавьте что-нибудь!</p>';
                    return;
                }}

                let html = '';
                favs.forEach(fav => {{
                    const item = db[fav.id];
                    if (!item) return;

                    // Верстка карточки 1 в 1 как на главной, с твоими классами
                    html += `
                    <div class="cheat-card" onclick="window.location.href='/cheat/${{fav.id}}'">
                        <div class="tag-container">
                            ${{item.tags.map(t => `<span class="tag">${{t}}</span>`).join('')}}
                        </div>
                        <h3>${{item.name}}</h3>
                        <p style="color:var(--text-dim); margin-bottom:20px;">${{item.desc}}</p>
                        <div class="card-meta">
                            <span class="version-tag">${{item.ver}}</span>
                            <button class="heart-btn liked" data-id="${{fav.id}}" onclick="event.stopPropagation(); updateFavs('${{fav.id}}', '${{item.name}}'); location.reload();">❤</button>
                        </div>
                    </div>`;
                }});
                container.innerHTML = html;
            }});
        </script>
    </body></html>''')
    
@app.route('/cheat/<id>')
def detail(id):
    item = DATABASE.get(id)
    if not item: return "404", 404
    
   # Видео будет одно для всех, как ты и просил
    video_file = "2026-02-16-22-54-44.mp4" 

    return render_template_string(f'''
    <html><head>{STYLE}</head><body>
        <div class="bg-glow"></div>
        {get_nav("detail")}
        <div class="container" style="padding-top: 20px;">
            <div class="detail-view" style="display: flex; flex-direction: column; align-items: center; gap: 20px;">
                <div style="width: 100%; display: flex; justify-content: space-between; align-items: center;">
                    <a href="/" style="color:var(--accent); text-decoration:none; font-weight:900;">← Назад</a>
                    <button class="heart-btn" data-id="{id}" onclick="updateFavs('{id}', '{item['name']}')">❤</button>
                </div>

                <h1 style="font-size:3rem; margin:0;">{item['name']}</h1>

                <div class="dl-section" style="padding: 25px; display: flex; flex-direction: column; align-items: center; gap: 20px; width: 100%;">
                    <span class="version-tag">Версия: {item['ver']}</span>
                    <p style="font-size:1.1rem; color:#ccc; text-align:center; margin:0;">{item['desc']}</p>
                    
                    <button onclick="forceDownload('{item['file_url']}', '{item['name']}')" class="big-dl-btn">СКАЧАТЬ ОТ HK</button>

                    <div style="width: 100%; max-width: 400px; border-radius: 15px; overflow: hidden; border: 1px solid var(--card-border); margin-top: 10px;">
                        <video width="100%" height="auto" controls style="display: block;">
                            <source src="/static/{video_file}" type="video/mp4">
                            Браузер не тянет видео
                        </video>
                    </div>
                </div>
            </div>
        </div>
        {SCRIPTS}
    </body></html>''')

if __name__ == "__main__":
    
    
