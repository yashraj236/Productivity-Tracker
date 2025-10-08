## Productivity Tracker (Windows, Local, AI Summaries)

Local Python app that periodically captures screenshots, summarizes them with an AI vision model, and logs summaries for a simple activity report.

### Features
- Periodic screenshots (default every 15 minutes)
- AI (OpenAI) vision summarization
- CSV activity log and on-demand report generation
- Runs locally on Windows

### Prerequisites
- Python 3.10+
- Windows with screen access (disable Focus Assist for screenshots if needed)

### Setup
1. Clone/download this folder.
2. Create and activate a virtual environment (recommended).
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Copy `.env.example` to `.env` and set your key:
```bash
OPENAI_API_KEY=YOUR_OPENAI_API_KEY_HERE
```

### Run
```bash
python tracker.py
```
The app will:
- Create `screenshots/` and `reports/`
- Save screenshots to `screenshots/`
- Append entries to `reports/activity_log.csv`
- On Ctrl+C, generate a text report in `reports/`

### Configuration
- Screenshot/report folders: `screenshots/`, `reports/`
- Schedule: 15 minutes (change in `tracker.py` where `schedule.every(15).minutes` is set)

### Notes for Windows
- If you see errors capturing the screen, ensure the session is not locked or minimized to a virtual desktop.
- Use `pythonw.exe` to run without a console window.

### Auto-start (Optional)
Use Task Scheduler:
1. Open Task Scheduler → Create Basic Task
2. Trigger: At startup or Daily at a chosen time
3. Action: Start a Program
   - Program/script: `pythonw.exe`
   - Arguments: Absolute path to `tracker.py`
   - Start in: Project directory path

### Privacy
- All screenshots remain local; the app sends only encoded images to the AI API for summarization. Delete entries or screenshots as needed.

### Example outputs
- `reports/activity_log.csv`:
```
timestamp,screenshot_path,summary
2025-10-08 10:30:00,screenshots/2025-10-08_10-30-00.png,Working on Java Spring Boot project
```
- Report file: `reports/report_YYYY-MM-DD_HH-MM-SS.txt`



