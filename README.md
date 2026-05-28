# Cognee Memory Demo

Cognee helps applications turn user data into memory that can be searched and reused later.
It stores information in a knowledge graph, then recalls relevant facts when a user asks a question.
This demo saves travel preferences, visualizes the graph, and uses the stored memory for itinerary-style answers.

Use `inference.py` for a quickstart using Cognee with default LLM and embedding i.e., OpenAI, `custom_app.py` for Gemini + FastEmbed + Qdrant, and `ui.py` for the Streamlit interface.

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

## Custom App Setup

`custom_app.py` uses:

- Gemini as the LLM
- FastEmbed as the embedding provider
- Qdrant Cloud as the vector database

Install the extra packages:

```bash
pip install fastembed google-genai python-dotenv
pip install git+https://github.com/topoteretes/cognee-community.git#subdirectory=packages/vector/qdrant
```

Create a `.env` file from the custom app example:

```bash
cp .env.example.custom_app .env
```

Add these values to `.env`:

```bash
LLM_API_KEY=YOUR_GEMINI_API_KEY
LLM_PROVIDER=gemini
LLM_MODEL=gemini/gemini-flash-latest

EMBEDDING_PROVIDER=fastembed
EMBEDDING_MODEL=jinaai/jina-embeddings-v2-base-en
EMBEDDING_DIMENSIONS=768

QDRANT_URL=YOUR_QDRANT_CLOUD_CLUSTER_URL
QDRANT_API_KEY=YOUR_QDRANT_API_KEY
VECTOR_DB_PROVIDER=qdrant
VECTOR_DATASET_DATABASE_HANDLER=qdrant
```

Get the Gemini API key from Google AI Studio: [aistudio.google.com](https://aistudio.google.com/).

Get the Qdrant URL and API key from Qdrant Cloud:

- Create or open a Qdrant Cloud cluster: [cloud.qdrant](https://cloud.qdrant.io/)
- Copy the cluster endpoint URL into `QDRANT_URL`.
- Create or copy an API key for that cluster into `QDRANT_API_KEY`.

## Run

Run the inference script first:

```bash
python inference.py
```

Run the custom app with Gemini, FastEmbed, and Qdrant Cloud:

```bash
python custom_app.py
```

To build a UI to interface with saved memory, we use Streamlit:

```bash
streamlit run ui.py
```

The UI opens a local Streamlit app where you can add memory, ask questions, and view the generated knowledge graph.
