import os

from prompt_runner import PromptReport
from video_runner import VideoReport
from zhipuai import ZhipuAI
from datashaper import (
    AsyncType,
    NoopVerbCallbacks,
    TableContainer,
    VerbCallbacks,
    VerbInput,
    derive_from_rows,
    progress_ticker,
    verb,
)

import pandas as pd


async def _generate_video(
        runner,
        strategy: dict,
        video_prompt: str,
        image_path: str,
) -> VideoReport | None:
    """Generate a video for a single strategy."""
    return await runner(
        video_prompt, image_path, strategy
    )


async def convert_image_to_video(level_contexts: pd.DataFrame, strategy: dict) -> pd.DataFrame:
    from video_runner import run as runner
    reports: list[VideoReport | None] = []

    async def run_generate(record):
        video_prompt_key = strategy['video_prompt_key']
        image_path_key = strategy['image_path_key']
        result = await _generate_video(
            runner,
            video_prompt=record[video_prompt_key],
            image_path=record[image_path_key],
            strategy=strategy,
        )
        return result

    local_reports = await derive_from_rows(
        level_contexts,
        run_generate,
        callbacks=NoopVerbCallbacks(),
        num_threads=1,
        scheduling_type=AsyncType.AsyncIO,
    )
    reports.extend([lr for lr in local_reports if lr is not None])
    return pd.DataFrame(reports)


async def _generate_prompt(
        runner,
        strategy: dict,
        input_text: str,
) -> PromptReport | None:
    """Generate a video for a single strategy."""
    return await runner(
        input_text, strategy
    )


async def convert_text_generator(level_contexts: pd.DataFrame, strategy: dict) -> pd.DataFrame:
    from prompt_runner import run as runner
    reports: list[PromptReport | None] = []

    async def run_generate(record):
        input_text_key = strategy['input_text_key']
        result = await _generate_prompt(
            runner,
            input_text=record[input_text_key],
            strategy=strategy,
        )
        return result

    local_reports = await derive_from_rows(
        level_contexts,
        run_generate,
        callbacks=NoopVerbCallbacks(),
        num_threads=strategy.get("num_threads", 1),
        scheduling_type=AsyncType.AsyncIO,
    )
    reports.extend([lr for lr in local_reports if lr is not None])
    return pd.DataFrame(reports)
