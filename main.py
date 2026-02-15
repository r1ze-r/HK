from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string('''
        <body style="background-color: #000; color: white; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; font-family: sans-serif; margin: 0;">
            <img src="https://raw.githubusercontent.com/r1ze-r/HK/main/HK.png" style="width: 300px; filter: drop-shadow(0 0 20px red);">
            <h1 style="margin-top: 20px; font-size: 3rem; letter-spacing: -2px;">HelloKilaura (HK)</h1>
            <p style="color: #666; font-size: 1.2rem;">The лютейшая имба is coming soon...</p>
        </body>
    ''')

if __name__ == "__main__":
    app.run()
