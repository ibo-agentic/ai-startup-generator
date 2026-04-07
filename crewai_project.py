# ============================================================
# AI STARTUP IDEA GENERATOR
# Built with CrewAI + Gradio
# 4 Agents: Idea Generator, Market Researcher, 
#           Business Strategist, Pitch Creator
# ============================================================

# --- IMPORTS ---
# os: lets us talk to the operating system (read files, env vars)
import os

# gradio: creates the web UI (the website you see in browser)
import gradio as gr

# load_dotenv: reads the .env file and loads API keys into memory
from dotenv import load_dotenv

# Agent: creates an AI worker with a role and personality
# Task: gives specific work to an agent
# Crew: manages all agents and tasks together
# Process: decides how agents work (sequential = one by one)
from crewai import Agent, Task, Crew, Process

# --- LOAD API KEY ---
# This reads GROQ_API_KEY from your .env file
# Without this, agents have no brain to think with
load_dotenv()

# ============================================================
# CONVERSATION MEMORY SYSTEM
# This gives the app memory so it remembers past conversations
# Like a notebook that stores what user asked before
# ============================================================

# Empty list to store conversation history
# Each item will be a dictionary: {"user": ..., "ai": ...}
conversation_history = []

def add_to_memory(user_input, ai_output):
    # This function saves each conversation to our notebook
    # Called after every successful generation
    conversation_history.append({
        "user": user_input,   # what user typed
        "ai": ai_output       # what AI generated
    })

def get_memory_context():
    # This function reads the notebook and returns past context
    # So agents know what was discussed before
    
    # If notebook is empty, return nothing
    if not conversation_history:
        return ""
    
    # Start building context string
    context = "\n\nPrevious conversation context:\n"
    
    # Only read last 3 conversations ([-3:] means last 3 items)
    for item in conversation_history[-3:]:
        context += f"User asked: {item['user']}\n"
        # [:200] means only first 200 characters to save space
        context += f"Output summary: {item['ai'][:200]}...\n\n"
    
    return context

# ============================================================
# AGENT 1 — IDEA GENERATOR
# Job: Thinks of 3 startup ideas based on user input
# Thinks like: a creative entrepreneur
# ============================================================
idea_generator = Agent(
    # Job title of this agent
    role="Startup Idea Generator",
    
    # What this agent wants to achieve
    goal="Generate 3 innovative startup ideas based on user interests",
    
    # Personality and experience — makes AI respond like this person
    # The more detailed the backstory, the better the output
    backstory="""You are a first-time founder who has tried and failed 
    at 2 startups before finally succeeding on the third. You think 
    practically. You spot problems in everyday life and turn them into 
    business ideas. You speak from real experience, not textbooks.""",
    
    # Which AI model to use as the brain
    # groq/llama-3.3-70b-versatile is free and powerful
    llm="groq/llama-3.3-70b-versatile",
    
    # verbose=True means show what agent is doing in terminal
    verbose=True,
    
    # allow_delegation=False means this agent cannot pass 
    # work to other agents by itself
    allow_delegation=False
)

# ============================================================
# AGENT 2 — MARKET RESEARCHER
# Job: Analyzes market size, competitors, trends
# Thinks like: a senior market analyst
# ============================================================
market_researcher = Agent(
    role="Market Researcher",
    
    goal="Analyze market potential and competition for each startup idea",
    
    backstory="""You are a market analyst who spent 10 years at a 
    consulting firm before going independent. You are known for 
    finding hidden market opportunities others miss. You back every 
    claim with real numbers and honest risk assessment.""",
    
    llm="groq/llama-3.3-70b-versatile",
    verbose=True,
    allow_delegation=False
)

# ============================================================
# AGENT 3 — BUSINESS STRATEGIST
# Job: Builds revenue model, GTM plan, roadmap
# Thinks like: an MBA consultant
# ============================================================
business_strategist = Agent(
    role="Business Strategist",
    
    goal="Develop a solid business strategy with revenue model and go-to-market plan",
    
    backstory="""You did your MBA and then joined a startup as employee 
    number 3. You helped them grow from zero to $5M revenue in 2 years. 
    You know what works in theory AND in practice. You build strategies 
    that are realistic, not just impressive on paper.""",
    
    llm="groq/llama-3.3-70b-versatile",
    verbose=True,
    allow_delegation=False
)

# ============================================================
# AGENT 4 — PITCH CREATOR
# Job: Writes the investor pitch in human voice
# Thinks like: a real founder pitching for the first time
# ============================================================
pitch_creator = Agent(
    role="Pitch Deck Creator",
    
    goal="Create a compelling investor pitch written in natural human voice",
    
    # This backstory is key — makes output sound human not AI
    backstory="""You are a first-time founder pitching to investors 
    for the first time. You are passionate and real. You write how 
    you talk. You avoid corporate buzzwords like leverage, utilize, 
    robust, scalable, revolutionary. Instead you say use, build, grow, 
    better, faster. You tell real stories. People say your pitches 
    feel genuine, not polished and fake.""",
    
    llm="groq/llama-3.3-70b-versatile",
    verbose=True,
    allow_delegation=False
)

# ============================================================
# FORMAT OUTPUT AS BEAUTIFUL HTML
# This converts plain text output into nice colored cards
# Each section (HOOK, PROBLEM etc) gets its own card
# ============================================================
def format_output(text):
    # Dictionary mapping section names to emojis
    # These are the 7 sections Agent 4 will write
    sections = {
        "HOOK": "🎯",
        "PROBLEM": "❗",
        "SOLUTION": "💡",
        "MARKET OPPORTUNITY": "📈",
        "BUSINESS MODEL": "💰",
        "TRACTION PLAN": "🚀",
        "THE ASK": "🤝"
    }

    # CSS styles for the cards
    # This makes the output look beautiful
    html = """
    <style>
        .result-container {
            font-family: 'Segoe UI', sans-serif;
            padding: 20px;
            max-width: 900px;
        }
        .section-card {
            background: #1e1e2e;
            border-radius: 12px;
            padding: 20px 25px;
            margin-bottom: 16px;
            border-left: 4px solid #7c3aed;
        }
        .section-title {
            color: #a78bfa;
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .section-body {
            color: #e2e8f0;
            font-size: 15px;
            line-height: 1.8;
        }
        .section-body strong {
            color: #a78bfa;
        }
        ol, ul {
            padding-left: 20px;
            margin-top: 8px;
        }
        li {
            margin-bottom: 6px;
            color: #e2e8f0;
        }
        .header-banner {
            background: linear-gradient(135deg, #7c3aed, #2563eb);
            border-radius: 12px;
            padding: 20px 25px;
            margin-bottom: 20px;
            color: white;
            font-size: 22px;
            font-weight: 800;
        }
    </style>
    <div class="result-container">
        <div class="header-banner">🚀 Your Startup Plan is Ready!</div>
    """

    # Split the text into lines and process each one
    lines = text.split('\n')
    current_section = None  # tracks which section we are in
    current_content = []    # stores lines of current section

    for line in lines:
        line = line.strip()  # remove extra spaces
        if not line:
            continue  # skip empty lines

        # Check if this line is a section header like **HOOK**
        found_section = False
        for section_name, emoji in sections.items():
            if f"**{section_name}**" in line or f"**{section_name}:" in line:
                
                # If we were already in a section, save it first
                if current_section:
                    content_html = '<br>'.join(current_content)
                    prev_emoji = sections.get(current_section, "📌")
                    # Add the completed section card to HTML
                    html += f"""
                    <div class="section-card">
                        <div class="section-title">{prev_emoji} {current_section}</div>
                        <div class="section-body">{content_html}</div>
                    </div>"""
                
                # Start new section
                current_section = section_name
                current_content = []
                found_section = True
                break

        # If not a header, add line to current section content
        if not found_section and current_section:
            # Convert **bold** markdown to HTML <strong> tags
            line = line.replace('**', '<strong>', 1)
            line = line.replace('**', '</strong>', 1)
            current_content.append(line)

    # Don't forget to add the very last section
    if current_section:
        content_html = '<br>'.join(current_content)
        prev_emoji = sections.get(current_section, "📌")
        html += f"""
        <div class="section-card">
            <div class="section-title">{prev_emoji} {current_section}</div>
            <div class="section-body">{content_html}</div>
        </div>"""

    # Close the container div
    html += "</div>"
    return html

# ============================================================
# MAIN FUNCTION
# This runs when user clicks the Generate button
# It creates tasks, assembles crew, and returns result
# ============================================================
def run_startup_generator(user_input, progress=gr.Progress()):
    
    # Get memory from previous conversations
    memory_context = get_memory_context()
    
    # Combine current input with memory
    # This is how follow-up questions work
    full_context = user_input + memory_context

    # Update loading bar to 10%
    progress(0.1, desc="Starting agents...")

    # ---- TASK 1: Given to Agent 1 (Idea Generator) ----
    # Agent 1 reads this and generates 3 startup ideas
    task1 = Task(
        description=f"""Generate 3 unique startup ideas based on: {full_context}
        For each idea provide:
        - Startup name and one-line description
        - The core problem it solves
        - Target customers
        - Basic revenue model
        
        Write in simple, clear language. Be specific and realistic.""",
        
        # Tells agent what a good answer looks like
        expected_output="3 detailed startup ideas each with name, description, problem, target customers, revenue model",
        
        # Which agent does this task
        agent=idea_generator
    )

    progress(0.25, desc="Agent 1: Generating ideas...")

    # ---- TASK 2: Given to Agent 2 (Market Researcher) ----
    # Agent 2 automatically receives Agent 1's output
    # No need to pass it manually - CrewAI does this automatically
    task2 = Task(
        description="""Analyze the 3 startup ideas from market perspective.
        For each idea provide:
        - Market size estimate with real numbers
        - 2-3 key competitors by name
        - Market trends supporting this idea
        - One major risk to watch out for
        
        Then pick the BEST idea and explain exactly why.""",
        
        expected_output="Market analysis for all 3 ideas with trends, risks and clear final recommendation",
        agent=market_researcher
    )

    progress(0.5, desc="Agent 2: Researching market...")

    # ---- TASK 3: Given to Agent 3 (Business Strategist) ----
    # Agent 3 receives output from Agent 1 AND Agent 2
    task3 = Task(
        description="""Create a business strategy for the best startup idea.
        Include:
        - Revenue model with actual pricing numbers
        - Go-to-market strategy (how to get first 100 customers)
        - Key partnerships needed
        - Top 3 risks and how to handle them
        - 6-month milestone roadmap with specific goals
        
        Be practical and realistic, not just theoretical.""",
        
        expected_output="Complete business strategy with revenue model, GTM plan, partnerships, risks and 6-month roadmap",
        agent=business_strategist
    )

    progress(0.75, desc="Agent 3: Building strategy...")

    # ---- TASK 4: Given to Agent 4 (Pitch Creator) ----
    # Agent 4 receives everything from all 3 agents
    # and writes the final pitch
    task4 = Task(
        description="""Write an investor pitch with these 7 sections.
        Use exactly these headers with ** markers:
        **HOOK**
        **PROBLEM**
        **SOLUTION**
        **MARKET OPPORTUNITY**
        **BUSINESS MODEL**
        **TRACTION PLAN**
        **THE ASK**

        IMPORTANT WRITING RULES - follow these strictly:
        - Write like a real human founder, passionate about their idea
        - Use simple everyday words, avoid fancy business jargon
        - Write in natural paragraphs, not just bullet points
        - Add personal touches like "we believe", "we noticed", "here is the thing"
        - Mix short sentences with longer ones for natural flow
        - Avoid these words: leverage, utilize, streamline, robust, 
          scalable, groundbreaking, revolutionary, cutting-edge
        - Instead use: use, build, grow, simple, better, faster, cheaper
        - Sound excited but real, like pitching to a friend
        - Use real numbers to sound grounded
        - Occasionally use phrases like "think about it", "the truth is"
        """,
        
        expected_output="A 7-section investor pitch written in natural human voice with ** section headers",
        agent=pitch_creator
    )

    progress(0.9, desc="Agent 4: Writing pitch...")

    # ---- ASSEMBLE THE CREW ----
    # Put all agents and tasks together
    crew = Crew(
        # List of all 4 agents
        agents=[idea_generator, market_researcher, business_strategist, pitch_creator],
        
        # List of all 4 tasks in order
        tasks=[task1, task2, task3, task4],
        
        # sequential = run one by one (1 then 2 then 3 then 4)
        process=Process.sequential,
        
        # Show detailed logs in terminal
        verbose=True
    )

    # KICKOFF! This starts all agents working
    result = crew.kickoff()
    
    # Convert result to string
    result_str = str(result)
    
    # Save to memory for future follow-up questions
    add_to_memory(user_input, result_str)
    
    # Loading bar complete
    progress(1.0, desc="Done!")

    # Return both formatted HTML (for display) and raw text (for copying)
    return format_output(result_str), result_str

# ============================================================
# GRADIO UI
# This creates the website interface
# gr.Blocks = full page layout control
# ============================================================
with gr.Blocks(
    title="AI Startup Idea Generator",
    css="""
        .gradio-container { max-width: 1200px !important; }
        footer { display: none !important; }
    """
) as demo:

    # Page title and description
    gr.Markdown("# 🚀 AI Startup Idea Generator")
    gr.Markdown("4 AI agents collaborate to generate, research, strategize, and pitch your startup idea.")
    gr.Markdown("---")

    # gr.Row = puts things side by side horizontally
    with gr.Row():
        
        # Left column - input side (scale=1 means smaller)
        with gr.Column(scale=1):
            gr.Markdown("### 💡 Your Input")
            
            # Text input box where user types their idea
            user_input = gr.Textbox(
                label="Describe your interests or industry",
                placeholder="Example: I'm interested in healthcare and AI...",
                lines=4
            )
            
            # Clickable example prompts to help users get started
            gr.Examples(
                examples=[
                    ["I'm passionate about education and want to use AI to help students learn better"],
                    ["I want to build something in fintech that helps Gen Z manage money"],
                    ["Sustainable fashion targeting eco-conscious millennials"],
                    ["Mental health and wellness apps"]
                ],
                inputs=user_input
            )
            
            # The main Generate button
            # variant="primary" makes it colored/highlighted
            generate_btn = gr.Button(
                "🚀 Generate My Startup",
                variant="primary",
                size="lg"
            )
            
            gr.Markdown("---")
            gr.Markdown("### 🧠 Memory Active")
            gr.Markdown("Try: *'Now make it low-cost'* or *'Make the pitch more aggressive'*")

        # Right column - output side (scale=2 means 2x bigger)
        with gr.Column(scale=2):
            gr.Markdown("### 📊 Results")
            
            # HTML output - shows beautiful formatted cards
            html_output = gr.HTML(label="Your Startup Plan")
            
            # Accordion = collapsible section
            # open=False means it starts collapsed/hidden
            with gr.Accordion("📋 Raw Text (for copying)", open=False):
                # Plain text output for easy copying
                raw_output = gr.Textbox(
                    label="Raw Output",
                    lines=15,
                    max_lines=30
                )

    # Connect the button to the function
    # When button clicked:
    # - fn: which function to run
    # - inputs: what to pass to the function
    # - outputs: where to put the results (2 outputs now!)
    generate_btn.click(
        fn=run_startup_generator,
        inputs=user_input,
        outputs=[html_output, raw_output],
        show_progress=True
    )

    gr.Markdown("---")
    gr.Markdown("Built with CrewAI + Gradio | 4 Agents: Idea Generator → Market Researcher → Business Strategist → Pitch Creator")

# ============================================================
# LAUNCH THE APP
# if __name__ == "__main__" means:
# only run this if we directly run this file
# not if another file imports it
# ============================================================
if __name__ == "__main__":
    # Start the web server
    # share=False = only accessible on your computer
    # share=True = creates public link anyone can access
    demo.launch(share=False)