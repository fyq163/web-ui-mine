import os
import pickle
import uuid
import gradio as gr

tasks="""
{
  {
  "goal": "在多个招聘网站上搜索与 data,financial data 相关的工作，并记录下合适的职位。如果看到‘save’或‘star’按钮，请收藏该职位。如果检测到与上一步相同的工作，则自动滚动页面继续浏览。",
  
  "websites": [
    {
      "url": "https://hk.jobsdb.com/",
      "steps": [
        "首先，请检查右上角是否显示您的名字‘Sebastian’，如果显示，说明已经登录，可以直接开始搜索工作。",
        "如果没有登录，请点击顶部右侧的‘Sign in’，输入账户信息并完成验证。",
        "在页面的搜索框（seek）中输入‘Python’，点击搜索按钮获取相关职位。如果看到Recommended for you，请直接scroll down",
        "滚动页面查看职位信息，如果与上一职位相同，请执行‘scroll down’操作。或者执行go back 操作",
        "点击每个职位以查看详细信息，记录下所有合适的职位。如果看到‘save’或‘star’按钮，请点击收藏该职位。THEN, 点击返回按钮返回搜索结果页面，go back action。"
        "继续滚动页面并查看新的职位，直到搜索结果页面结束。If you see any words appear in <disregard_jobs>, please ignore the job."
      ],
      "define_good_job": {
        "criteria": [
          "技能要求包含 Python、MySQL、数据、Azure 或 AI",
          "requires no more than 3 years experiences, 3+ and more just disregard",
          "job location Hong Kong",
          "最好要求至少是毕业生", graduate
        ],
        "disregard_jobs": [
          "hong kong permanent resident only",
          "cantonese is a must or Korean",
          "职位技能需求包含 Java、C# 或 Fortran"
          "4 and more years of experience"
        ]
      },
      "account_info": {
        "username": "seb.fan@outlook.com.au"
      },
      "job_search": {,
        "job_keywords": "data",
        "search_button": "#seek"}}]}

"""
def default_config():
    """Prepare the default configuration"""
    return {
        "agent_type": "custom",
        "max_steps": 100,
        "max_actions_per_step": 3,
        "use_vision": False,
        "tool_calling_method": "auto",
        "llm_provider": "openai",
        "llm_model_name": "gpt-4o",
        "llm_temperature": 1.0,
        "llm_base_url": "",
        "llm_api_key": "",
        "use_own_browser": os.getenv("CHROME_PERSISTENT_SESSION", "false").lower() == "true",
        "keep_browser_open": False,
        "headless": False,
        "disable_security": True,
        "enable_recording": True,
        "window_w": 800,
        "window_h": 1100,
        "save_recording_path": "./tmp/record_videos",
        "save_trace_path": "./tmp/traces",
        "save_agent_history_path": "./tmp/agent_history",
        "task": tasks,
    }


def load_config_from_file(config_file):
    """Load settings from a UUID.pkl file."""
    try:
        with open(config_file, 'rb') as f:
            settings = pickle.load(f)
        return settings
    except Exception as e:
        return f"Error loading configuration: {str(e)}"


def save_config_to_file(settings, save_dir="./tmp/webui_settings"):
    """Save the current settings to a UUID.pkl file with a UUID name."""
    os.makedirs(save_dir, exist_ok=True)
    config_file = os.path.join(save_dir, f"{uuid.uuid4()}.pkl")
    with open(config_file, 'wb') as f:
        pickle.dump(settings, f)
    return f"Configuration saved to {config_file}"


def save_current_config(*args):
    current_config = {
        "agent_type": args[0],
        "max_steps": args[1],
        "max_actions_per_step": args[2],
        "use_vision": args[3],
        "tool_calling_method": args[4],
        "llm_provider": args[5],
        "llm_model_name": args[6],
        "llm_temperature": args[7],
        "llm_base_url": args[8],
        "llm_api_key": args[9],
        "use_own_browser": args[10],
        "keep_browser_open": args[11],
        "headless": args[12],
        "disable_security": args[13],
        "enable_recording": args[14],
        "window_w": args[15],
        "window_h": args[16],
        "save_recording_path": args[17],
        "save_trace_path": args[18],
        "save_agent_history_path": args[19],
        "task": args[20],
    }
    return save_config_to_file(current_config)


def update_ui_from_config(config_file):
    if config_file is not None:
        loaded_config = load_config_from_file(config_file.name)
        if isinstance(loaded_config, dict):
            return (
                gr.update(value=loaded_config.get("agent_type", "custom")),
                gr.update(value=loaded_config.get("max_steps", 100)),
                gr.update(value=loaded_config.get("max_actions_per_step", 3)),
                gr.update(value=loaded_config.get("use_vision", False)),
                gr.update(value=loaded_config.get("tool_calling_method", True)),
                gr.update(value=loaded_config.get("llm_provider", "openai")),
                gr.update(value=loaded_config.get("llm_model_name", "gpt-4o")),
                gr.update(value=loaded_config.get("llm_temperature", 1.0)),
                gr.update(value=loaded_config.get("llm_base_url", "")),
                gr.update(value=loaded_config.get("llm_api_key", "")),
                gr.update(value=loaded_config.get("use_own_browser", False)),
                gr.update(value=loaded_config.get("keep_browser_open", False)),
                gr.update(value=loaded_config.get("headless", False)),
                gr.update(value=loaded_config.get("disable_security", True)),
                gr.update(value=loaded_config.get("enable_recording", True)),
                gr.update(value=loaded_config.get("window_w", 1280)),
                gr.update(value=loaded_config.get("window_h", 1100)),
                gr.update(value=loaded_config.get("save_recording_path", "./tmp/record_videos")),
                gr.update(value=loaded_config.get("save_trace_path", "./tmp/traces")),
                gr.update(value=loaded_config.get("save_agent_history_path", "./tmp/agent_history")),
                gr.update(value=loaded_config.get("task", "")),
                "Configuration loaded successfully."
            )
        else:
            return (
                gr.update(), gr.update(), gr.update(), gr.update(), gr.update(),
                gr.update(), gr.update(), gr.update(), gr.update(), gr.update(),
                gr.update(), gr.update(), gr.update(), gr.update(), gr.update(),
                gr.update(), gr.update(), gr.update(), gr.update(), gr.update(),
                gr.update(), "Error: Invalid configuration file."
            )
    return (
        gr.update(), gr.update(), gr.update(), gr.update(), gr.update(),
        gr.update(), gr.update(), gr.update(), gr.update(), gr.update(),
        gr.update(), gr.update(), gr.update(), gr.update(), gr.update(),
        gr.update(), gr.update(), gr.update(), gr.update(), gr.update(),
        gr.update(), "No file selected."
    )
