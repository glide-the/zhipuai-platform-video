import traceback
from typing import Any, TypedDict
import logging
from datashaper import VerbCallbacks

from cache import load_cache
from rate_limiter import RateLimiter
from utils import create_hash_key
from zhipuai import ZhipuAI

log = logging.getLogger(__name__)


class VideoReport(TypedDict):
    video_prompt: str
    image_path: str
    video_task_id: str


# Function to encode the image
def encode_image(image_path):
    import base64
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


class VideoStrategyGenerator:
    def __init__(
            self,
    ):
        pass

    async def __call__(self, inputs: dict[str, Any]) -> str:
        """Call method definition."""
        output = None
        try:
            client = ZhipuAI()  # 填写您自己的APIKey
            if inputs.get("request_img", True):

                base64_image = encode_image(inputs["image_path"])
                output = client.videos.generations(
                    model="cogvideo",
                    image_url=base64_image,
                    prompt=inputs["video_prompt"]
                )
            else:
                output = client.videos.generations(
                    model="cogvideo",
                    prompt=inputs["video_prompt"]
                )
        except Exception as e:
            log.exception("error VideoStrategyGenerator")
            output = {}

        return output.id


async def run(
        video_prompt: str,
        image_path: str,
        reporter: VerbCallbacks,
        strategy_config: dict[str, Any],
) -> VideoReport | None:
    return await _run_extractor(video_prompt, image_path, reporter, strategy_config)


async def _run_extractor(
        video_prompt: str,
        image_path: str,
        reporter: VerbCallbacks,
        strategy_config: dict[str, Any],
) -> VideoReport | None:
    # RateLimiter
    rate_limiter = RateLimiter(rate=1, per=60)
    generator = VideoStrategyGenerator()

    try:
        await rate_limiter.acquire()

        cache_key = create_hash_key("VideoStrategyGenerator",
                                    {
                                        "video_prompt": video_prompt,
                                        "image_path": image_path
                                    })
        _cache = load_cache(root_dir="cache_data", base_dir="VideoStrategyGenerator")

        cached_result = await _cache.get(cache_key)

        if cached_result:
            return VideoReport(video_prompt=video_prompt,
                               image_path=image_path,
                               video_task_id=cached_result
                               )

        reporter.log(f"Running VideoStrategyGenerator:{cache_key}")
        generator_output = await generator({"image_path": image_path,
                                            "video_prompt": video_prompt,
                                            "request_img": strategy_config.get("request_img", True)
        })
        if generator_output:
            await _cache.set(
                cache_key,
                generator_output,
                {
                    "video_prompt": video_prompt,
                    "image_path": image_path
                },
            )
        return VideoReport(video_prompt=video_prompt,
                           image_path=image_path,
                           video_task_id=generator_output
                           )
    except Exception as e:
        log.exception("Error processing video_prompt: %s", video_prompt)
        reporter.error("input_text Error", e, traceback.format_exc())
        return None
