---
title: AI Digital Life Simulator 🧬
emoji: 🧬
colorFrom: indigo
colorTo: purple
sdk: streamlit
sdk_version: 1.30.0
app_file: app.py
pinned: false
---

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-1.30+-red?style=for-the-badge&logo=streamlit" alt="Streamlit">
  <img src="https://img.shields.io/badge/OpenEnv-Compatible-green?style=for-the-badge" alt="OpenEnv">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">
</p>

<h1 align="center">🧬 AI Digital Life Simulator</h1>

<p align="center">
  <strong>A reinforcement-learning environment that simulates real-world human life decisions.</strong><br>
  Balance health, career, relationships, finances, and stress — how well can you live?
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#how-it-works">How It Works</a> •
  <a href="#example-output">Example Output</a> •
  <a href="#deployment">Deployment</a>
</p>

---

## 🧩 Problem Statement

Real-life decisions are interconnected — working overtime earns money but costs health and relationships. Traditional RL environments rarely capture this **multidimensional trade-off**. The AI Digital Life Simulator acts as a **Personal Resource Allocation Optimizer** where an AI agent must learn to balance competing priorities across 3 distinct tasks (Wealth, Career, and Balance) to achieve a fulfilling life, strictly adhering to the OpenEnv specification.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎯 **OpenEnv Compatible** | Standard `reset()` / `step()` / `state()` interface |
| 🧠 **6 Actions** | Work, Exercise, Invest, Learn, Socialize, Rest |
| 📊 **7 State Variables** | Age, Health, Money, Stress, Career, Relationships, Happiness |
| 🏆 **3 Distinct Tasks** | Wealth Builder (Easy), Career Climber (Medium), Perfect Balance (Hard) |
| 🎭 **5 Personality Modes** | Risk Taker, Conservative, Lazy, Ambitious, Balanced |
| 🌪️ **8 Random Events** | Promotions, layoffs, emergencies, market crashes, and more |
| ⏱️ **Time Progression** | Aging, health decay, delayed investment returns |
| 🎚️ **3 Difficulty Levels** | Easy, Medium, Hard with increasing complexity |
| 🏆 **Agent Grading** | 0.0–1.0 normalized life-quality score |
| 🤖 **Baseline Agent** | Rule-based AI with decision explanations |
| 🎨 **Stunning Dashboard** | Glassmorphism UI with dark/light mode, Plotly charts |
| 🚀 **One-Command Deploy** | Docker + Hugging Face Spaces ready |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        app.py (UI)                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────────┐  │
│  │ Metrics  │ │ Timeline │ │  Events  │ │ AI Decisions  │  │
│  │  Cards   │ │  Chart   │ │   Feed   │ │    Panel      │  │
│  └──────────┘ └──────────┘ └──────────┘ └───────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                      env.py (Core)                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────────┐  │
│  │  State   │ │  Reward  │ │   Time   │ │  Difficulty   │  │
│  │  Engine  │ │  System  │ │  System  │ │   Config      │  │
│  └──────────┘ └──────────┘ └──────────┘ └───────────────┘  │
├──────────┬──────────┬──────────┬──────────┬─────────────────┤
│models.py │events.py │person-   │grader.py │   agent.py      │
│  Enums   │ Dynamic  │alities  │ Scoring  │  Rule-Based     │
│  Types   │ Events   │  .py    │ Grades   │  Baseline       │
├──────────┴──────────┴──────────┴──────────┴─────────────────┤
│                     utils.py (Helpers)                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/ai-digital-life-simulator.git
cd ai-digital-life-simulator

# Install dependencies
pip install -r requirements.txt
```

### Run the Dashboard

```bash
# From the project root
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

### Run the Baseline Agent (Terminal)

```bash
python agent.py
```

---

## 🎮 How It Works

### Actions & Effects

Each action affects multiple life dimensions, creating realistic trade-offs:

| Action | 💰 Money | ❤️ Health | 😰 Stress | 💼 Career | 👥 Social | 😊 Happy |
|--------|---------|---------|---------|---------|---------|---------|
| Work Overtime | +120 | -3 | +12 | +4 | -2 | -4 |
| Exercise | -10 | +8 | -8 | — | +1 | +5 |
| Invest Money | ±var | — | +4 | +1 | -1 | — |
| Learn Skill | -30 | -1 | +5 | +7 | -1 | +3 |
| Socialize | -40 | +1 | -5 | +1 | +10 | +8 |
| Rest | -5 | +5 | -12 | -1 | +2 | +4 |

### Reward System

The reward function encourages **balanced living**, not extreme min-maxing:

1. **Weighted Score** — Health (25%), Career (20%), Relationships (20%), Money (15%), Low Stress (20%)
2. **Imbalance Penalty** — Standard deviation penalty across dimensions
3. **Consistency Bonus** — Sustained balance over 5 consecutive steps
4. **Burnout Penalty** — Escalating penalty for chronic high stress

### Random Events

Probabilistic life events that affect multiple variables:

| Event | Probability | Key Effects |
|-------|------------|-------------|
| 🎉 Job Promotion | 6% | Career +15, Money +300 |
| 😰 Job Loss | 4% | Career -20, Stress +20 |
| 🏥 Medical Emergency | 5% | Health -25, Money -500 |
| 📉 Market Crash | 4% | Money -400, Stress +15 |
| 👨‍👩‍👧 Family Issue | 6% | Relationships -15, Stress +12 |
| 🎰 Lottery Win | 2% | Money +800, Happiness +15 |
| 🌪️ Natural Disaster | 3% | Health -10, Money -300 |
| 💰 Inheritance | 2% | Money +1000, Relationships +5 |

### Termination Conditions

- ❌ Health reaches 0 (death)
- ❌ Stress reaches 100 (total burnout)
- ✅ Maximum steps reached (simulation ends)

---

## 📊 Example Output

```
============================================================
  🧬  AI DIGITAL LIFE SIMULATOR  —  Baseline Agent Run
============================================================
  Personality : balanced
  Difficulty  : medium
  Max Steps   : 100
============================================================

─── Step 100  | Week 100 | Age 26.9 ───
  Health         |██████████████████████████▒▒▒▒|   87.4 / 100
  Money          |████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒| 1647.6 / 10000
  Stress         |███████████████████████▒▒▒▒▒▒▒|   78.0 / 100
  Career         |████████████████████████▒▒▒▒▒▒|   82.3 / 100

============================================================
  📊  FINAL RESULTS
============================================================
  Total Steps     : 100
  Total Reward    : +40.9853
  Final Grade     : 0.4629
  Assessment      : ⚠️ Average — Room for Improvement
============================================================
```

---

## 🐳 Deployment

### Docker

```bash
# From the project root
docker build -t life-sim .
docker run -p 8501:8501 life-sim
```

### Hugging Face Spaces

1. Create a new Space on [huggingface.co/spaces](https://huggingface.co/spaces)
2. Select **Streamlit** as the SDK
3. Upload all project files (ensure `app.py` is in the root)
4. The Space will automatically build and deploy using the metadata provided in this README.

---

## 📂 Project Structure

```
OpenEnv_Soln/
├── app.py              # Streamlit UI dashboard
├── env.py              # Core environment (reset/step/state)
├── models.py           # Data models, enums, dataclasses
├── utils.py            # Utility functions
├── events.py           # Dynamic random events system
├── personalities.py    # Personality modifier profiles
├── grader.py           # Agent grading (0.0–1.0)
├── agent.py            # Baseline rule-based AI agent
├── openenv.yaml        # OpenEnv specification
├── style.css           # Glassmorphism CSS theme
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker deployment
├── README.md           # This file
└── .streamlit/
    └── config.toml     # Streamlit server config
```

---

## 🛠️ Tech Stack

- **Python 3.11** — Core language
- **Streamlit** — Interactive web dashboard
- **Plotly** — Beautiful interactive charts
- **CSS3** — Glassmorphism, animations, theming
- **Docker** — Containerized deployment

---

## 📄 License

MIT License — See [LICENSE](LICENSE) for details.

---

<p align="center">
  Built with ❤️ for the Hackathon<br>
  <strong>AI Digital Life Simulator</strong> — Navigate life's decisions. Balance your destiny.
</p>
