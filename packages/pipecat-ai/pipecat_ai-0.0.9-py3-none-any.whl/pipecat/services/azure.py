import aiohttp
import asyncio
import io
from openai import AsyncAzureOpenAI

from collections.abc import AsyncGenerator

from pipecat.services.ai_services import TTSService, ImageGenService
from PIL import Image

from loguru import logger

# See .env.example for Azure configuration needed
try:
    from azure.cognitiveservices.speech import (
        SpeechSynthesizer,
        SpeechConfig,
        ResultReason,
        CancellationReason,
    )
except ModuleNotFoundError as e:
    logger.error(f"Exception: {e}")
    logger.error(
        "In order to use Azure TTS, you need to `pip install pipecat-ai[azure]`. Also, set `AZURE_SPEECH_API_KEY` and `AZURE_SPEECH_REGION` environment variables.")
    raise Exception(f"Missing module: {e}")

from pipecat.services.openai_api_llm_service import BaseOpenAILLMService


class AzureTTSService(TTSService):
    def __init__(self, *, api_key, region, voice="en-US-SaraNeural"):
        super().__init__()

        self.speech_config = SpeechConfig(subscription=api_key, region=region)
        self.speech_synthesizer = SpeechSynthesizer(
            speech_config=self.speech_config, audio_config=None
        )
        self._voice = voice

    async def run_tts(self, sentence) -> AsyncGenerator[bytes, None]:
        self.logger.info("Running azure tts")
        ssml = (
            "<speak version='1.0' xml:lang='en-US' xmlns='http://www.w3.org/2001/10/synthesis' "
            "xmlns:mstts='http://www.w3.org/2001/mstts'>"
            f"<voice name='{self._voice}'>"
            "<mstts:silence type='Sentenceboundary' value='20ms' />"
            "<mstts:express-as style='lyrical' styledegree='2' role='SeniorFemale'>"
            "<prosody rate='1.05'>"
            f"{sentence}"
            "</prosody></mstts:express-as></voice></speak> ")
        result = await asyncio.to_thread(self.speech_synthesizer.speak_ssml, (ssml))
        self.logger.info("Got azure tts result")
        if result.reason == ResultReason.SynthesizingAudioCompleted:
            self.logger.info("Returning result")
            # azure always sends a 44-byte header. Strip it off.
            yield result.audio_data[44:]
        elif result.reason == ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            self.logger.info(
                "Speech synthesis canceled: {}".format(
                    cancellation_details.reason))
            if cancellation_details.reason == CancellationReason.Error:
                self.logger.info(
                    "Error details: {}".format(
                        cancellation_details.error_details))


class AzureLLMService(BaseOpenAILLMService):
    def __init__(
            self,
            *,
            api_key,
            endpoint,
            api_version="2023-12-01-preview",
            model):
        self._endpoint = endpoint
        self._api_version = api_version

        super().__init__(api_key=api_key, model=model)
        self._model: str = model

    def create_client(self, api_key=None, base_url=None):
        self._client = AsyncAzureOpenAI(
            api_key=api_key,
            azure_endpoint=self._endpoint,
            api_version=self._api_version,
        )


class AzureImageGenServiceREST(ImageGenService):

    def __init__(
        self,
        *,
        api_version="2023-06-01-preview",
        image_size: str,
        aiohttp_session: aiohttp.ClientSession,
        api_key,
        endpoint,
        model,
    ):
        super().__init__()

        self._api_key = api_key
        self._azure_endpoint = endpoint
        self._api_version = api_version
        self._model = model
        self._aiohttp_session = aiohttp_session
        self._image_size = image_size

    async def run_image_gen(self, prompt: str) -> tuple[str, bytes, tuple[int, int]]:
        url = f"{self._azure_endpoint}openai/images/generations:submit?api-version={self._api_version}"
        headers = {
            "api-key": self._api_key,
            "Content-Type": "application/json"}
        body = {
            # Enter your prompt text here
            "prompt": prompt,
            "size": self._image_size,
            "n": 1,
        }
        async with self._aiohttp_session.post(
            url, headers=headers, json=body
        ) as submission:
            # We never get past this line, because this header isn't
            # defined on a 429 response, but something is eating our
            # exceptions!
            operation_location = submission.headers["operation-location"]
            status = ""
            attempts_left = 120
            json_response = None
            while status != "succeeded":
                attempts_left -= 1
                if attempts_left == 0:
                    raise Exception("Image generation timed out")

                await asyncio.sleep(1)
                response = await self._aiohttp_session.get(
                    operation_location, headers=headers
                )
                json_response = await response.json()
                status = json_response["status"]

            image_url = (
                json_response["result"]["data"][0]["url"] if json_response else None)
            if not image_url:
                raise Exception("Image generation failed")
            # Load the image from the url
            async with self._aiohttp_session.get(image_url) as response:
                image_stream = io.BytesIO(await response.content.read())
                image = Image.open(image_stream)
                return (image_url, image.tobytes(), image.size)
