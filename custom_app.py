import os,pathlib
import asyncio

import cognee
from cognee_community_vector_adapter_qdrant import register 

from dotenv import load_dotenv
load_dotenv()

system_path = pathlib.Path(__file__).parent
cognee.config.system_root_directory(os.path.join(system_path, ".cognee_system"))
cognee.config.data_root_directory(os.path.join(system_path, ".data_storage"))

cognee.config.set_relational_db_config({"db_provider": "sqlite"})
cognee.config.set_vector_db_config({
    "vector_db_provider": "qdrant",
    "vector_db_url": os.getenv("QDRANT_URL"),
    "vector_db_key": os.getenv("QDRANT_API_KEY"),
    "vector_dataset_database_handler":"qdrant"
})
MY_PREFERENCE = """
- I like to visit places near the beach where I can find the best spots. 
- I need locations that are rare to find on blogs but are goldmine places for your eyes
- I prefer Vegetarian meals. Use this when I ask for restaurants recommendation
- My hobbies that might also help in planning Itineraries: I love Anime, F1 and Cricket.
"""

async def main():
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)

    await cognee.add(MY_PREFERENCE,node_set="personal_tarun")
    await cognee.add("- In Food I usually prefer Thali and Indian Vegetarian food places",node_set=["food"])
    await cognee.cognify()
    await cognee.memify()

    results = await cognee.search("plan 3 days Itinerary for Rome based on my preference")

    for result in results:
        print(result)

if __name__ == '__main__':
    asyncio.run(main())