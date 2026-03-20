import os
import json
import requests
import re
from pathlib import Path


class MinimaxClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("MINIMAX_API_KEY")
        self.key_source = "MINIMAX_API_KEY"
        if not self.api_key:
            self.api_key = self._get_key_from_openclaw()
            self.key_source = "~/.openclaw/openclaw.json (MiniMax Token Plan API Key)"

        if not self.api_key:
            raise ValueError(
                "MiniMax Token Plan API Key not found. Configure MINIMAX_API_KEY or add the MiniMax Token Plan key to ~/.openclaw/openclaw.json."
            )

        self.base_url = "https://api.minimaxi.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _get_key_from_openclaw(self):
        config_path = os.path.expanduser("~/.openclaw/openclaw.json")
        if not os.path.exists(config_path):
            return None
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                providers = config.get("models", {}).get("providers", {})
                for name, cfg in providers.items():
                    if "minimax" in name.lower():
                        return cfg.get("apiKey")
        except Exception:
            return None
        return None

    def post(self, endpoint, data):
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def get(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def _load_costs(self):
        with open(os.path.join(os.path.dirname(__file__), "../references/costs.json"), 'r') as f:
            return json.load(f)

    def get_budget_report(self, model_id, text_len=0):
        try:
            costs = self._load_costs()
            rolling_hours = costs.get("rolling_window_hours", 5)
            default_plan = costs.get("default_plan", "Plus-Speed")
            plan_limit = costs["token_plan"].get(default_plan, 1500)

            # Speech in official docs is per generation, capped at 1000 chars each call
            if model_id.lower().startswith("speech-"):
                generations = max(1, (text_len + 999) // 1000)
                unit_cost = costs["models"].get(model_id, 600)
                estimated = generations * unit_cost
                basis = f"{unit_cost} 次请求/每次语音生成（单次上限 1000 字符）"
            elif model_id.lower().startswith("async-speech-"):
                generations = max(1, (text_len + 999) // 1000)
                unit_cost = costs["models"].get(model_id, 450)
                estimated = generations * unit_cost
                basis = f"{unit_cost} 次请求/每次异步语音生成（单次上限 1000 字符）"
            else:
                unit_cost = costs["models"].get(model_id, 1)
                estimated = unit_cost
                basis = f"{unit_cost} 次请求/次"

            report = "\n[Token Plan 预估]\n"
            report += f"模型: {model_id}\n"
            report += f"Key 来源: {self.key_source}\n"
            report += f"预计消耗: {estimated:.0f} 次请求\n"
            report += f"计费依据: {basis}\n"
            report += f"套餐窗口: {rolling_hours} 小时滚动窗口\n"
            report += f"默认参考套餐上限: {default_plan} = {plan_limit} 次请求/{rolling_hours}小时\n"

            if estimated > plan_limit:
                report += "⚠️ 警告: 本次任务预计消耗超过默认参考套餐窗口上限，可能触发额度不足。\n"
            elif estimated >= plan_limit * 0.5:
                report += "💡 提示: 本次任务属于高消耗操作，建议确认当前套餐余量。\n"

            report += "提示: 该 skill 默认使用 MiniMax Token Plan API Key；若 5 小时窗口内触顶，可等待额度恢复或改用按量计费 API Key。\n"
            return report
        except Exception as e:
            return f"\n[Token Plan 预估]\n无法读取套餐信息：{e}\n"

    def print_saved_result(self, filepath, media_type, project=None):
        print("✅ 生成完成")
        print(f"类型: {media_type}")
        print(f"保存位置: {filepath}")
        if project:
            print(f"项目目录: {project}")
        print("提示: 如需长期管理，建议后续按项目整理到明确目录中。")


def get_standard_path(modality, project=None, prompt_slug="", output_dir=None):
    from datetime import datetime

    env_output = os.environ.get("MINIMAX_OUTPUT_DIR")
    cwd = Path(os.getcwd())
    workspace_output = cwd / "workspace" / "03-Resources" / "minimax-output"
    fallback_output = cwd / "outputs" / "minimax"

    if output_dir:
        output_hub = Path(output_dir).expanduser()
    elif env_output:
        output_hub = Path(env_output).expanduser()
    elif (cwd / "workspace").is_dir():
        output_hub = workspace_output
    else:
        output_hub = fallback_output

    modality_map = {
        "IMG": "Images",
        "VID": "Videos",
        "TTS": "Speech",
        "MSC": "Music"
    }

    sub_folder = modality_map.get(modality, "Other")
    target_dir = output_hub / project / sub_folder if project else output_hub / sub_folder
    target_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_slug = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fa5]', '-', prompt_slug[:30]).strip('-').lower()
    filename_base = f"{timestamp}_{modality}_{clean_slug}" if clean_slug else f"{timestamp}_{modality}"

    return str(target_dir), filename_base
