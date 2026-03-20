#!/usr/bin/env python3
import sys
import argparse
import os
import requests
import time
from minimax_client import MinimaxClient, get_standard_path


def main():
    parser = argparse.ArgumentParser(description="Asynchronous long-text speech synthesis (up to 1M characters)")
    parser.add_argument("text_or_file", help="Text to synthesize, or path to a .txt file")
    parser.add_argument("--voice", default="male-qn-qingse", help="Voice ID")
    parser.add_argument("--speed", type=float, default=1.0, help="Speech speed (0.5-2.0)")
    parser.add_argument("--format", default="mp3", choices=["mp3", "pcm", "flac", "wav"], help="Audio format")
    parser.add_argument("--project", help="Project name for sub-directory storage")
    parser.add_argument("--output-dir", help="Override output root directory")
    parser.add_argument("--estimate", action="store_true", help="Only estimate cost, don't execute")
    args = parser.parse_args()

    if os.path.isfile(args.text_or_file):
        with open(args.text_or_file, 'r', encoding='utf-8') as f:
            text = f.read()
        print(f"Loaded text from file: {args.text_or_file} ({len(text)} chars)")
    else:
        text = args.text_or_file

    try:
        client = MinimaxClient()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(client.get_budget_report("async-speech-2.8-hd", text_len=len(text)))
    if len(text) > 10000:
        print("⚠️ 超长文本，将使用异步任务模式，结果需轮询获取")
    if args.estimate:
        sys.exit(0)

    data = {
        "model": "speech-2.8-hd",
        "text": text[:100000],
        "stream": False,
        "voice_setting": {
            "voice_id": args.voice,
            "speed": args.speed,
            "vol": 1.0,
            "pitch": 0
        },
        "output_format": "url"
    }

    if len(text) > 10000:
        print("使用异步模式创建任务...")
        resp = client.post("t2a_v2/async", data)
    else:
        resp = client.post("t2a_v2", data)

    if resp.get("base_resp", {}).get("status_code") == 0:
        if "task_id" in resp:
            task_id = resp["task_id"]
            print(f"✅ 异步任务已创建! Task ID: {task_id}")
            print("轮询任务状态中（长文本可能需要几分钟）...")
            while True:
                time.sleep(20)
                status_resp = client.get(f"t2a_v2/async/query?task_id={task_id}")
                status = status_resp.get("data", {}).get("status")
                if status == 2:
                    file_id = status_resp.get("data", {}).get("file_id")
                    print(f"✅ 合成完成! file_id={file_id}")
                    download_resp = client.get(f"files/retrieve_content?file_id={file_id}")
                    if download_resp.get("base_resp", {}).get("status_code") == 0:
                        audio_url = download_resp.get("data", {}).get("audio_url")
                        if audio_url:
                            target_dir, filename_base = get_standard_path("TTS", project=args.project, prompt_slug="async_speech", output_dir=args.output_dir)
                            filepath = os.path.join(target_dir, f"{filename_base}.{args.format}")
                            audio_data = requests.get(audio_url).content
                            with open(filepath, 'wb') as f:
                                f.write(audio_data)
                            client.print_saved_result(filepath, "Speech", project=args.project)
                            print(f"MEDIA:{filepath}")
                    break
                elif status == 1:
                    print(f"仍在处理中... (task_id={task_id})")
                else:
                    print(f"任务状态异常: {status_resp}")
                    break
        else:
            url = resp["data"]["audio"]
            target_dir, filename_base = get_standard_path("TTS", project=args.project, prompt_slug="speech", output_dir=args.output_dir)
            filepath = os.path.join(target_dir, f"{filename_base}.{args.format}")
            audio_data = requests.get(url).content
            with open(filepath, 'wb') as f:
                f.write(audio_data)
            client.print_saved_result(filepath, "Speech", project=args.project)
            print(f"MEDIA:{filepath}")
    else:
        print(f"Error: {resp}")


if __name__ == "__main__":
    main()
