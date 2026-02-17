# ♟️ AI Chess Arena

<div align="center">

![AI Chess](https://img.shields.io/badge/AI%20Chess-Groq%20Powered-blueviolet?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![Groq](https://img.shields.io/badge/Groq-Llama%203.3-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**AI vs AI Chess Game - Watch AI Agents Battle**

[Live Demo](https://ai-chessagent.streamlit.app/) • [Report Bug](https://github.com/KanavChauhan23/ai-chess-arena/issues)

*Groq AI • Free to Use • Real-Time Chess*

</div>

---

## 🌟 Overview

**AI Chess Arena** is an interactive chess game where two AI agents powered by **Groq's Llama 3.3** play against each other. Watch as AI battles AI in strategic chess gameplay with beautiful real-time visualization!

### Why AI Chess Arena?

- 🤖 **Dual AI Agents** - Two independent AI players competing
- ⚡ **Groq Powered** - Lightning-fast inference with Llama 3.3 70B
- ♟️ **Full Chess Rules** - Complete chess implementation
- 🆓 **100% Free** - No user API key needed!
- 📊 **Real-Time Visualization** - Watch every move as it happens
- 🎮 **Interactive** - Control game length and settings

---

## ✨ Features

### 🤖 AI vs AI Battle

**Two AI Agents:**

1. **Agent White** ⚪
   - Controls white pieces
   - Aggressive, attacking strategy
   - Powered by Groq Llama 3.3
   - Independent decision-making

2. **Agent Black** ⚫
   - Controls black pieces
   - Defensive, counter-attacking strategy
   - Powered by Groq Llama 3.3
   - Strategic positioning

### ♟️ Complete Chess

- ✅ All standard chess rules
- ✅ Move validation
- ✅ Check/Checkmate detection
- ✅ Stalemate handling
- ✅ Draw conditions
- ✅ Legal move generation

### 📊 Visualization

- Beautiful SVG board rendering
- Move arrows and highlights
- Complete move history
- Real-time game log
- Progress tracking

---

## 🚀 Live Demo

**Try it now:** [Live](https://ai-chessagent.streamlit.app/)

### Quick Start

1. Visit the app (no signup needed!)
2. Set number of moves (5-30)
3. Click "Start New Game"
4. Watch AI agents play!

**No API key required!** 🎉

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Groq** | AI inference (Llama 3.3 70B) |
| **Python-Chess** | Chess engine & rules |
| **Streamlit** | Web interface |
| **CairoSVG** | Board visualization |

---

## 💻 Installation

### Prerequisites

- Python 3.9+
- Groq API key ([Get free key](https://console.groq.com/))

### Local Setup

1. **Clone repository**
   ```bash
   git clone https://github.com/KanavChauhan23/ai-chess-arena.git
   cd ai-chess-arena
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Groq API key**
   
   Create `.streamlit/secrets.toml`:
   ```toml
   GROQ_API_KEY = "your-groq-api-key-here"
   ```

4. **Run application**
   ```bash
   streamlit run app.py
   ```

5. **Open browser**
   ```
   http://localhost:8501
   ```

---

## 🎯 How It Works

### Game Flow

```
Start Game
    ↓
Agent White analyzes board
    ↓
Groq AI chooses best move
    ↓
Move executed & validated
    ↓
Agent Black's turn
    ↓
Repeat until game ends
```

### AI Decision Making

1. **Position Analysis**
   - AI receives current board state (FEN)
   - Gets list of legal moves
   - Analyzes position strategically

2. **Move Selection**
   - Groq Llama 3.3 evaluates options
   - Considers piece safety, center control
   - Makes strategic decision

3. **Execution**
   - Move validated against chess rules
   - Board updated
   - Visualization generated

---

## 📊 Performance

**Using Groq (Free Tier):**
- **Speed:** ~1-2 seconds per move
- **Cost:** 100% FREE!
- **Quality:** GPT-4 level reasoning
- **Reliability:** High uptime

**Game Durations:**
- 5 moves: ~10-15 seconds
- 10 moves: ~20-30 seconds
- 30 moves: ~1-2 minutes

---

## 🎮 Use Cases

### For AI Enthusiasts
- Watch AI strategic thinking
- See different playing styles
- Learn chess tactics

### For Developers
- Learn Groq integration
- Chess AI implementation
- Real-time game visualization

### For Fun
- AI vs AI entertainment
- Unpredictable games
- No chess knowledge needed!

---

## 🚀 Deployment

### Streamlit Cloud

1. Push code to GitHub
2. Connect to [share.streamlit.io](https://share.streamlit.io)
3. Add `GROQ_API_KEY` in secrets
4. Deploy!

**That's it!** Users can play without their own API keys.

---

## 🤝 Contributing

Contributions welcome!

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open Pull Request

### Ideas

- [ ] Different AI difficulty levels
- [ ] Save/load games
- [ ] Move commentary
- [ ] Opening book integration
- [ ] Game analysis
- [ ] PGN export

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

## 👨‍💻 Author

**Kanav Chauhan**

- GitHub: [@KanavChauhan23](https://github.com/KanavChauhan23)
- LinkedIn: [Kanav Chauhan](https://linkedin.com/in/kanavchauhan23)

---

## 🙏 Acknowledgments

- **Groq** for lightning-fast AI inference
- **Python-Chess** for the chess engine
- **Streamlit** for the beautiful framework

---

## 💡 Why Groq?

**Groq vs OpenAI for Chess:**

| Feature | Groq | OpenAI |
|---------|------|--------|
| **Speed** | ⚡ Ultra-fast | Slower |
| **Cost** | 🆓 Free! | Paid |
| **Quality** | Excellent | Excellent |
| **Rate Limits** | Generous | Strict |
| **Setup** | Simple | Complex billing |

**Perfect for chess AI!** ♟️

---

<div align="center">

**Made with ❤️ by Kanav Chauhan**

Give it a ⭐ if you enjoyed watching AI play chess!

[⬆ Back to Top](#-ai-chess-arena)

</div>
