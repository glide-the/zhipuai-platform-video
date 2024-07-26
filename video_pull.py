import argparse
import asyncio

import pandas as pd
import os
import sys
import logging
import logging.config

from datashaper import NoopVerbCallbacks, derive_from_rows, AsyncType

from video_pull_runner import VideoResult

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])


async def _video_pull(
        runner,
        strategy: dict,
        video_task_id: str,
) -> VideoResult | None:
    return await runner(
        video_task_id, strategy
    )


async def video_pull_task(level_contexts: pd.DataFrame, strategy: dict) -> pd.DataFrame:
    from video_pull_runner import run as runner
    reports: list[VideoResult | None] = []

    async def run_generate(record):
        video_task_id_key = strategy['video_task_id_key']
        result = await _video_pull(
            runner,
            video_task_id=record[video_task_id_key],
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert the image to video')
    parser.add_argument('--task_video_csv', type=str, help='The input excel file')
    parser.add_argument('--output_path', type=str, help='The output path')
    parser.add_argument('--num_threads', type=int, default=2, help='The number of threads ')
    args = parser.parse_args()
    # Load the data
    level_contexts = pd.read_csv(args.task_video_csv)

    video_strategy = {
        "video_task_id_key": "video_task_id",
        "num_threads": 10
    }

    video_pull_report: pd.DataFrame = asyncio.run(video_pull_task(level_contexts, video_strategy))

    # Save the video report
    video_pull_report_path = os.path.join(args.output_path, "video_pull_report.csv")
    video_pull_report.to_csv(video_pull_report_path, index=False)