"""
AI Chess Arena - Multi-Agent Chess with Groq
Two AI agents play chess using Groq AI (Free & Fast!)

Author: Kanav Chauhan
"""

import chess
import chess.svg
import streamlit as st
from groq import Groq
import random

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
        padding: 0.75rem;
        border-radius: 12px;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Session state
if "board" not in st.session_state:
    st.session_state.board = chess.Board()
if "move_history" not in st.session_state:
    st.session_state.move_history = []
if "game_log" not in st.session_state:
    st.session_state.game_log = []
if "max_moves" not in st.session_state:
    st.session_state.max_moves = 10
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# Initialize Groq
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ GROQ_API_KEY not found! Add it in Streamlit Secrets.")
    st.stop()

# Header
st.markdown('<h1 class="main-header">♟️ AI Chess Arena</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;color:#666;font-size:1.2rem;">Watch Two AI Agents Battle on Chess Board</p>', unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center;margin-bottom:2rem;'>
    <span class='agent-badge'>🤖 Multi-Agent AI</span>
    <span class='agent-badge'>⚡ Groq Llama 3.3</span>
    <span class='agent-badge'>♟️ Full Chess Rules</span>
    <span class='agent-badge'>🆓 100% Free!</span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Game Settings")
    
    max_moves = st.slider("Number of Moves:", 5, 30, 10)
    st.session_state.max_moves = max_moves
    
    st.info(f"""
**Selected:** {max_moves} moves

💡 **Recommendations:**
- Quick demo: 5-10 moves
- Medium game: 15-20 moves
- Long game: 25-30 moves

✅ **Completely FREE!**
No API key needed!
""")
    
    st.markdown("---")
    st.markdown("### 🤖 The AI Agents")
    st.markdown("""
**Agent White** ⚪
- Controls white pieces
- Aggressive strategy
- Powered by Groq Llama 3.3

**Agent Black** ⚫
- Controls black pieces
- Defensive tactics
- Powered by Groq Llama 3.3

Both agents analyze positions and make strategic decisions in real-time!
""")
    
    st.markdown("---")
    st.markdown("### 📊 Stats")
    st.metric("Moves Played", len(st.session_state.move_history))
    st.metric("Max Moves", st.session_state.max_moves)

# AI Agent function
def get_ai_move(board: chess.Board, player: str) -> str:
    """Get chess move from AI agent using Groq"""
    
    legal_moves = [str(move) for move in board.legal_moves]
    
    if player == "white":
        personality = "You play WHITE pieces. Be aggressive, control center, attack when possible."
    else:
        personality = "You play BLACK pieces. Be solid defensively, look for counter-attacks."
    
    prompt = f"""{personality}

Board position (FEN): {board.fen()}

Legal moves: {', '.join(legal_moves[:20])}

Analyze and choose the BEST move. Consider:
- Piece safety
- Center control  
- King safety
- Tactics

Respond with ONLY the move in UCI format (like 'e2e4'). Nothing else."""

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a chess grandmaster. Respond only with a move in UCI format."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.8,
            max_tokens=30
        )
        
        move_text = response.choices[0].message.content.strip().lower()
        
        # Extract valid move
        for word in move_text.split():
            word = word.strip('.,!?"\n')
            if len(word) >= 4 and len(word) <= 5:
                try:
                    test_move = chess.Move.from_uci(word)
                    if test_move in board.legal_moves:
                        return word
                except:
                    pass
        
        # Fallback: random legal move
        return random.choice(legal_moves)
    
    except Exception as e:
        # Fallback on error
        return random.choice(legal_moves)

# Main interface
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🎮 Chess Board")
    
    # Display board
    board_svg = chess.svg.board(st.session_state.board, size=450)
    st.image(board_svg, use_container_width=True)

with col2:
    st.markdown("### 📊 Game Status")
    
    if st.session_state.board.is_checkmate():
        winner = 'White' if st.session_state.board.turn == chess.BLACK else 'Black'
        st.success(f"🏆 {winner} wins by checkmate!")
        st.session_state.game_over = True
    elif st.session_state.board.is_stalemate():
        st.info("🤝 Draw by stalemate")
        st.session_state.game_over = True
    elif st.session_state.board.is_insufficient_material():
        st.info("⚖️ Draw - insufficient material")
        st.session_state.game_over = True
    elif st.session_state.board.is_check():
        st.warning("⚠️ King is in check!")
    else:
        turn = "White" if st.session_state.board.turn == chess.WHITE else "Black"
        st.info(f"Turn: {turn}")
    
    st.markdown("---")
    
    st.markdown("**Game Progress**")
    progress = min(len(st.session_state.move_history) / st.session_state.max_moves, 1.0)
    st.progress(progress)
    st.caption(f"{len(st.session_state.move_history)} / {st.session_state.max_moves} moves")

st.markdown("---")

# Game controls
col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ Start New Game", type="primary", use_container_width=True):
        # Reset game
        st.session_state.board = chess.Board()
        st.session_state.move_history = []
        st.session_state.game_log = []
        st.session_state.game_over = False
        
        # Play game
        with st.spinner("🤖 AI agents are playing chess..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            move_count = 0
            
            while move_count < st.session_state.max_moves and not st.session_state.game_over:
                # Determine whose turn
                player = "white" if st.session_state.board.turn == chess.WHITE else "black"
                agent_name = "Agent White ⚪" if player == "white" else "Agent Black ⚫"
                
                status_text.text(f"Move {move_count + 1}: {agent_name} is thinking...")
                
                # Get AI move
                move_uci = get_ai_move(st.session_state.board, player)
                
                # Execute move
                try:
                    move = chess.Move.from_uci(move_uci)
                    piece = st.session_state.board.piece_at(move.from_square)
                    from_sq = chess.square_name(move.from_square)
                    to_sq = chess.square_name(move.to_square)
                    
                    st.session_state.board.push(move)
                    
                    # Save board state
                    board_svg = chess.svg.board(
                        st.session_state.board,
                        arrows=[(move.from_square, move.to_square)],
                        size=400
                    )
                    st.session_state.move_history.append(board_svg)
                    
                    # Log move
                    piece_name = chess.piece_name(piece.piece_type).capitalize()
                    log_entry = f"{agent_name}: {piece_name} {from_sq} → {to_sq}"
                    st.session_state.game_log.append(log_entry)
                    
                    # Check game end
                    if st.session_state.board.is_checkmate():
                        winner = 'White' if st.session_state.board.turn == chess.BLACK else 'Black'
                        st.session_state.game_log.append(f"🏆 Checkmate! {winner} wins!")
                        st.session_state.game_over = True
                    elif st.session_state.board.is_stalemate():
                        st.session_state.game_log.append("🤝 Stalemate - Draw!")
                        st.session_state.game_over = True
                    elif st.session_state.board.is_insufficient_material():
                        st.session_state.game_log.append("⚖️ Draw - Insufficient material")
                        st.session_state.game_over = True
                    elif st.session_state.board.is_check():
                        st.session_state.game_log.append("⚠️ Check!")
                    
                    move_count += 1
                    progress_bar.progress(min(move_count / st.session_state.max_moves, 1.0))
                
                except Exception as e:
                    st.error(f"Error with move: {e}")
                    break
            
            status_text.empty()
            progress_bar.empty()
        
        st.success("✅ Game complete! Scroll down to see all moves.")
        st.rerun()

with col2:
    if st.button("🔄 Reset Board", use_container_width=True):
        st.session_state.board = chess.Board()
        st.session_state.move_history = []
        st.session_state.game_log = []
        st.session_state.game_over = False
        st.rerun()

# Game log
if st.session_state.game_log:
    st.markdown("---")
    st.markdown("### 📜 Game Log")
    
    for i, log in enumerate(st.session_state.game_log):
        st.text(f"{i+1}. {log}")

# Move history visualization
if st.session_state.move_history:
    st.markdown("---")
    st.markdown("### 🎥 Move History")
    
    cols = st.columns(3)
    for i, board_svg in enumerate(st.session_state.move_history):
        agent = "White ⚪" if i % 2 == 0 else "Black ⚫"
        
        with cols[i % 3]:
            st.markdown(f"**Move {i+1}** by {agent}")
            st.image(board_svg)

# Footer
st.markdown("---")

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.link_button(
        "🔗 Connect on LinkedIn",
        "https://linkedin.com/in/kanavchauhan23",
        use_container_width=True,
        type="primary"
    )

st.markdown("<h4 style='text-align:center;'>Built with ❤️ by Kanav Chauhan</h4>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>AI Chess Arena - Powered by Groq Llama 3.3</p>", unsafe_allow_html=True)
