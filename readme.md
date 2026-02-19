# Python Cron Scheduler

A lightweight **Python cron scheduler** for running reminders, Python scripts, or shell commands at specific times or repeated intervals.

This project is **JSON-based** and does not require a full database. Jobs are persisted in `cron_store.json`.

---

## Features

* Schedule jobs **at a specific time** or **repeatedly** at intervals.
* Run **Python scripts** or **shell commands** automatically.
* Store job details persistently in `cron_store.json`.
* Supports absolute date/time scheduling or seconds-based intervals.
* Logs job execution status and errors in the terminal.

---

## Requirements

* Python 3.10+
* Packages:

```bash
pip install croniter loguru
```


---

## Project Structure

```
cron_project/
├── cron/                  # Cron service module
│   ├── __init__.py
│   ├── service.py         # CronService class
│   └── types.py           # Job and schedule data classes
├── example_main.py        # CLI for creating and running jobs
└── cron_store.json        # Job persistence file (created automatically)
```

---

## Usage

1. **Run the scheduler**

```bash
python main.py
```

2. **Create jobs via input prompt**

* **Job name:** Name of your job
* **Job type:** `every` (interval) or `at` (specific time)
* **Time / interval:**

  * `every` → seconds between runs
  * `at` → seconds from now **or** absolute datetime (format: `DD Mon YYYY HH:MM`)
* **Command / script:** Python script path or shell command

3. **Example inputs**

```
Job name: Reminder
Job type: every
Interval (seconds): 10
Command: echo "Drink water!"
```

```
Job name: Python Test
Job type: at
Schedule by: 2 (absolute date/time)
Date/time: 20 Feb 2026 09:00
Command: python test.py
```


5. **Exiting input mode**

* Type `exit` as the job name.
* Scheduler continues running until you press `Ctrl+C`.

---

## Customization

* Change `cron_store.json` path in `main.py`:

```python
cron = CronService(store_path=Path("my_cron_store.json"), on_job=handle_job)
```

* Modify `handle_job()` to customize how jobs are executed (Python scripts, shell commands, reminders, API calls, etc.).

---

## Notes

* **Python scripts:** For Windows paths with spaces, enclose in quotes:

  ```
  python "C:\Program Files\Scripts\test.py"
  ```
* **Persistence:** All jobs are saved in `cron_store.json` automatically.
* **Intervals:** Minimum 1 second interval for `every` type.

---

## Future Improvements

* Replace JSON with a database (SQLite, MongoDB, Redis) for better scalability.
* Add a **web dashboard** to manage cron jobs.
* Support **distributed cron jobs** across multiple machines.

---

## License

MIT License
