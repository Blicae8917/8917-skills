#!/usr/bin/env python3
import sys
import argparse
import os
import requests
from minimax_client import MinimaxClient, get_standard_path

VIDEO_AGENT_TEMPLATES = {
    "diving": {"id": "392753057216684038", "name": "跳水", "desc": "上传图片，生成图中主体完成完美跳水动作的视频", "media_required": True, "text_required": False},
    "rings": {"id": "393881433990066176", "name": "吊环", "desc": "上传宠物照片，生成宠物完成完美吊环动作的视频", "media_required": True, "text_required": False},
    "pubg": {"id": "393769180141805569", "name": "绝地求生", "desc": "上传宠物图片并输入野兽种类，生成宠物野外绝地求生视频", "media_required": True, "text_required": True},
    "labubu": {"id": "394246956137422856", "name": "万物皆可 labubu", "desc": "上传人物/宠物照片，生成 labubu 换脸视频", "media_required": True, "text_required": False},
    "mcdonalds": {"id": "393879757702918151", "name": "麦当劳宠物外卖员", "desc": "上传爱宠照片，生成麦当劳宠物外卖员视频", "media_required": True, "text_required": False},
    "tibetan": {"id": "393766210733957121", "name": "藏族风写真", "desc": "上传面部参考图，生成藏族风视频写真", "media_required": True, "text_required": False},
    "dead": {"id": "394125185182695432", "name": "生无可恋", "desc": "输入各类主角痛苦表情，一键生成角色痛苦生活的小动画", "media_required": False, "text_required": True},
    "love_letter": {"id": "393857704283172864", "name": "情书写真", "desc": "上传照片生成冬日雪景写真", "media_required": True, "text_required": False},
    "female_model": {"id": "393866076583718914", "name": "女模特试穿广告", "desc": "上传服装图片，生成女模特试穿广告", "media_required": True, "text_required": False},
    "four_seasons": {"id": "398574688191234048", "name": "四季写真", "desc": "上传人脸照片生成四季写真", "media_required": True, "text_required": False},
    "male_model": {"id": "393876118804459526", "name": "男模特试穿广告", "desc": "上传服装图片，生成男模特试穿广告", "media_required": True, "text_required": False}
}


def main():
    parser = argparse.ArgumentParser(description="Generate video using MiniMax Video Agent templates")
    parser.add_argument("template", help=f"Template name: {', '.join(VIDEO_AGENT_TEMPLATES.keys())}")
    parser.add_argument("--media", help="Path to input image file (for templates requiring image)")
    parser.add_argument("--text", help="Text input (for templates that need text)")
    parser.add_argument("--project", help="Project name for sub-directory storage")
    parser.add_argument("--output-dir", help="Override output root directory")
    parser.add_argument("--estimate", action="store_true", help="Only estimate cost, don't execute")
    args = parser.parse_args()

    if args.template not in VIDEO_AGENT_TEMPLATES:
        print(f"Error: Unknown template '{args.template}'")
        print(f"Available templates: {', '.join(VIDEO_AGENT_TEMPLATES.keys())}")
        sys.exit(1)

    tmpl = VIDEO_AGENT_TEMPLATES[args.template]
    if tmpl["media_required"] and not args.media:
        print(f"Error: Template '{tmpl['name']}' requires an image file (--media)")
        sys.exit(1)
    if tmpl["text_required"] and not args.text:
        print(f"Error: Template '{tmpl['name']}' requires text input (--text)")
        sys.exit(1)

    try:
        client = MinimaxClient()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(client.get_budget_report("MiniMax-Hailuo-02-512P-6s"))
    print(f"模板: {tmpl['name']} - {tmpl['desc']}")
    print("⚠️ 视频链接有效期: 9小时，请生成后立即下载！")
    if args.estimate:
        sys.exit(0)

    data = {"template_id": tmpl["id"]}

    if args.media:
        print(f"上传素材: {args.media}")
        with open(args.media, "rb") as media_file:
            files = {"file": media_file}
            upload_resp = requests.post(
                f"{client.base_url}/v1/files/upload",
                headers={"Authorization": f"Bearer {client.api_key}"},
                files=files
            )
        upload_resp.raise_for_status()
        file_id = upload_resp.json().get("data", {}).get("file_id")
        if not file_id:
            print(f"Error: Upload failed - {upload_resp.text}")
            sys.exit(1)
        data["media_inputs"] = [{"type": "image", "file_id": file_id}]
        print(f"素材上传成功: file_id={file_id}")

    if args.text:
        data["text_inputs"] = [{"text": args.text}]

    print("创建视频模板任务...")
    resp = client.post("video_generation/video_agent", data)

    if resp.get("base_resp", {}).get("status_code") == 0:
        task_id = resp.get("task_id")
        print(f"✅ 任务已创建! Task ID: {task_id}")
        target_dir, filename_base = get_standard_path("VID", project=args.project, prompt_slug=args.template, output_dir=args.output_dir)
        print(f"建议输出目录: {os.path.join(target_dir, filename_base + '.mp4')}")
        print("请等待处理，完成后使用 task_id 查询结果并立即下载。")
    else:
        print(f"Error: {resp}")


if __name__ == "__main__":
    main()
