import asyncio
import cognee

import os
from dotenv import load_dotenv
load_dotenv() 

DATASET = "agent_sessions"

SAMPLE_PREFERENCES = """\
User travel preferences:
- Likes to visit places near the beach where they can find the best spots.
- Wants locations that are rare to find on blogs — goldmine, off-the-beaten-path places.
- Prefers vegetarian meals; use this for any restaurant recommendation.
- Hobbies that help with itinerary planning: Anime, F1, and Cricket.
"""

async def ingest(data, dataset: str = DATASET) -> None:
    await cognee.serve(
        url=os.getenv("COGNEE_BASE_URL"),
        api_key=os.getenv("COGNEE_API_KEY"),
    )
    try:
        await cognee.remember(data, dataset_name=dataset)
    finally:
        await cognee.disconnect()


async def chat(query: str, dataset: str = DATASET) -> list:
    await cognee.serve(
        url=os.getenv("COGNEE_BASE_URL"),
        api_key=os.getenv("COGNEE_API_KEY"),
    )
    try:
        return await cognee.recall(query, datasets=[dataset])
    finally:
        await cognee.disconnect()

async def main() -> None:
    await ingest(SAMPLE_PREFERENCES) # just once

    query = "Plan a one-day itinerary for Munster, including restaurants to try."

    results = await chat(query)
    print(results[0]['text'])


if __name__ == "__main__":
    asyncio.run(main())