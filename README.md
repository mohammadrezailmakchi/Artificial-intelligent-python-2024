# 🧠 Artificial Intelligent – Python – 2024

📄 [نسخه فارسی README_FA.md](./README_FA.md)  
> A historical AI desktop assistant project built in early 2024 as a showcase for the Khwarizmi Festival — demonstrating my knowledge of APIs, GUI design, and Python programming at the time.

> 📝 Note: The HTML templates in the `docs/` folder were originally designed by [HTML5 UP](https://html5up.net/)

---

## 📜 Overview

This project was built in **Farvardin 1403 (March–April 2024)** using **Python 3.10.6** and is my **first complete and official AI application** — polished, packaged, and documented entirely by myself (aside from open-source libraries and some help from a friend on code comments).

It represents a **snapshot of my development skills in 2024**, and although it's no longer being actively updated, it stands as a historical project meant to showcase:
- My technical level during those years
- My passion for AI development
- The earlier structure of OpenAI’s API integrations

---

## 🚀 Features

- 🎙️ Voice-to-text input (OpenAI Whisper)
- 🧠 Chat with GPT-3.5/4 via OpenAI API
- 🖼️ DALL·E 3 image generation
- 🔊 AI-powered TTS (Text-to-Speech)
- 🪟 Custom GUI using `customtkinter`
- 🎵 Sound playback with `pygame` & `sounddevice`
- 📋 Clipboard, tooltips, styled windows
- ✨ All code in a single file: `main.py`

> ⚠️ This app is **not modularized** and is intentionally kept as it was in 2024 to preserve its educational value.

---

## 💾 Installation & Usage

### 1. Clone the repo

```bash
git clone https://github.com/mohammadrezailmakchi/Artificial-intelligent-python-2024.git
cd Artificial-intelligent-python-2024
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate.bat
```

Or use the provided batch script:

```bash
RunClient.bat
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Add your OpenAI API key

Create a `.env` file in the root folder:

```
OPENAI_API_KEY=your-api-key-here
```

> You can copy the `.env.example` file and rename it to `.env`.

### 5. Run the app

```bash
python main.py
```

---

## ⚙️ Tech Stack

- **Python 3.10.6**
- `customtkinter`, `pygame`, `sounddevice`, `pydub`, `dotenv`
- **OpenAI API** (ChatGPT, Whisper, DALL·E, TTS)

---

## 💻 Platform Compatibility

This project is currently built and tested for:

- ✅ **Windows 10/11**

However, since it’s written in **pure Python**, with some adjustments (e.g., modifying batch scripts and ensuring library compatibility), it can be adapted for other platforms like **macOS** or **Linux**.

---

## 🏛 Historical Context

> This project is not intended for production or active use.

It is uploaded as a **personal and historical record** of how I developed AI applications in 2024. Since then, my skills have advanced, and I'm currently working on newer, modular, and production-ready versions of this concept — to be released in the future.

Still, this code serves as:
- An educational reference
- A real-world showcase of OpenAI API usage (from earlier SDK versions)
- A personal archive of how I built my first complete app 💪

---

## 🤝 Credits

- Developed by **Mohammadreza Ilmakchi**  
- Special thanks to my friend who helped with code comments  
- Powered by open-source libraries and the OpenAI API  
- HTML templates from [HTML5 UP](https://html5up.net/)

---

## 🔐 License

This project is licensed under the [MIT License](LICENSE).

---

> ⚡ Follow the journey: [github.com/mohammadrezailmakchi](https://github.com/mohammadrezailmakchi)
