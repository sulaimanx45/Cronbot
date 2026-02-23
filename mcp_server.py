from pathlib import Path
import asyncio
from datetime import datetime
import time
from cron import CronService, CronSchedule
from fastmcp import FastMCP

mcp = FastMCP("cron-reminder-server")

async def handle_job(job):
    """What happens when a job runs"""
    message = job.payload.message
    if not message:
        print("No message provided.")
        return
    print(f"\n Reminder: {message}")

cron = CronService(
    store_path=Path("cron_store.json"),
    on_job=handle_job)

async def startup():
    await cron.start()

@mcp.tool()
async def add_job(name: str, schedule_type: str, value: str, message: str) -> str:
    """
    Add a new reminder job.

    schedule_type must be one of:
    - "every" → run repeatedly every N seconds (value = seconds)
    - "after" → run once after N seconds from now (value = seconds)
    - "at" → run once at a specific date & time
             (value format: "DD Mon YYYY HH:MM")
    """

    if schedule_type == "every":
        schedule = CronSchedule(
            kind="every",
            every_ms=int(value) * 1000
        )

    elif schedule_type == "after":
        at_ms = int(time.time() * 1000) + int(value) * 1000
        schedule = CronSchedule(
            kind="at",
            at_ms=at_ms
        )

    elif schedule_type == "at":
        dt = datetime.strptime(value, "%d %b %Y %H:%M")
        schedule = CronSchedule(
            kind="at",
            at_ms=int(dt.timestamp() * 1000)
        )

    else:
        raise ValueError("Invalid schedule_type")

    job = cron.add_job(
        name=name,
        schedule=schedule,
        message=message
    )

    return {'id':job.id, 'name':job.name}


@mcp.tool()
async def list_jobs() -> list:
    """
    List all jobs in the scheduler.
    
    """

    jobs = cron.list_jobs(include_disabled=True)

    return [
        {
            "id": j.id,
            "name": j.name,
            "next_run_at_ms": j.state.next_run_at_ms
        }
        for j in jobs
    ]


@mcp.tool()
async def delete_job(job_id: str) -> bool:
    """
    Delete a job by its ID.

    """

    return {'job removed':cron.remove_job(job_id)}


@mcp.tool()
async def update_job(
    job_id: str,
    name: str,
    schedule_type: str,
    value: str,
    message: str
) -> bool:
    """
    Update an existing job completely (title, schedule, and message).

    The old job is removed and replaced with a new one.

    schedule_type rules are the same as add_job().
    """

    if not cron.remove_job(job_id):
        return False

    # Recreate job with new parameters
    new_id = await add_job(name, schedule_type, value, message)

    return new_id is not None


if __name__ == "__main__":
    asyncio.run(startup()) 
    mcp.run(host="0.0.0.0", port=8000, transport="sse")