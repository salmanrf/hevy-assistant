from typing import Annotated
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig


@tool()
async def find_workout_routine(
    keyword: Annotated[
        str, "Name of the routine, e.g: Upper Body, Lower Body, Push, Pull, Legs, etc"
    ],
    config: RunnableConfig,
):
    """Find user's workout routine or program
    Use this when you need detailed information about specific workout routine/program
    """
    # configuration = config.get("configurable", {})

    routine = {
        "title": "Push",
        "exercises": [
            {
                "title": "Bench Press (Dumbbell)",
                "sets": [
                    {"type": "warmup", "weight_in_kg": 20, "reps": 8},
                    {"type": "warmup", "weight_in_kg": 30, "reps": 4},
                    {"type": "warmup", "weight_in_kg": 35, "reps": 2},
                    {"type": "failure_set", "weight_in_kg": 40, "reps": 5},
                    {"type": "failure_set", "weight_in_kg": 35, "reps": 5},
                ],
            },
        ],
    }

    return routine
