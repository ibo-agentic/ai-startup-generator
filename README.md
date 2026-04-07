# AI Startup Idea Generator

An AI system that generates startup ideas using 4 collaborative agents built with CrewAI and Gradio.

---

## What it does

- Generates 3 startup ideas based on your interests
- Researches market size, competitors, and trends for each idea
- Builds a business strategy with revenue model and go-to-market plan
- Writes a full investor pitch in natural human voice
- Conversation memory — follow up with "make it low-cost" or "make the pitch more aggressive"

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| CrewAI | Multi-agent framework |
| Groq API (Llama 3.3 70B) | LLM backend |
| Gradio | Web UI |
| Python | Core logic |

---

## Agents

| Agent | Role |
|-------|------|
| Idea Generator | Creates 3 startup ideas |
| Market Researcher | Analyzes market, competitors, risks |
| Business Strategist | Revenue model, GTM plan, roadmap |
| Pitch Creator | Writes the investor pitch |

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/ibo-agentic/ai-startup-generator.git
cd ai-startup-generator
```

**2. Install dependencies**
```bash
pip install crewai gradio python-dotenv
```

**3. Add your Groq API key**

Create a `.env` file:

GROQ_API_KEY=your_key_here

Get a free key at [console.groq.com](https://console.groq.com)

**4. Run the app**
```bash
python crewai_project.py
```

Open `http://127.0.0.1:7860` in your browser.

---

## How to use

1. Describe your interests or industry in the text box
2. Click **Generate My Startup**
3. Wait for all 4 agents to finish
4. Read the pitch cards on the right
5. Ask follow-up questions in the follow-up box

---

## Author

**Ibo** — [@ibo-agentic](https://github.com/ibo-agentic)