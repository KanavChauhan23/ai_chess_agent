"""
AI Chess Arena - Multi-Agent Chess Game
Two AI agents play chess using AutoGen

Author: Kanav Chauhan
"""

import chess
import chess.svg
import streamlit as st
from autogen import ConversableAgent, register_function

# Page config
st.set_page_config(
    page_title="AI Chess Arena",
    layout="wide",
    page_icon="♟️"
)

# Custom CSS  
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    
    * { font-family: 'Poppins', sans-serif; }
    
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .agent-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        display: inline-block;
        margin: 0.3rem;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Session state
for key, default in [
    ("openai_api_key", None),
    ("board", chess.Board()),
    ("made_move", False),
    ("move_history", []),
    ("max_turns", 5)
]:
    if key not in st.session_state:
        st.session_state[key] = default

# Header
st.markdown('<h1 class="main-header">♟️ AI Chess Arena</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;color:#666;font-size:1.2rem;">Watch Two AI Agents Battle on Chess Board</p>', unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center;margin-bottom:2rem;'>
    <span class='agent-badge'>🤖 AutoGen</span>
    <span class='agent-badge'>🧠 GPT-4o-mini</span>
    <span class='agent-badge'>♟️ Python Chess</span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    api_key = st.text_input("OpenAI API Key:", type="password")
    if api_key:
        st.session_state.openai_api_key = api_key
        st.success("✅ API key saved!")
    
    st.markdown("---")
    st.markdown("### 🎮 Settings")
    
    max_turns = st.slider("Number of Moves:", 1, 50, 5)
    st.session_state.max_turns = max_turns
    
    st.info(f"""
**Current:** {max_turns} moves

💡 **Recommended:**
- Quick: 5-10 moves
- Short: 20-30 moves  
- Full: 100+ moves

⚠️ More moves = higher API costs
""")
    
    st.markdown("---")
    st.markdown("### 🤖 The Agents")
    st.markdown("""
**Agent White** ⚪
- White pieces
- Opening strategy
- GPT-4o-mini

**Agent Black** ⚫
- Black pieces
- Counter-attack
- GPT-4o-mini

**Game Master** 🎯
- Validates moves
- Manages turns
""")

# Chess functions
def available_moves() -> str:
    moves = [str(m) for m in st.session_state.board.legal_moves]
    return "Available moves: " + ",".join(moves)

def execute_move(move: str) -> str:
    try:
        chess_move = chess.Move.from_uci(move)
        if chess_move not in st.session_state.board.legal_moves:
            return f"Invalid move: {move}"
        
        st.session_state.board.push(chess_move)
        st.session_state.made_move = True
        
        board_svg = chess.svg.board(
            st.session_state.board,
            arrows=[(chess_move.from_square, chess_move.to_square)],
            size=400
        )
        st.session_state.move_history.append(board_svg)
        
        piece = st.session_state.board.piece_at(chess_move.to_square)
        from_sq = chess.SQUARE_NAMES[chess_move.from_square]
        to_sq = chess.SQUARE_NAMES[chess_move.to_square]
        
        desc = f"Moved {chess.piece_name(piece.piece_type)} from {from_sq} to {to_sq}."
        
        if st.session_state.board.is_checkmate():
            winner = 'White' if st.session_state.board.turn == chess.BLACK else 'Black'
            desc += f"\n🏆 Checkmate! {winner} wins!"
        elif st.session_state.board.is_check():
            desc += "\n⚠️ Check!"
        
        return desc
    except:
        return f"Invalid move: {move}"

def check_made_move(msg):
    if st.session_state.made_move:
        st.session_state.made_move = False
        return True
    return False

# Main
if st.session_state.openai_api_key:
    try:
        config = [{"model": "gpt-4o-mini", "api_key": st.session_state.openai_api_key}]
        
        agent_white = ConversableAgent(
            name="Agent_White",
            system_message="You are a chess player with white pieces. Call available_moves() then execute_move().",
            llm_config={"config_list": config, "cache_seed": None}
        )
        
        agent_black = ConversableAgent(
            name="Agent_Black",
            system_message="You are a chess player with black pieces. Call available_moves() then execute_move().",
            llm_config={"config_list": config, "cache_seed": None}
        )
        
        game_master = ConversableAgent(
            name="Game_Master",
            llm_config=False,
            is_termination_msg=check_made_move,
            default_auto_reply="Make a move.",
            human_input_mode="NEVER"
        )
        
        for agent in [agent_white, agent_black]:
            register_function(execute_move, caller=agent, executor=game_master, name="execute_move", description="Make a move")
            register_function(available_moves, caller=agent, executor=game_master, name="available_moves", description="Get legal moves")
        
        agent_white.register_nested_chats(
            trigger=agent_black,
            chat_queue=[{"sender": game_master, "recipient": agent_white, "summary_method": "last_msg"}]
        )
        
        agent_black.register_nested_chats(
            trigger=agent_white,
            chat_queue=[{"sender": game_master, "recipient": agent_black, "summary_method": "last_msg"}]
        )
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🎮 Chess Board")
            board_svg = chess.svg.board(st.session_state.board, size=400)
            st.image(board_svg, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Game Info")
            st.metric("Moves", len(st.session_state.move_history))
            st.metric("Max Moves", st.session_state.max_turns)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("▶️ Start Game", type="primary", use_container_width=True):
                st.session_state.board.reset()
                st.session_state.move_history = []
                
                with st.spinner("🤖 AI agents playing..."):
                    result = agent_black.initiate_chat(
                        recipient=agent_white,
                        message="Let's play chess! You go first.",
                        max_turns=st.session_state.max_turns,
                        summary_method="reflection_with_llm"
                    )
                
                st.success("✅ Game complete!")
                st.markdown(f"**Summary:** {result.summary}")
        
        with col2:
            if st.button("🔄 Reset", use_container_width=True):
                st.session_state.board.reset()
                st.session_state.move_history = []
                st.rerun()
        
        if st.session_state.move_history:
            st.markdown("---")
            st.markdown("### 📜 Move History")
            
            cols = st.columns(3)
            for i, svg in enumerate(st.session_state.move_history):
                agent = "White ⚪" if i % 2 == 0 else "Black ⚫"
                with cols[i % 3]:
                    st.markdown(f"**Move {i+1}** by {agent}")
                    st.image(svg)
    
    except Exception as e:
        st.error(f"❌ Error: {e}")

else:
    st.info("""
### 🚀 Getting Started

AI Chess Arena - Two AI agents play chess!

**How it works:**
1. Two AI agents (White & Black) powered by GPT-4o-mini
2. They analyze and make strategic moves
3. Game Master validates moves

**To start:**
1. Get OpenAI API key from platform.openai.com
2. Enter it in sidebar
3. Click "Start Game"

**Features:**
- ♟️ Full chess rules
- 🤖 Multi-agent AutoGen
- 🎯 Move validation
- 📊 Real-time tracking
""")
    st.warning("⚠️ Enter API key in sidebar!")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns([1,1,1])
with col2:
    st.link_button("🔗 LinkedIn", "https://linkedin.com/in/kanavchauhan23", use_container_width=True, type="primary")

st.markdown("<h4 style='text-align:center;'>Built with ❤️ by Kanav Chauhan</h4>", unsafe_allow_html=True)
