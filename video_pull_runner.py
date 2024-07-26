import traceback
from typing import Any, TypedDict, List
import logging
from datashaper import VerbCallbacks

from cache import load_cache
from rate_limiter import RateLimiter
from utils import create_hash_key
from zhipuai import ZhipuAI

log = logging.getLogger(__name__)


class VideoData(TypedDict):
    url: str
    cover_image_url: str


class VideoResult(TypedDict):
    video_task_id: str

    result: List[VideoData]
    task_status: str


class VideoPullGenerator:
    def __init__(
            self,
    ):
        pass

    async def __call__(self, inputs: dict[str, Any]) -> VideoResult:
        """Call method definition."""
        output = None
        try:
            client = ZhipuAI()  # 填写您自己的APIKey

            output = client.videos.retrieve_videos_result(
                id=inputs["video_task_id"]
            )

        except Exception as e:
            log.exception("error VideoPullGenerator")
            output = {}

        return VideoResult(
            video_task_id=inputs["video_task_id"],
            result=[VideoData(url=video.url, cover_image_url=video.cover_image_url)
                    for video in output.video_result
                    if video is not None],
            task_status=output.task_status
        )


async def run(
        video_task_id: str,
        reporter: VerbCallbacks,
) -> VideoResult | None:
    return await _run_extractor(video_task_id, reporter)


async def _run_extractor(
        video_task_id: str,
        reporter: VerbCallbacks,
) -> VideoResult | None:
    # RateLimiter
    rate_limiter = RateLimiter(rate=1, per=60)
    generator = VideoPullGenerator()

    try:
        await rate_limiter.acquire()

        cache_key = create_hash_key("VideoPullGenerator",
                                    {
                                        "video_task_id": video_task_id,
                                    })
        _cache = load_cache(root_dir="cache_data", base_dir="VideoPullGenerator")

        cached_result = await _cache.get(cache_key)

        if cached_result:
            return cached_result

        generator_output = await generator({"video_task_id": video_task_id})
        if generator_output:
            await _cache.set(
                cache_key,
                generator_output,
                {
                    "video_task_id": video_task_id,
                },
            )
        return generator_output
    except Exception as e:
        log.exception("Error processing video_task_id: %s", video_task_id)
        reporter.error("input_text Error", e, traceback.format_exc())
        return None
