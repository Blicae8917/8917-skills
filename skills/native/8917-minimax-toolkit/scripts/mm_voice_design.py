#!/usr/bin/env python3
import sys
import argparse
import requests
from minimax_client import MinimaxClient


def main():
    parser = argparse.ArgumentParser(description="Design a new voice using text description via MiniMax Voice Design API")
    parser.add_argument("description", help="Text description of the desired voice")
    parser.add_argument("--model", default="speech-02-hd", help="Model to use (recommended: speech-02-hd)")
    parser.add_argument("--lang", default="auto", help="Language: auto, Chinese, English, Japanese, Korean, etc.")
    parser.add_argument("--estimate", action="store_true", help="Only show info, don't execute")
    args = parser.parse_args()

    try:
        client = MinimaxClient()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print("[MiniMax Voice Design]")
    print(f"描述: {args.description}")
    print("预计消耗: 按语音合成费率，首次使用此音色时扣费")
    print("⚠️ 生成音色有效期: 7天（168小时），期间需至少调用一次语音合成以保留")
    print(f"Key 来源: {client.key_source}")

    if args.estimate:
        print("音色设计预览:")
        print(f"1. 输入描述: {args.description}")
        print(f"2. 指定语言: {args.lang}")
        print("3. 系统将返回一个 voice_id 供后续语音合成使用")
        sys.exit(0)

    data = {
        "model": args.model,
        "description": args.description,
        "language": args.lang
    }

    print("正在生成音色...")
    resp = requests.post(
        f"{client.base_url}/v1/voice/design",
        headers={"Authorization": f"Bearer {client.api_key}", "Content-Type": "application/json"},
        json=data
    )
    result = resp.json()

    if result.get("base_resp", {}).get("status_code") == 0:
        voice_data = result.get("data", {})
        voice_id = voice_data.get("voice_id")
        preview_url = voice_data.get("preview_url", "")
        print("\n✅ 音色生成成功!")
        print(f"Voice ID: {voice_id}")
        if preview_url:
            print(f"试听链接: {preview_url}")
        print("⚠️ 重要提醒:")
        print("1. 此音色为临时音色，7天内需至少调用一次语音合成才能永久保留")
        print(f"2. 使用方式: python3 scripts/mm_speech.py '...' --voice {voice_id}")
    else:
        print(f"Error: {result}")


if __name__ == "__main__":
    main()
