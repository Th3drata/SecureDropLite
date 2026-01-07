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
- <img src="https://img.shields.io/badge/QRCode-7.4.2-orange?logo=qrcode" alt="QRCode" height="20"> qrcode
- <img src="https://img.shields.io/badge/Bootstrap-5.3.0-purple?logo=bootstrap" alt="Bootstrap" height="20"> Bootstrap (UI)

---

## ⚡ Main Features

- 🔐 Strong file encryption (Fernet/AES)
- ⏳ Configurable link expiration (1-1440 minutes)
- 🔢 Configurable maximum downloads (1-100)
- 💣 Self-destruction after downloads limit or expiration
- 🗝️ Separate decryption key
- 📱 Automatic QR code generation for easy sharing
- 🌑 Built-in dark mode
- 🌐 Local network access support

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
   Open [http://localhost:5001](http://localhost:5001) in your browser.

   > The app listens on `0.0.0.0:5001`, so you can also access it from other devices on your local network using your computer's IP address (e.g., `http://YOUR_IP:5001`).

---

## � How to Use

1. **Upload a file**: Select the file you want to share
2. **Configure parameters**:
   - **Link expiration**: Set how long the link will remain valid (1-1440 minutes)
   - **Maximum downloads**: Choose how many times the file can be downloaded (1-100)
3. **Generate link**: Click "Encrypt & Generate Link"
4. **Share the link**: Send the download link to your recipient
5. **Share the key separately**: Send the decryption key through a different channel (SMS, phone call, etc.)
6. **QR Code**: Use the automatically generated QR code for quick sharing on mobile devices

> 🔒 **Security Tip**: Always send the decryption key separately from the download link to maximize security.

---

## �📂 Project Structure

```
SecureDropLite/
├── app.py                # Main Flask application
├── requirements.txt      # Python dependencies
├── database.db           # SQLite database (auto-generated)
├── .secure/              # Encrypted files storage (auto-generated)
└── templates/            # HTML templates (Bootstrap, dark mode)
    ├── index.html        # Upload page
    ├── link.html         # Generated link page with QR code
    └── download.html     # Download page
```

## 🙏 Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [cryptography](https://cryptography.io/)
- [Bootstrap](https://getbootstrap.com/)

<p align="center">
  <b>Project by th3drata - 2025</b>
</p>
