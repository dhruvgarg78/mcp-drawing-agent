# 🖌️ MCP Drawing Agent

**mcp-drawing-agent** is an AI-powered automation tool that uses a language model (Google Gemini) to control Microsoft Paint. It interprets natural language instructions and executes drawing commands such as opening Paint, drawing rectangles, and inserting text — all via the MCP agent framework.

---

## 🧠 What It Does

This project connects:
- Google Gemini (LLM) for interpreting commands
- MCP (Modular Command Protocol) for tool orchestration
- Pywinauto & Win32 APIs for GUI automation
- A tool server that defines math and Paint actions

---

## 📁 Project Structure

```
.
├── talk2mcp-2.py        # Main orchestrator: prompts Gemini and calls tools
├── example2.py          # MCP server defining all math and Paint tools
├── .env                 # Local environment variables (not committed)
├── .env.example         # Example env file for reference
├── requirements.txt     # Python dependencies
└── README.md            # You're reading this :)
```

---

## 🚀 Setup Instructions

1. **Clone this repo**
```bash
git clone https://github.com/your-username/mcp-drawing-agent.git
cd mcp-drawing-agent
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Create your `.env` file**
```env
GEMINI_API_KEY=your_google_gemini_api_key
```

4. **Run the project**
```bash
python talk2mcp-2.py
```

---

## ✍️ Example Prompt

> Please open Paint, draw a rectangle from (780, 300) to (1140, 620), and add the text 'AUTOMATED SUCCESS' inside the rectangle.

The LLM will respond with step-by-step function calls like:

```
FUNCTION_CALL: open_paint
FUNCTION_CALL: draw_rectangle|780|300|1140|620
FUNCTION_CALL: add_text_in_paint|AUTOMATED SUCCESS
```

These get parsed and executed in sequence.

---

## 🧰 Features

- ✅ Tool registration using MCP
- ✅ Language model interprets and controls tool flow
- ✅ Supports both math and GUI tools
- ✅ Paint automation (open, draw shapes, write text)
- ✅ Modular tool functions (fibonacci, sin, log, etc.)

---

## ⚠️ Requirements & Notes

- Windows OS (MS Paint is required)
- Python 3.9+
- Internet access for Gemini API
- Tested on multi-monitor setups (uses secondary screen)

---

## 🔐 Environment Variables

Create a `.env` file like this:

```
GEMINI_API_KEY=your_google_gemini_api_key
```

**Important:** `.env` is in `.gitignore` and should never be committed.

---

## 📦 requirements.txt

```
python-dotenv
google-generativeai
mcp
pywinauto
Pillow
```

---

## 🤝 License

MIT License. Feel free to fork, modify, and build on top of it.

---
