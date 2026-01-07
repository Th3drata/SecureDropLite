import os
import sqlite3
import secrets
import time
import io
import socket
import base64
from flask import Flask, request, render_template, send_file, redirect, url_for, flash
from cryptography.fernet import Fernet
import qrcode

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
UPLOAD_FOLDER = '.secure'
DB_PATH = 'database.db'

def get_local_ip():
    """Obtient l'adresse IP locale du réseau"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'

def generate_qr_code(data):
    """Génère un QR code et le retourne en base64"""
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode()
    return img_base64

# Initialisation du dossier de stockage
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        # Créer la table si elle n'existe pas
        conn.execute('''CREATE TABLE IF NOT EXISTS files
                        (token TEXT PRIMARY KEY, filename_enc TEXT, key TEXT, expires_at INTEGER, 
                         max_downloads INTEGER DEFAULT 1, download_count INTEGER DEFAULT 0)''')
        
        # Vérifier et ajouter les colonnes manquantes si nécessaire
        cursor = conn.execute("PRAGMA table_info(files)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'max_downloads' not in columns:
            conn.execute('ALTER TABLE files ADD COLUMN max_downloads INTEGER DEFAULT 1')
        
        if 'download_count' not in columns:
            conn.execute('ALTER TABLE files ADD COLUMN download_count INTEGER DEFAULT 0')
        
        conn.commit()
init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            flash('Aucun fichier sélectionné.', 'danger')
            return redirect(url_for('index'))
        
        # Récupération des paramètres avec valeurs par défaut
        expiration_minutes = int(request.form.get('expiration', 10))
        max_downloads = int(request.form.get('max_downloads', 1))
        
        # Validation des paramètres
        if expiration_minutes < 1 or expiration_minutes > 1440:  # Max 24h
            flash('La durée d\'expiration doit être entre 1 et 1440 minutes.', 'danger')
            return redirect(url_for('index'))
        if max_downloads < 1 or max_downloads > 100:
            flash('Le nombre d\'utilisations doit être entre 1 et 100.', 'danger')
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
        expires_at = int(time.time()) + (expiration_minutes * 60)
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                'INSERT INTO files (token, filename_enc, key, expires_at, max_downloads, download_count) VALUES (?, ?, ?, ?, ?, ?)',
                (token, filename_enc, key.decode(), expires_at, max_downloads, 0)
            )
        local_ip = get_local_ip()
        download_link = f"http://{local_ip}:5001/download/{token}"
        qr_code = generate_qr_code(download_link)
        return render_template('link.html', link=download_link, key=key.decode(), expires=expiration_minutes, qr_code=qr_code, max_downloads=max_downloads)
    return render_template('index.html')

@app.route('/download/<token>', methods=['GET', 'POST'])
def download(token):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute('SELECT filename_enc, key, expires_at, max_downloads, download_count FROM files WHERE token=?', (token,))
        row = cur.fetchone()
        if not row:
            return render_template('download.html', error="Lien invalide ou expiré."), 410
        filename_enc, key_db, expires_at, max_downloads, download_count = row
        
        # Vérifier si le lien est expiré
        if int(time.time()) > expires_at:
            path = os.path.join(UPLOAD_FOLDER, token)
            if os.path.exists(path):
                os.remove(path)
            conn.execute('DELETE FROM files WHERE token=?', (token,))
            return render_template('download.html', error="Lien expiré."), 410
        
        # Vérifier si le nombre max de téléchargements est atteint
        if download_count >= max_downloads:
            path = os.path.join(UPLOAD_FOLDER, token)
            if os.path.exists(path):
                os.remove(path)
            conn.execute('DELETE FROM files WHERE token=?', (token,))
            return render_template('download.html', error="Nombre maximum de téléchargements atteint."), 410
        
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
            
            # Incrémenter le compteur de téléchargements
            new_count = download_count + 1
            conn.execute('UPDATE files SET download_count=? WHERE token=?', (new_count, token))
            
            # Si c'était le dernier téléchargement autorisé, supprimer le fichier
            if new_count >= max_downloads:
                os.remove(path)
                conn.execute('DELETE FROM files WHERE token=?', (token,))
            
            return send_file(
                io.BytesIO(data),
                as_attachment=True,
                download_name=filename
            )
        
        # Afficher les infos sur le nombre de téléchargements restants
        remaining = max_downloads - download_count
        return render_template('download.html', error=None, remaining=remaining, max_downloads=max_downloads)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 