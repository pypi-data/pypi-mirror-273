import aiohttp
import asyncio
import os
import wave

from pipecat.transports.daily_transport import DailyTransport
from pipecat.services.azure_ai_services import AzureLLMService, AzureTTSService
from pipecat.pipeline.aggregators import LLMContextAggregator
from pipecat.services.ai_services import AIService, FrameLogger
from pipecat.pipeline.frames import Frame, AudioFrame, LLMResponseEndFrame, LLMMessagesFrame
from typing import AsyncGenerator

from runner import configure

from dotenv import load_dotenv
load_dotenv(override=True)

sounds = {}
sound_files = [
    'ding1.wav',
    'ding2.wav'
]

script_dir = os.path.dirname(__file__)

for file in sound_files:
    # Build the full path to the image file
    full_path = os.path.join(script_dir, "assets", file)
    # Get the filename without the extension to use as the dictionary key
    filename = os.path.splitext(os.path.basename(full_path))[0]
    # Open the image and convert it to bytes
    with wave.open(full_path) as audio_file:
        sounds[file] = audio_file.readframes(-1)


class OutboundSoundEffectWrapper(AIService):
    def __init__(self):
        pass

    async def process_frame(self, frame: Frame) -> AsyncGenerator[Frame, None]:
        if isinstance(frame, LLMResponseEndFrame):
            yield AudioFrame(sounds["ding1.wav"])
            # In case anything else up the stack needs it
            yield frame
        else:
            yield frame


class InboundSoundEffectWrapper(AIService):
    def __init__(self):
        pass

    async def process_frame(self, frame: Frame) -> AsyncGenerator[Frame, None]:
        if isinstance(frame, LLMMessagesFrame):
            yield AudioFrame(sounds["ding2.wav"])
            # In case anything else up the stack needs it
            yield frame
        else:
            yield frame


async def main(room_url: str, token, phone):
    async with aiohttp.ClientSession() as session:

        global transport
        global llm
        global tts

        transport = DailyTransport(
            room_url,
            token,
            "Respond bot",
            300,
        )
        transport._mic_enabled = True
        transport._mic_sample_rate = 16000
        transport._camera_enabled = False

        llm = AzureLLMService()
        tts = AzureTTSService()

        @transport.event_handler("on_first_other_participant_joined")
        async def on_first_other_participant_joined(transport, participant):
            await tts.say("Hi, I'm listening!", transport.send_queue)
            await transport.send_queue.put(AudioFrame(sounds["ding1.wav"]))

        async def handle_transcriptions():
            messages = [
                {"role": "system", "content": "You are a helpful LLM in a WebRTC call. Your goal is to demonstrate your capabilities in a succinct way. Your output will be converted to audio. Respond to what the user said in a creative and helpful way."},
            ]

            tma_in = LLMContextAggregator(
                messages, "user", transport._my_participant_id
            )
            tma_out = LLMContextAggregator(
                messages, "assistant", transport._my_participant_id
            )
            out_sound = OutboundSoundEffectWrapper()
            in_sound = InboundSoundEffectWrapper()
            fl = FrameLogger("LLM Out")
            fl2 = FrameLogger("Transcription In")
            await out_sound.run_to_queue(
                transport.send_queue,
                tts.run(
                    tma_out.run(
                        llm.run(
                            fl2.run(
                                in_sound.run(
                                    tma_in.run(
                                        transport.get_receive_frames()
                                    )
                                )
                            )
                        )
                    )
                )
            )

        @transport.event_handler("on_participant_joined")
        async def pax_joined(transport, pax):
            print(f"PARTICIPANT JOINED: {pax}")

        @transport.event_handler("on_call_state_updated")
        async def on_call_state_updated(transport, state):
            if (state == "joined"):
                if (phone):
                    transport.start_recording()
                    transport.dialout(phone)

        await asyncio.gather(transport.run(), handle_transcriptions())


if __name__ == "__main__":
    (url, token) = configure()
    asyncio.run(main(url, token))
