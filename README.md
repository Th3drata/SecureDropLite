<!-- Main Banner -->
<p align="center">
  <img src="https://img.shields.io/badge/Flask-2.3.2-blue?logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Cryptography-41.0.3-green?logo=lock" alt="Cryptography">
</p>

<h1 align="center">🔒 SecureDropLite</h1>

<p align="center">
  <b>Share your files in an ultra-secure, temporary, and anonymous way.</b><br>
  <i>Encryption, self-destruction, simplicity.</i>
</p>

---

## 🚀 Overview

SecureDropLite is a web application that allows you to share files securely. Files are encrypted server-side, accessible via a unique link, and self-destruct after download or expiration.

---

## 🖼️ Visual Preview

<p align="center">
  <!-- Replace the links below with your own images/screenshots -->
  <img src="https://github.com/Th3drata/SecureDropLite/blob/main/Send.png" alt="Preview 1" width="400"/>
  <img src="https://github.com/Th3drata/SecureDropLite/blob/main/Upload.png" alt="Preview 2" width="400"/>
</p>

---

## 🛠️ Technologies Used

- <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python" alt="Python" height="20"> Python 3
- <img src="https://img.shields.io/badge/Flask-2.3.2-blue?logo=flask" alt="Flask" height="20"> Flask
- <img src="https://img.shields.io/badge/Cryptography-41.0.3-green?logo=lock" alt="Cryptography" height="20"> cryptography
- <img src="https://img.shields.io/badge/SQLite-DB-lightgrey?logo=sqlite" alt="SQLite" height="20"> SQLite
- <img src="https://img.shields.io/badge/Bootstrap-5.3.0-purple?logo=bootstrap" alt="Bootstrap" height="20"> Bootstrap (UI)

---

## ⚡ Main Features

- 🔐 Strong file encryption (Fernet/AES)
- ⏳ Temporary link (10 minutes)
- 💣 Self-destruction after download or expiration
- 🗝️ Separate decryption key
- 🌑 Built-in dark mode

---

## 🚩 Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the application**:
   ```bash
   python app.py
   ```
3. **Access the interface**:
   Open [http://localhost:5000](http://localhost:5000) in your browser.
   
   > The app now listens on `0.0.0.0`, so you can also access it from other devices on your local network using your computer's IP address (e.g., `http://YOUR_IP:5000`).

---

## 📂 Project Structure

```
SecureDropLite/
├── app.py                # Main Flask application
├── requirements.txt      # Python dependencies
├── database.db           # SQLite database
└── templates/            # HTML templates (Bootstrap, dark mode)
```

## 🙏 Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [cryptography](https://cryptography.io/)
- [Bootstrap](https://getbootstrap.com/)


<p align="center">
  <b>Project by th3drata - 2025</b>
</p> 
