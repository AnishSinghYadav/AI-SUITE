import streamlit as st
import openai
import os
import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit
st.set_page_config(page_title="AI Suite", layout="centered")

# ---------------------- Face Swap Components ----------------------
@st.cache_resource
def load_models():
    app = FaceAnalysis(name='buffalo_l')
    app.prepare(ctx_id=0, det_size=(640, 640))
    model_path = os.path.join(os.getcwd(), "/Users/anishsmac/Desktop/Avatar/face-swap-app/inswapper_128.onnx")
    if not os.path.exists(model_path):
        st.error("Face swap model not found!")
        return None, None
    swapper = insightface.model_zoo.get_model(model_path)
    return app, swapper

def swap_faces(swapper, target_image, target_face, source_face):
    return swapper.get(target_image, target_face, source_face, paste_back=True)

def faceswap_page(app, swapper):
    st.title("🖼️ Face Swapper")
    col1, col2 = st.columns(2)
    with col1:
        source_image = st.file_uploader("Source Image", type=["jpg", "jpeg", "png"])
    with col2:
        target_image = st.file_uploader("Target Image", type=["jpg", "jpeg", "png"])

    if source_image and target_image:
        with st.spinner("Swapping Faces..."):
            try:
                # Process images
                source_img = cv2.imdecode(np.frombuffer(source_image.read(), np.uint8), -1)
                target_img = cv2.imdecode(np.frombuffer(target_image.read(), np.uint8), -1)
                source_img = cv2.cvtColor(source_img, cv2.COLOR_BGR2RGB)
                target_img = cv2.cvtColor(target_img, cv2.COLOR_BGR2RGB)

                # Detect faces
                source_faces = app.get(source_img)
                target_faces = app.get(target_img)

                if not source_faces:
                    st.error("No face in source image!")
                    return
                if not target_faces:
                    st.error("No face in target image!")
                    return

                # Perform swap
                swapped_img = swap_faces(swapper, target_img, target_faces[0], source_faces[0])

                # Display results
                st.success("Success!")
                cols = st.columns(3)
                cols[0].image(source_img, caption="Source", use_column_width=True)
                cols[1].image(target_img, caption="Target", use_column_width=True)
                cols[2].image(swapped_img, caption="Result", use_column_width=True)

            except Exception as e:
                st.error(f"Error: {str(e)}")

# ---------------------- Literary Creator Components ----------------------
openai.api_key = os.getenv("OPENAI_API_KEY")
openai_voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

def init_session_state():
    session_vars = {
        'attempts_left': 10,
        'allowed_topics': [],
        'generated_poem': "",
        'generated_story': "",
        'audio_content': None,
        'edited_text': "",
        'poem_topic': "",
        'story_topic': ""
    }
    for key, default in session_vars.items():
        if key not in st.session_state:
            st.session_state[key] = default

def check_topic_relevance(user_topic):
    if not user_topic or not st.session_state.allowed_topics:
        return False
    
    prompt = f"""Analyze if '{user_topic}' relates to any of these topics: {', '.join(st.session_state.allowed_topics)}.
    Consider synonyms, sub-topics, and direct associations. Respond ONLY with 'YES' or 'NO'."""
    
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=3
        )
        decision = response.choices[0].message.content.strip().lower()
        return decision.startswith('yes')
    except Exception as e:
        st.error(f"Validation error: {str(e)}")
        return False

def generate_literary_content(prompt):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Generation failed: {str(e)}")
        return ""

def literary_creator_page():
    st.title("📚 AI Literary Creator")
    init_session_state()
    
    # Parent Controls
    with st.sidebar:
        st.header("Parent Controls")
        new_topic = st.text_input("Add Approved Topic:")
        if st.button("Add Topic") and new_topic:
            if new_topic not in st.session_state.allowed_topics:
                st.session_state.allowed_topics.append(new_topic)
        st.write("**Approved Topics:**", st.session_state.allowed_topics)
        st.divider()
        st.write(f"Attempts Left: {st.session_state.attempts_left}/10")

    # Main Interface
    tab1, tab2 = st.tabs(["Poem Generator", "Story Generator"])
    
    with tab1:
        st.subheader("Create a Poem")
        if not st.session_state.allowed_topics:
            st.warning("No topics approved yet!")
            return
            
        st.session_state.poem_topic = st.text_input("Enter Poem Topic:", key="poem_input")
        col1, col2 = st.columns(2)
        with col1:
            poem_style = st.radio("Style:", ["Rhyming", "Free Verse", "Haiku"])
        with col2:
            poem_length = st.select_slider("Length:", ["Short", "Medium", "Long"])
        
        if st.button("Generate Poem"):
            if st.session_state.attempts_left <= 0:
                st.error("No attempts left!")
                return
                
            if not st.session_state.poem_topic:
                st.error("Please enter a topic!")
                return
                
            with st.spinner("Validating topic..."):
                if not check_topic_relevance(st.session_state.poem_topic):
                    st.error("Topic not allowed! Ask parents to add new topics.")
                    return
                    
            with st.spinner("Creating your poem..."):
                style_map = {
                    "Rhyming": "Create a rhyming poem about",
                    "Free Verse": "Write an emotional free-verse poem about",
                    "Haiku": "Compose a haiku (5-7-5 syllables) about"
                }
                length_map = {
                    "Short": "using concise language",
                    "Medium": "with vivid imagery",
                    "Long": "with extensive descriptive details"
                }
                prompt = f"{style_map[poem_style]} {st.session_state.poem_topic} {length_map[poem_length]}"
                
                st.session_state.generated_poem = generate_literary_content(prompt)
                st.session_state.edited_text = st.session_state.generated_poem
                st.session_state.attempts_left -= 1
                
        st.text_area("Edit Poem:", value=st.session_state.edited_text, height=300)

    with tab2:
        st.subheader("Create a Story")
        st.session_state.story_topic = st.text_input("Story Topic:", key="story_input")
        story_title = st.text_input("Story Title:")
        story_chapters = st.slider("Chapters:", 1, 10, 3)
        story_author = st.text_input("Author Name:")
        
        if st.button("Generate Story"):
            if st.session_state.attempts_left <= 0:
                st.error("No attempts left!")
                return
                
            if not st.session_state.story_topic:
                st.error("Please enter a story topic!")
                return
                
            with st.spinner("Validating topic..."):
                if not check_topic_relevance(st.session_state.story_topic):
                    st.error("Topic not allowed! Ask parents to add new topics.")
                    return
                    
            with st.spinner("Crafting your story..."):
                prompt = f"""Write a {story_chapters}-chapter story titled '{story_title}' 
                about {st.session_state.story_topic}. Include dialogues, character development, 
                and vivid descriptions. Author: {story_author}"""
                
                st.session_state.generated_story = generate_literary_content(prompt)
                st.session_state.edited_text = st.session_state.generated_story
                st.session_state.attempts_left -= 1
            
        st.text_area("Edit Story:", value=st.session_state.edited_text, height=300)

    # TTS Section
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        tts_voice = st.selectbox("Voice Style:", openai_voices)
    with col2:
        tts_speed = st.select_slider("Speech Speed:", ["0.75", "1.0", "1.25"])
    
    if st.button("Convert to Speech"):
        if not st.session_state.edited_text:
            st.error("No content to convert!")
            return
            
        try:
            audio = openai.audio.speech.create(
                model="tts-1",
                voice=tts_voice,
                input=st.session_state.edited_text,
                speed=float(tts_speed))
            st.audio(audio.content, format="audio/mp3")
        except Exception as e:
            st.error(f"Audio error: {str(e)}")

# ---------------------- Main Application ----------------------
def main():
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Select Mode:", ["Literary Creator", "Face Swapper"])

    if app_mode == "Literary Creator":
        literary_creator_page()
    else:
        app, swapper = load_models()
        if app and swapper:
            faceswap_page(app, swapper)
        else:
            st.error("Face swap components failed to load!")

if __name__ == "__main__":
    main()