import streamlit as st
import tempfile
import os
from PIL import Image
from src.word_bot import define_word
from src.image_bot import describe_image
from src.safety import is_safe_request

# --- 1. Page Config (Browser Title) ---
st.set_page_config(
    page_title="Multimodal Dictionary",
    page_icon="book",
    layout="centered"  # Centered looks more like a mobile app/tool
)

# --- 2. Custom CSS (To make it look unique) ---
st.markdown("""
<style>
    /* Change the top header line color */
    div[data-testid="stDecoration"] {
        background-image: linear-gradient(90deg, #0066cc, #00ccff);
    }
    /* Style the main title */
    .main-title {
        font-family: 'Helvetica', sans-serif;
        color: #333;
        text-align: center;
        padding-bottom: 20px;
    }
    /* Custom card style for results */
    .result-box {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #e0e0e0;
        margin-top: 20px;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: #888;
        text-align: center;
        padding: 10px;
        font-size: 12px;
        border-top: 1px solid #eee;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. Helper Function to Clean Text ---
def parse_response(text):
    """Turns the raw text tags into a clean dictionary."""
    data = {}
    lines = text.split('\n')
    current_key = None
    
    for line in lines:
        if line.startswith('[') and ']' in line:
            # Found a tag like [definition]
            tag_end = line.find(']')
            key = line[1:tag_end].lower()
            data[key] = "" # Initialize
            current_key = key
        elif current_key:
            # Append text to the current key
            data[current_key] += line + " "
            
    # Clean up whitespace
    return {k: v.strip() for k, v in data.items()}

# --- 4. Main UI Layout ---

# Custom Title
st.markdown("<h1 class='main-title'>Multimodal Dictionary</h1>", unsafe_allow_html=True)

# Tabs for Navigation (Looks cleaner than sidebar)
tab1, tab2 = st.tabs(["Word Lookup", "Image Analysis"])

# --- TAB 1: WORD LOOKUP ---
with tab1:
    st.markdown("### Search Dictionary")
    query = st.text_input("Type a word:", placeholder="e.g., Serendipity")
    
    if st.button("Define Word", use_container_width=True):
        if not query:
            st.warning("Please enter a word first.")
        elif not is_safe_request(query):
            st.error("Request refused: Unsafe content detected.")
        else:
            with st.spinner("Searching WordNet..."):
                raw_out = define_word(query)
                res = parse_response(raw_out)
                
                # Display Result in a nice box
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                
                # Header: Word & POS
                c1, c2 = st.columns([2, 1])
                with c1:
                    st.subheader(res.get('word', query).title())
                with c2:
                    st.caption("Part of Speech")
                    st.write(f"**{res.get('pos', 'Unknown')}**")
                
                st.divider()
                
                # Definition
                st.markdown("##### Definition")
                st.write(res.get('definition', 'No definition found.'))
                
                # Examples & Synonyms (Accordion)
                with st.expander("More Details"):
                    st.markdown("**Examples:**")
                    st.write(res.get('examples', 'N/A'))
                    st.markdown("**Synonyms:**")
                    st.write(res.get('synonyms', 'N/A'))
                
                st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 2: IMAGE ANALYSIS ---
with tab2:
    st.markdown("### Identify Object")
    uploaded = st.file_uploader("Upload an image", type=['png', 'jpg', 'jpeg'])
    
    if uploaded:
        # Show image and button centered
        st.image(uploaded, caption="Preview", use_column_width=True)
        
        if st.button("Analyze Image", type="primary", use_container_width=True):
            with st.spinner("Processing image..."):
                # Handle file temp save
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                    tmp.write(uploaded.getvalue())
                    tmp_path = tmp.name
                
                # Run Logic
                raw_out = describe_image(tmp_path)
                os.remove(tmp_path) # Cleanup
                
                res = parse_response(raw_out)
                
                # Display Result
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                
                st.success(f"**Label:** {res.get('label', 'Unknown').upper()}")
                
                st.markdown("**Description:**")
                st.write(res.get('description', 'N/A'))
                
                st.info(f"💡 **Context:** {res.get('meaning', 'N/A')}")
                
                st.markdown('</div>', unsafe_allow_html=True)

# --- 5. Footer ---
st.markdown("""
<div class="footer">
    Midterm Exam Project | Intelligent Systems | Student: Jimenez
</div>
""", unsafe_allow_html=True)