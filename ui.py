import os
import base64
import asyncio
import threading
import streamlit as st
import cognee
from cognee.api.v1.visualize.visualize import visualize_graph

from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="Cognee Memory Demo",
    page_icon="🧠",
    layout="wide"
)

if 'event_loop' not in st.session_state:
    loop = asyncio.new_event_loop()
    st.session_state.event_loop = loop
    thread = threading.Thread(target=loop.run_forever, daemon=True)
    thread.start()

if 'stage' not in st.session_state:
    st.session_state.stage = 'add_data'
if 'data_added' not in st.session_state:
    st.session_state.data_added = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'user_data' not in st.session_state:
    st.session_state.user_data = ""
if 'force_refresh_viz' not in st.session_state:
    st.session_state.force_refresh_viz = False

def run_async(coro):
    future = asyncio.run_coroutine_threadsafe(coro, st.session_state.event_loop)
    return future.result(timeout=300)

async def remember_and_visualize(text, viz_path):
    await cognee.remember(text)
    os.makedirs(os.path.dirname(viz_path), exist_ok=True)
    await visualize_graph(viz_path)

async def only_visualize(viz_path):
    os.makedirs(os.path.dirname(viz_path), exist_ok=True)
    await visualize_graph(viz_path)

def get_viz_path():
    return os.path.join(os.path.dirname(__file__), ".artifacts", "graph_visualization.html")

def add_data_stage():
    st.title("🧠 Cognee Memory Demo")
    st.markdown("#### Step 1: Add Your Data")

    user_text = st.text_area(
        "Enter your data:",
        value=st.session_state.user_data,
        height=300,
        placeholder="Example:\n- I like to visit places near the beach\n- I prefer vegetarian meals\n- My hobbies include anime, F1, and cricket"
    )

    col1, col2 = st.columns([1, 5])

    with col1:
        if st.button("Remember Data", type="primary", use_container_width=True):
            if user_text.strip():
                with st.spinner("Processing and storing your data..."):
                    try:
                        run_async(remember_and_visualize(user_text, get_viz_path()))
                        st.session_state.user_data = user_text
                        st.session_state.data_added = True
                        st.session_state.stage = 'chatbot'
                        st.session_state.force_refresh_viz = False
                        st.success("Data successfully remembered!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error storing data: {str(e)}")
            else:
                st.warning("Please enter some text before proceeding.")

    with col2:
        st.write("")

def chatbot_stage():
    st.title("🧠 Cognee Memory Demo")
    st.markdown("#### Step 2: Chat and Recall")

    with st.sidebar:
        st.markdown("#### Your Stored Data")
        with st.expander("View stored data"):
            st.text_area("Stored data", value=st.session_state.user_data, height=200, disabled=True, label_visibility="collapsed")

        if st.button("Add More Data", use_container_width=True):
            st.session_state.stage = 'add_data'
            st.rerun()

        if st.button("Visualize Knowledge Graph", type="primary", use_container_width=True):
            st.session_state.stage = 'visualize'
            st.rerun()

        if st.button("Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

        if st.button("Reset Everything", use_container_width=True):
            with st.spinner("Clearing all data..."):
                try:
                    run_async(cognee.forget(dataset="main_dataset"))
                    viz_path = get_viz_path()
                    if os.path.exists(viz_path):
                        os.remove(viz_path)
                    st.session_state.stage = 'add_data'
                    st.session_state.data_added = False
                    st.session_state.chat_history = []
                    st.session_state.user_data = ""
                    st.session_state.force_refresh_viz = False
                    st.success("All data cleared!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error clearing data: {str(e)}")

    st.write("Ask questions based on the data you've stored. The system will recall relevant information to answer your queries.")

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input("Ask a question..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Recalling information..."):
                try:
                    results = run_async(cognee.recall(prompt))

                    if results:
                        texts = []
                        for result in results:
                            if hasattr(result, 'text'):
                                texts.append(result.text)
                            elif isinstance(result, dict) and 'text' in result:
                                texts.append(result['text'])
                            else:
                                raw = str(result)
                                if "text='" in raw:
                                    texts.append(raw.split("text='", 1)[1].rsplit("'", 1)[0])
                                else:
                                    texts.append(raw)
                        response = "\n\n".join(texts)
                    else:
                        response = "I could not find relevant information to answer your question."

                    st.write(response)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})

                except Exception as e:
                    error_msg = f"Error recalling information: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "content": error_msg})

def visualization_stage():
    st.title("🧠 Cognee Memory Demo")
    st.markdown("#### Step 3: Knowledge Graph Visualization")

    with st.sidebar:
        if st.button("← Back to Chat", use_container_width=True):
            st.session_state.stage = 'chatbot'
            st.rerun()

        if st.button("Add More Data", use_container_width=True):
            st.session_state.stage = 'add_data'
            st.rerun()

        if st.button("Refresh Visualization", type="primary", use_container_width=True):
            st.session_state.force_refresh_viz = True
            st.rerun()

    st.write("This visualization shows how your data is structured and connected in the knowledge graph.")

    viz_path = get_viz_path()

    with st.spinner("Generating knowledge graph visualization..."):
        try:
            if st.session_state.force_refresh_viz:
                run_async(only_visualize(viz_path))
                st.session_state.force_refresh_viz = False

            if os.path.exists(viz_path):
                with open(viz_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()

                encoded = base64.b64encode(html_content.encode('utf-8')).decode('utf-8')
                data_uri = f"data:text/html;base64,{encoded}"

                st.iframe(data_uri, height=800)
                st.success("Visualization loaded successfully!")

                with open(viz_path, 'rb') as f:
                    st.download_button(
                        label="Download Visualization",
                        data=f,
                        file_name="knowledge_graph.html",
                        mime="text/html"
                    )
            else:
                st.error("Visualization file not found. Please make sure data has been added and processed.")

        except Exception as e:
            st.error(f"Error generating visualization: {str(e)}")
            st.write("Please make sure you have added data and it has been processed correctly.")

def main():
    if st.session_state.stage == 'add_data':
        add_data_stage()
    elif st.session_state.stage == 'chatbot':
        chatbot_stage()
    elif st.session_state.stage == 'visualize':
        visualization_stage()

if __name__ == "__main__":
    main()