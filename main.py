import asyncio
import time
from pathlib import Path
from datetime import datetime
from cron import CronService, CronSchedule

async def handle_job(job):
    """What happens when a job runs"""
    message = job.payload.message
    if not message:
        print("No message provided.")
        return
    print(f"\n Reminder: {message}")

async def main():
    cron = CronService(
        store_path=Path("cron_store.json"),
        on_job=handle_job
    )
    await cron.start()
    while True:
        cmd = await asyncio.to_thread(
            input,
            "\nCommand (add/list/update/delete/exit): "
        )

        if cmd == "exit":
            print("Stopping scheduler...")
            cron.stop()
            return

        elif cmd == "add":
            name = await asyncio.to_thread(input, "Job title: ")
            choice = await asyncio.to_thread(
                input,
                "\nSchedule type:\n"
                "'Every' N seconds\n"
                "'After' N seconds (run once)\n"
                "'At' specific date & time\n")

            if choice.lower() == "every":
                seconds = int(await asyncio.to_thread(input,"Interval in seconds: "))
                schedule = CronSchedule(kind="every",every_ms=seconds * 1000)

            elif choice.lower() == "after":
                seconds = int(await asyncio.to_thread(input,"Run after seconds from now: "))
                at_ms = int(time.time() * 1000) + seconds * 1000
                schedule = CronSchedule(
                    kind="at",
                    at_ms=at_ms)

            elif choice.lower() == "at":
                time_input = await asyncio.to_thread(input,"Enter date & time (e.g., 20 Feb 2026 09:00): ")
                try:
                    dt = datetime.strptime(
                        time_input,
                        "%d %b %Y %H:%M")
                    at_ms = int(dt.timestamp() * 1000)
                    schedule = CronSchedule(
                        kind="at",
                        at_ms=at_ms)
                except ValueError:
                    print("Invalid format.")
                    continue
            else:
                print("Invalid choice.")
                continue

            message = await asyncio.to_thread(input,"Reminder text: ")

            job = cron.add_job(
                name=name,
                schedule=schedule,
                message=message)
            print(f"Added job '{job.name}'")

        elif cmd == "list":
            jobs = cron.list_jobs(include_disabled=True)
            if not jobs:
                print("No jobs found.")
            else:
                print("\nJobs:")
                for j in jobs:
                    print(
                        f"{j.id} | {j.name}"
                        f" | next={j.state.next_run_at_ms}")

        elif cmd == "update":

            job_id = await asyncio.to_thread(input, "Enter job ID: ")

            name = await asyncio.to_thread(
                input,
                "New title (leave empty to keep same): "
            )

            choice = await asyncio.to_thread(
                input,
                "\nNew schedule type:\n"
                "'Every' N seconds\n"
                "'After' N seconds (run once)\n"
                "'At' specific date & time\n"
                "(leave empty to keep same)\n"
            )

            schedule = None

            if choice.lower() == "every":
                seconds = int(await asyncio.to_thread(
                    input,
                    "Interval in seconds: "
                ))
                schedule = CronSchedule(
                    kind="every",
                    every_ms=seconds * 1000
                )

            elif choice.lower() == "after":
                seconds = int(await asyncio.to_thread(
                    input,
                    "Run after seconds from now: "
                ))
                at_ms = int(time.time() * 1000) + seconds * 1000
                schedule = CronSchedule(
                    kind="at",
                    at_ms=at_ms
                )

            elif choice.lower() == "at":
                time_input = await asyncio.to_thread(
                    input,
                    "Enter date & time (e.g., 20 Feb 2026 09:00): "
                )
                try:
                    dt = datetime.strptime(
                        time_input,
                        "%d %b %Y %H:%M"
                    )
                    at_ms = int(dt.timestamp() * 1000)
                    schedule = CronSchedule(
                        kind="at",
                        at_ms=at_ms
                    )
                except ValueError:
                    print("Invalid format.")
                    continue

            message = await asyncio.to_thread(
                input,
                "New reminder text (leave empty to keep same): "
            )

            updated = cron.update_job(
                job_id=job_id,
                name=name if name else None,
                schedule=schedule,
                message=message if message else None
            )

            if updated:
                print("Job updated successfully.")
            else:
                print("Job not found.")
        elif cmd == "delete":
            job_id = input("Enter job ID: ") 
            if cron.remove_job(job_id): 
                print("Job removed.") 
            else: 
                print("Job not found.")
        else:
            print("Unknown command.")

asyncio.run(main())