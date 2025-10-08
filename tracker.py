import os
import time
import base64
from datetime import datetime

import pandas as pd
import pyautogui
import schedule
from dotenv import load_dotenv

# OpenAI SDK v1.x
from openai import OpenAI


def ensure_directories(screenshot_dir: str, report_dir: str) -> None:
    os.makedirs(screenshot_dir, exist_ok=True)
    os.makedirs(report_dir, exist_ok=True)


def initialize_log(log_file: str) -> None:
    if not os.path.exists(log_file):
        pd.DataFrame(columns=["timestamp", "screenshot_path", "summary"]).to_csv(
            log_file, index=False
        )


def capture_screenshot(screenshot_dir: str) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filepath = os.path.join(screenshot_dir, f"{timestamp}.png")
    image = pyautogui.screenshot()
    image.save(filepath)
    print(f"[+] Screenshot saved: {filepath}")
    return filepath


def encode_image_to_base64(filepath: str) -> str:
    with open(filepath, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def summarize_image_with_openai(client: OpenAI, image_path: str) -> str:
    try:
        b64_image = encode_image_to_base64(image_path)
        # Using the new Responses API style for image input
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a productivity tracker assistant."},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Summarize what task this screenshot shows. Be concise."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{b64_image}",
                            },
                        },
                    ],
                },
            ],
        )
        summary = response.choices[0].message.content.strip()
        print(f"[AI] {summary}")
        return summary
    except Exception as e:
        print(f"[Error] Failed to summarize screenshot: {e}")
        return "AI summary unavailable"


def append_activity_log(log_file: str, screenshot_path: str, summary: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        df = pd.read_csv(log_file)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["timestamp", "screenshot_path", "summary"])
    df.loc[len(df)] = [timestamp, screenshot_path, summary]
    df.to_csv(log_file, index=False)
    print(f"[\u2713] Activity logged at {timestamp}\n")


def generate_report_file(log_file: str, report_dir: str) -> str:
    try:
        df = pd.read_csv(log_file)
    except FileNotFoundError:
        print("No activity logged yet.")
        return ""

    if df.empty:
        print("No activity logged yet.")
        return ""

    report_name = f"report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    report_path = os.path.join(report_dir, report_name)

    summaries = "\n".join(
        f"- {row['timestamp']}: {row['summary']}" for _, row in df.iterrows()
    )

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("=== Productivity Report ===\n")
        f.write(f"Generated on: {datetime.now()}\n\n")
        f.write(summaries)

    print(f"[\ud83d\udcc4] Report generated: {report_path}")
    return report_path


def main() -> None:
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("[Error] OPENAI_API_KEY not found in environment. Set it in .env.")
        return

    client = OpenAI(api_key=api_key)

    SCREENSHOT_DIR = "screenshots"
    REPORT_DIR = "reports"
    LOG_FILE = os.path.join(REPORT_DIR, "activity_log.csv")

    ensure_directories(SCREENSHOT_DIR, REPORT_DIR)
    initialize_log(LOG_FILE)

    def job() -> None:
        path = capture_screenshot(SCREENSHOT_DIR)
        summary = summarize_image_with_openai(client, path)
        append_activity_log(LOG_FILE, path, summary)

    schedule.every(15).minutes.do(job)
    print("\ud83d\udfe2 Productivity Tracker running... Press Ctrl+C to stop.")

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n[!] Stopped by user. Generating final report...")
        generate_report_file(LOG_FILE, REPORT_DIR)


if __name__ == "__main__":
    main()



