"""Configuration: provider endpoints, model IDs and defaults.

Every value can be overridden by an environment variable or by motion/config.json, because model IDs
change faster than this code. Check the IDs against your provider's model list before a paid run.
"""
import json
import os

DEFAULTS = {
    # OpenAI Images API. gpt-image-2 was released on 21 April 2026.
    "openai_base": "https://api.openai.com/v1",
    "image_model": "gpt-image-2",
    "image_size_draft": "1536x1024",
    "image_quality_draft": "low",
    "image_quality_final": "high",
    # Seedance 2.0 on BytePlus ModelArk. Volcengine Ark (China) uses https://ark.cn-beijing.volces.com/api/v3
    # and doubao-seedance-2-0-260128. A first-party Seedance 2.5 ID was not in the public ModelArk catalogue
    # at the time of writing; set FMOTION_VIDEO_MODEL when your account lists one.
    "ark_base": "https://ark.ap-southeast.bytepluses.com/api/v3",
    "video_model": "dreamina-seedance-2-0-260128",
    "video_model_draft": "dreamina-seedance-2-0-fast-260128",
    "video_resolution_draft": "480p",
    "video_resolution_final": "1080p",
    # Kling. The international API host is api-singapore.klingai.com. The access-key API's model_name list
    # tops out at kling-v3; newer IDs (kling-3.0-turbo, kling-v3-omni) sit on Kling's newer endpoints, which
    # this adapter does not call yet. Override FMOTION_KLING_MODEL with any ID your account lists.
    "kling_base": "https://api-singapore.klingai.com",
    "kling_model": "kling-v3",
    "kling_mode_draft": "std",
    "kling_mode_final": "pro",
    "kling_cfg_scale": 0.5,
    "video_provider": "seedance",
    "poll_seconds": 10,
    "poll_timeout_seconds": 1800,
}

ENV = {
    "openai_base": "FMOTION_OPENAI_BASE",
    "image_model": "FMOTION_IMAGE_MODEL",
    "ark_base": "FMOTION_ARK_BASE",
    "video_model": "FMOTION_VIDEO_MODEL",
    "video_model_draft": "FMOTION_VIDEO_MODEL_DRAFT",
    "kling_base": "FMOTION_KLING_BASE",
    "kling_model": "FMOTION_KLING_MODEL",
    "video_provider": "FMOTION_VIDEO_PROVIDER",
}


def load(workspace):
    cfg = dict(DEFAULTS)
    path = os.path.join(workspace, "config.json")
    if os.path.exists(path):
        with open(path) as f:
            cfg.update(json.load(f))
    for key, var in ENV.items():
        if os.environ.get(var):
            cfg[key] = os.environ[var]
    return cfg


def key(name):
    """API keys come only from the environment, never from files in the project."""
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"{name} is not set. Export it in your shell; fmotion never reads keys from project files.")
    return value
