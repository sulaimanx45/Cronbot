import asyncio
import subprocess
import time
from pathlib import Path
from datetime import datetime
from cron import CronService, CronSchedule

async def handle_job(job):
    command = job.payload.message
    if not command:
        print("No message/command provided for this job.")
        return

    if command.endswith(".py") or any(c in command for c in (" ", "/", "\\")):
        try:
            subprocess.run(command, shell=True, check=True)
            print(f"Command executed successfully: {command}")
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {e}")
    else:
        print(f"Reminder: {command}")

async def main():
    cron = CronService(
        store_path=Path("cron_store.json"),
        on_job=handle_job
    )
    await cron.start()

    print("Cron Job Creator")
    while True:
        name = input("\nEnter job name (or 'exit'): ")
        if name.lower() == "exit":
            break

        kind = input("Enter job type ('every' or 'at'): ").strip().lower()
        if kind not in ["every", "at"]:
            print("Invalid type! Must be 'every' or 'at'.")
            continue

        if kind == "every":
            seconds = input("Enter interval in seconds: ")
            try:
                seconds_int = int(float(seconds))
                if seconds_int <= 0:
                    print("Time must be greater than 0!")
                    continue
            except ValueError:
                print("Invalid number!")
                continue

            schedule = CronSchedule(kind="every", every_ms=seconds_int * 1000)

        else: 
            method = input("Schedule by (1) seconds from now or (2) absolute date/time? [1/2]: ").strip()
            if method == "1":
                seconds = input("Enter time in seconds from now: ")
                try:
                    seconds_int = int(float(seconds))
                    if seconds_int <= 0:
                        print("Time must be greater than 0!")
                        continue
                except ValueError:
                    print("Invalid number!")
                    continue

                at_ms = int(time.time() * 1000) + seconds_int * 1000
                schedule = CronSchedule(kind="at", at_ms=at_ms)

            elif method == "2":
                time_input = input("Enter time (e.g., 20 Feb 2026 09:00): ")
                try:
                    dt = datetime.strptime(time_input, "%d %b %Y %H:%M")
                    at_ms = int(dt.timestamp() * 1000)
                    schedule = CronSchedule(kind="at", at_ms=at_ms)
                except ValueError:
                    print("Invalid format! Use DD Mon YYYY HH:MM (e.g., 20 Feb 2026 09:00)")
                    continue
            else:
                print("Invalid choice! Must be 1 or 2.")
                continue

        message = input("Enter reminder text, script path, or shell command to run: ").strip()
        if not message:
            print("Message/command cannot be empty!")
            continue

        job = cron.add_job(
            name=name,
            schedule=schedule,
            message=message
        )
        print(f"'{job.name}' added!")
    print("Scheduler is running. Press Ctrl+C to stop.")
    while True:
        await asyncio.sleep(1)
asyncio.run(main())