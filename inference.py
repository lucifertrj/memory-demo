import os
import cognee
import asyncio
from dotenv import load_dotenv
load_dotenv() # or os.environ["LLM_API_KEY"] = "YOUR OPENAI_API_KEY"
from cognee.api.v1.visualize.visualize import visualize_graph

MY_PREFERENCE = """
- I like to visit places near the beach where I can find the best spots. 
- I need locations that are rare to find on blogs but are goldmine places for your eyes
- I prefer Vegetarian meals. Use this when I ask for restaurants recommendation
- My hobbies that might also help in planning Itineraries: I love Anime, F1 and Cricket.
"""

async def main():
    # Store permanently in the knowledge graph (runs add + cognify + improve)
    await cognee.remember(MY_PREFERENCE)
    # await cognee.remember("- I also like mountains views or nearby places", session_id="travel") # Store in session memory (fast cache, syncs to graph in background)
    visualize_graph_path = os.path.join(
        os.path.dirname(__file__), ".artifacts", "graph_after_remember.html"
    )
    await visualize_graph(visualize_graph_path)

    results = await cognee.recall("plan a 3 days Itinerary for Nairobi along with restaurants to try food.")
    for result in results:
        print(result)
   
    await cognee.forget(dataset="main_dataset")  # Delete when done

if __name__ == '__main__':
    asyncio.run(main())