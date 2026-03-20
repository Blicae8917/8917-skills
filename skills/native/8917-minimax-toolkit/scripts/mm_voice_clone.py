#!/usr/bin/env python3
import sys
import argparse
import os
import requests
from minimax_client import MinimaxClient


def main():
    parser = argparse.ArgumentParser(description="Clone a voice using MiniMax Voice Clone")
    parser.add_argument("audio", help="Path to audio file to clone (mp3/m4a/wav, recommended 30s+)")
    parser.add_argument("--prompt-audio", help="Optional: Path to sample audio for quality enhancement")
    parser.add_argument("--voice-id", required=True, help="Custom voice ID to assign (e.g. commander-voice)")
    parser.add_argument("--estimate", action="store_true", help="Only estimate cost, don't execute")
    args = parser.parse_args()

    if not os.path.exists(args.audio):
        print(f"Error: Audio file not found: {args.audio}")
        sys.exit(1)
    if args.prompt_audio and not os.path.exists(args.prompt_audio):
        print(f"Error: Prompt audio file not found: {args.prompt_audio}")
        sys.exit(1)

    try:
        client = MinimaxClient()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print("[MiniMax Voice Clone]")
    print("预计消耗: 克隆本身免费，首次使用合成时按语音合成费率扣费")
    print("⚠️ 克隆音色有效期: 7天（168小时），期间需至少调用一次语音合成以保留")
    print(f"Key 来源: {client.key_source}")

    if args.estimate:
        print("克隆步骤预览:")
        print(f"1. 上传音频: {args.audio}")
        if args.prompt_audio:
            print(f"2. 上传示例音频: {args.prompt_audio}")
        print(f"3. 调用克隆接口，voice_id={args.voice_id}")
        sys.exit(0)

    mime_map = {"mp3": "audio/mpeg", "m4a": "audio/mp4", "wav": "audio/wav"}

    print(f"[Step 1] 上传待克隆音频: {args.audio}")
    ext = os.path.splitext(args.audio)[1].lower().lstrip('.')
    mime = mime_map.get(ext, "audio/mpeg")
    with open(args.audio, "rb") as f:
        files = {"file": (os.path.basename(args.audio), f, mime)}
        resp = requests.post(
            f"{client.base_url}/voice/clone/upload",
            headers={"Authorization": f"Bearer {client.api_key}"},
            files=files
        )
    data = resp.json()
    if data.get("base_resp", {}).get("status_code") != 0:
        print(f"Error uploading clone audio: {data}")
        sys.exit(1)
    clone_file_id = data.get("data", {}).get("file_id")
    print(f"✅ 待克隆音频上传成功: file_id={clone_file_id}")

    prompt_file_id = None
    if args.prompt_audio:
        print(f"[Step 2] 上传示例音频: {args.prompt_audio}")
        ext2 = os.path.splitext(args.prompt_audio)[1].lower().lstrip('.')
        mime2 = mime_map.get(ext2, "audio/mpeg")
        with open(args.prompt_audio, "rb") as f:
            files2 = {"file": (os.path.basename(args.prompt_audio), f, mime2)}
            resp2 = requests.post(
                f"{client.base_url}/voice/clone/upload_prompt",
                headers={"Authorization": f"Bearer {client.api_key}"},
                files=files2
            )
        data2 = resp2.json()
        if data2.get("base_resp", {}).get("status_code") != 0:
            print(f"Error uploading prompt audio: {data2}")
            sys.exit(1)
        prompt_file_id = data2.get("data", {}).get("file_id")
        print(f"✅ 示例音频上传成功: file_id={prompt_file_id}")

    print("[Step 3] 执行音色克隆...")
    clone_data = {
        "model": "speech-2.8-hd",
        "voice_id": args.voice_id,
        "clone_audio": {"file_id": clone_file_id}
    }
    if prompt_file_id:
        clone_data["clone_prompt"] = {"prompt_audio": {"file_id": prompt_file_id}}

    clone_resp = requests.post(
        f"{client.base_url}/voice/clone",
        headers={"Authorization": f"Bearer {client.api_key}", "Content-Type": "application/json"},
        json=clone_data
    )
    clone_result = clone_resp.json()

    if clone_result.get("base_resp", {}).get("status_code") == 0:
        print("\n✅ 音色克隆成功!")
        print(f"Voice ID: {args.voice_id}")
        print("⚠️ 重要提醒:")
        print("1. 此音色为临时音色，7天内需至少调用一次语音合成才能永久保留")
        print(f"2. 使用方式: python3 scripts/mm_speech.py '...' --voice {args.voice_id}")
    else:
        print(f"Error: {clone_result}")


if __name__ == "__main__":
    main()
