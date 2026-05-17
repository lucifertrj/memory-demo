# Cognee Memory Demo

Cognee helps applications turn user data into memory that can be searched and reused later.
It stores information in a knowledge graph, then recalls relevant facts when a user asks a question.
This demo saves travel preferences, visualizes the graph, and uses the stored memory for itinerary-style answers.

Use `inference.py` for a quickstart using Cognee with default LLM and embedding i.e., OpenAI and `ui.py` for the Streamlit interface.

## Setup

Create a `.env` file with your LLM API key:

```bash
cp .env.example .env
```

Edit `.env`:

```bash
LLM_API_KEY=YOUR_OPENAI_API_KEY
```

Activate the local environment:

```bash
source pipenv/bin/activate
```

If you are setting up from scratch instead, install the main packages:

```bash
pip install cognee python-dotenv streamlit
```

## Run

Run the inference script first:

```bash
python inference.py
```

To build a UI to interface with saved memory, we use Streamlit:

```bash
streamlit run ui.py
```

The UI opens a local Streamlit app where you can add memory, ask questions, and view the generated knowledge graph.
