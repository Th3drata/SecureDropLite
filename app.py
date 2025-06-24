import os
import sqlite3
import secrets
import time
import io
from flask import Flask, request, render_template, send_file, redirect, url_for, flash
from cryptography.fernet import Fernet

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
UPLOAD_FOLDER = '.secure'
DB_PATH = 'database.db'

# Initialisation du dossier de stockage
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS files
                        (token TEXT PRIMARY KEY, filename_enc TEXT, key TEXT, expires_at INTEGER, downloaded INTEGER DEFAULT 0)''')
init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            flash('Aucun fichier sélectionné.', 'danger')
            return redirect(url_for('index'))
        key = Fernet.generate_key()
        f = Fernet(key)
        data = file.read()
        filename_enc = f.encrypt(file.filename.encode()).decode()
        file_enc = f.encrypt(data)
        token = secrets.token_urlsafe(16)
        path = os.path.join(UPLOAD_FOLDER, token)
        with open(path, 'wb') as out:
            out.write(file_enc)
        expires_at = int(time.time()) + 600  # 10 min
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                'INSERT INTO files (token, filename_enc, key, expires_at, downloaded) VALUES (?, ?, ?, ?, ?)',
                (token, filename_enc, key.decode(), expires_at, 0)
            )
        return render_template('link.html', link=url_for('download', token=token, _external=True), key=key.decode(), expires=10)
    return render_template('index.html')

@app.route('/download/<token>', methods=['GET', 'POST'])
def download(token):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute('SELECT filename_enc, key, expires_at, downloaded FROM files WHERE token=?', (token,))
        row = cur.fetchone()
        if not row:
            return render_template('download.html', error="Lien invalide ou expiré."), 410
        filename_enc, key_db, expires_at, downloaded = row
        if int(time.time()) > expires_at or downloaded:
            # Auto-destruction si expiré ou déjà téléchargé
            path = os.path.join(UPLOAD_FOLDER, token)
            if os.path.exists(path):
                os.remove(path)
            conn.execute('DELETE FROM files WHERE token=?', (token,))
            return render_template('download.html', error="Lien expiré ou déjà utilisé."), 410
        if request.method == 'POST':
            key = request.form['key'].encode()
            try:
                f = Fernet(key)
                path = os.path.join(UPLOAD_FOLDER, token)
                with open(path, 'rb') as inp:
                    file_enc = inp.read()
                filename = f.decrypt(filename_enc.encode()).decode()
                data = f.decrypt(file_enc)
            except Exception:
                return render_template('download.html', error="Clé invalide ou fichier corrompu."), 400
            # Marquer comme téléchargé et supprimer le fichier (auto-destruction)
            conn.execute('UPDATE files SET downloaded=1 WHERE token=?', (token,))
            os.remove(path)
            return send_file(
                io.BytesIO(data),
                as_attachment=True,
                download_name=filename
            )
        return render_template('download.html', error=None)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') 