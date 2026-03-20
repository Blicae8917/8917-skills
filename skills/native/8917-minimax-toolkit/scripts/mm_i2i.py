#!/usr/bin/env python3
import sys
import argparse
import os
import requests
from minimax_client import MinimaxClient, get_standard_path


def main():
    parser = argparse.ArgumentParser(description="Generate image from reference image (I2I) using MiniMax image-01")
    parser.add_argument("prompt", help="Text prompt describing the desired output style")
    parser.add_argument("--ref", required=True, help="Path to reference image")
    parser.add_argument("--model", default="image-01", choices=["image-01", "image-01-live"], help="Model name")
    parser.add_argument("--style", help="Style type (for image-01-live): 漫画, 元气, 中世纪, 水彩")
    parser.add_argument("--ratio", default="1:1", help="Aspect ratio")
    parser.add_argument("--project", help="Project name for sub-directory storage")
    parser.add_argument("--output-dir", help="Override output root directory")
    parser.add_argument("--estimate", action="store_true", help="Only estimate cost, don't execute")
    args = parser.parse_args()

    try:
        client = MinimaxClient()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(client.get_budget_report(args.model))
    if args.estimate:
        sys.exit(0)

    print(f"上传参考图: {args.ref}")
    with open(args.ref, "rb") as f:
        files = {"file": (os.path.basename(args.ref), f, "image/jpeg")}
        upload_resp = requests.post(
            f"{client.base_url}/files/upload",
            headers={"Authorization": f"Bearer {client.api_key}"},
            files=files
        )

    upload_data = upload_resp.json()
    if upload_data.get("base_resp", {}).get("status_code") != 0:
        print(f"Error uploading file: {upload_data}")
        sys.exit(1)

    file_id = upload_data.get("data", {}).get("file_id")
    print(f"参考图上传成功: file_id={file_id}")

    data = {
        "model": args.model,
        "prompt": args.prompt,
        "aspect_ratio": args.ratio,
        "response_format": "url",
        "image_urls": [f"file_id://{file_id}"]
    }

    if args.model == "image-01-live" and args.style:
        data["style"] = {"style_type": args.style, "style_weight": 0.8}

    print(f"生成图片: {args.prompt}...")
    resp = client.post("image_generation", data)

    if resp.get("base_resp", {}).get("status_code") == 0:
        url = resp["data"]["image_urls"][0]
        target_dir, filename_base = get_standard_path("IMG", project=args.project, prompt_slug=args.prompt, output_dir=args.output_dir)
        filepath = os.path.join(target_dir, f"{filename_base}.jpg")

        img_data = requests.get(url).content
        with open(filepath, 'wb') as f:
            f.write(img_data)

        client.print_saved_result(filepath, "Image", project=args.project)
        print(f"MEDIA:{filepath}")
    else:
        print(f"Error: {resp}")


if __name__ == "__main__":
    main()
