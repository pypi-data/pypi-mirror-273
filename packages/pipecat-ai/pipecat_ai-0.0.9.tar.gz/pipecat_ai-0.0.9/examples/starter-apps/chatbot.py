import asyncio
import aiohttp
import logging
import os
from PIL import Image
from typing import AsyncGenerator

from pipecat.pipeline.aggregators import (
    LLMAssistantResponseAggregator,
    LLMUserResponseAggregator,
)
from pipecat.pipeline.frames import (
    ImageFrame,
    SpriteFrame,
    Frame,
    LLMResponseEndFrame,
    LLMMessagesFrame,
    AudioFrame,
    PipelineStartedFrame,
)
from pipecat.services.ai_services import AIService
from pipecat.pipeline.pipeline import Pipeline
from pipecat.transports.daily_transport import DailyTransport
from pipecat.services.open_ai_services import OpenAILLMService
from pipecat.services.elevenlabs_ai_services import ElevenLabsTTSService

from runner import configure

from dotenv import load_dotenv
load_dotenv(override=True)

logging.basicConfig(format=f"%(levelno)s %(asctime)s %(message)s")
logger = logging.getLogger("pipecat")
logger.setLevel(logging.DEBUG)

sprites = []

script_dir = os.path.dirname(__file__)

for i in range(1, 26):
    # Build the full path to the image file
    full_path = os.path.join(script_dir, f"assets/robot0{i}.png")
    # Get the filename without the extension to use as the dictionary key
    # Open the image and convert it to bytes
    with Image.open(full_path) as img:
        sprites.append(img.tobytes())

flipped = sprites[::-1]
sprites.extend(flipped)
# When the bot isn't talking, show a static image of the cat listening
quiet_frame = ImageFrame(sprites[0], (1024, 576))
talking_frame = SpriteFrame(images=sprites)


class TalkingAnimation(AIService):
    """
    This class starts a talking animation when it receives an first AudioFrame,
    and then returns to a "quiet" sprite when it sees a LLMResponseEndFrame.
    """

    def __init__(self):
        super().__init__()
        self._is_talking = False

    async def process_frame(self, frame: Frame) -> AsyncGenerator[Frame, None]:
        if isinstance(frame, AudioFrame):
            if not self._is_talking:
                yield talking_frame
                yield frame
                self._is_talking = True
            else:
                yield frame
        elif isinstance(frame, LLMResponseEndFrame):
            yield quiet_frame
            yield frame
            self._is_talking = False
        else:
            yield frame


class AnimationInitializer(AIService):

    async def process_frame(self, frame: Frame) -> AsyncGenerator[Frame, None]:
        if isinstance(frame, PipelineStartedFrame):
            yield quiet_frame
            yield frame
        else:
            yield frame


async def main(room_url: str, token):
    async with aiohttp.ClientSession() as session:
        transport = DailyTransport(
            room_url,
            token,
            "Chatbot",
            duration_minutes=5,
            start_transcription=True,
            mic_enabled=True,
            mic_sample_rate=16000,
            camera_enabled=True,
            camera_width=1024,
            camera_height=576,
            vad_enabled=True,
        )

        tts = ElevenLabsTTSService(
            aiohttp_session=session,
            api_key=os.getenv("ELEVENLABS_API_KEY"),
            voice_id="pNInz6obpgDQGcFmaJgB",
        )

        llm = OpenAILLMService(
            api_key=os.getenv("OPENAI_API_KEY"),
            model="gpt-4-turbo-preview")

        ta = TalkingAnimation()
        ai = AnimationInitializer()
        pipeline = Pipeline([ai, llm, tts, ta])
        messages = [
            {
                "role": "system",
                "content": "You are Chatbot, a friendly, helpful robot. Your goal is to demonstrate your capabilities in a succinct way. Your output will be converted to audio. Respond to what the user said in a creative and helpful way, but keep your responses brief. Start by introducing yourself.",
            },
        ]

        @transport.event_handler("on_first_other_participant_joined")
        async def on_first_other_participant_joined(transport, participant):
            print(f"!!! in here, pipeline.source is {pipeline.source}")
            await pipeline.queue_frames([LLMMessagesFrame(messages)])

        async def run_conversation():

            await transport.run_interruptible_pipeline(
                pipeline,
                post_processor=LLMAssistantResponseAggregator(messages),
                pre_processor=LLMUserResponseAggregator(messages),
            )

        await asyncio.gather(transport.run(), run_conversation())


if __name__ == "__main__":
    (url, token) = configure()
    asyncio.run(main(url, token))
