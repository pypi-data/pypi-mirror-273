import copy
import aiohttp
import asyncio
import json
import logging
import os
import re
import wave
from typing import AsyncGenerator, List
from pipecat.pipeline.opeanai_llm_aggregator import (
    OpenAIAssistantContextAggregator,
    OpenAIUserContextAggregator,
)

from pipecat.pipeline.pipeline import Pipeline
from pipecat.transports.daily_transport import DailyTransport
from pipecat.services.openai_llm_context import OpenAILLMContext
from pipecat.services.open_ai_services import OpenAILLMService
# from pipecat.services.deepgram_ai_services import DeepgramTTSService
from pipecat.services.elevenlabs_ai_services import ElevenLabsTTSService
from pipecat.services.fireworks_ai_services import FireworksLLMService
from pipecat.pipeline.frames import (
    Frame,
    LLMFunctionCallFrame,
    LLMFunctionStartFrame,
    AudioFrame,
)
from pipecat.pipeline.openai_frames import OpenAILLMContextFrame
from pipecat.services.ai_services import FrameLogger, AIService
from openai._types import NotGiven, NOT_GIVEN

from openai.types.chat import (
    ChatCompletionToolParam,
)

from runner import configure

from dotenv import load_dotenv
load_dotenv(override=True)

logging.basicConfig(format="%(levelno)s %(asctime)s %(message)s")
logger = logging.getLogger("pipecat")
logger.setLevel(logging.DEBUG)

sounds = {}
sound_files = [
    "clack-short.wav",
    "clack.wav",
    "clack-short-quiet.wav",
    "ding.wav",
    "ding2.wav",
]

script_dir = os.path.dirname(__file__)

for file in sound_files:
    # Build the full path to the sound file
    full_path = os.path.join(script_dir, "assets", file)
    # Get the filename without the extension to use as the dictionary key
    filename = os.path.splitext(os.path.basename(full_path))[0]
    # Open the sound and convert it to bytes
    with wave.open(full_path) as audio_file:
        sounds[file] = audio_file.readframes(-1)


steps = [{"prompt": "Start by introducing yourself. Then, ask the user to confirm their identity by telling you their birthday, including the year. When they answer with their birthday, call the verify_birthday function.",
          "run_async": False,
          "failed": "The user provided an incorrect birthday. Ask them for their birthday again. When they answer, call the verify_birthday function.",
          "tools": [{"type": "function",
                     "function": {"name": "verify_birthday",
                                  "description": "Use this function to verify the user has provided their correct birthday.",
                                  "parameters": {"type": "object",
                                                 "properties": {"birthday": {"type": "string",
                                                                             "description": "The user's birthdate, including the year. The user can provide it in any format, but convert it to YYYY-MM-DD format to call this function.",
                                                                             }},
                                                 },
                                  },
                     }],
          },
         {"prompt": "Next, thank the user for confirming their identity, then ask the user to list their current prescriptions. Each prescription needs to have a medication name and a dosage. Do not call the list_prescriptions function with any unknown dosages.",
          "run_async": True,
          "tools": [{"type": "function",
                     "function": {"name": "list_prescriptions",
                                  "description": "Once the user has provided a list of their prescription medications, call this function.",
                                  "parameters": {"type": "object",
                                                 "properties": {"prescriptions": {"type": "array",
                                                                                  "items": {"type": "object",
                                                                                            "properties": {"medication": {"type": "string",
                                                                                                                          "description": "The medication's name",
                                                                                                                          },
                                                                                                           "dosage": {"type": "string",
                                                                                                                      "description": "The prescription's dosage",
                                                                                                                      },
                                                                                                           },
                                                                                            },
                                                                                  }},
                                                 },
                                  },
                     }],
          },
         {"prompt": "Next, ask the user if they have any allergies. Once they have listed their allergies or confirmed they don't have any, call the list_allergies function.",
          "run_async": True,
          "tools": [{"type": "function",
                     "function": {"name": "list_allergies",
                                  "description": "Once the user has provided a list of their allergies, call this function.",
                                  "parameters": {"type": "object",
                                                 "properties": {"allergies": {"type": "array",
                                                                              "items": {"type": "object",
                                                                                        "properties": {"name": {"type": "string",
                                                                                                                "description": "What the user is allergic to",
                                                                                                                }},
                                                                                        },
                                                                              }},
                                                 },
                                  },
                     }],
          },
         {"prompt": "Now ask the user if they have any medical conditions the doctor should know about. Once they've answered the question, call the list_conditions function.",
          "run_async": True,
          "tools": [{"type": "function",
                     "function": {"name": "list_conditions",
                                  "description": "Once the user has provided a list of their medical conditions, call this function.",
                                  "parameters": {"type": "object",
                                                 "properties": {"conditions": {"type": "array",
                                                                               "items": {"type": "object",
                                                                                         "properties": {"name": {"type": "string",
                                                                                                                 "description": "The user's medical condition",
                                                                                                                 }},
                                                                                         },
                                                                               }},
                                                 },
                                  },
                     },
                    ],
          },
         {"prompt": "Finally, ask the user the reason for their doctor visit today. Once they answer, call the list_visit_reasons function.",
          "run_async": True,
          "tools": [{"type": "function",
                     "function": {"name": "list_visit_reasons",
                                  "description": "Once the user has provided a list of the reasons they are visiting a doctor today, call this function.",
                                  "parameters": {"type": "object",
                                                 "properties": {"visit_reasons": {"type": "array",
                                                                                  "items": {"type": "object",
                                                                                            "properties": {"name": {"type": "string",
                                                                                                                    "description": "The user's reason for visiting the doctor",
                                                                                                                    }},
                                                                                            },
                                                                                  }},
                                                 },
                                  },
                     }],
          },
         {"prompt": "Now, thank the user and end the conversation.",
          "run_async": True,
          "tools": [],
          },
         {"prompt": "",
          "run_async": True,
          "tools": []},
         ]
current_step = 0


class ChecklistProcessor(AIService):

    def __init__(
        self,
        context: OpenAILLMContext,
        llm: AIService,
        tools: List[ChatCompletionToolParam] | NotGiven = NOT_GIVEN,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._context: OpenAILLMContext = context
        self._llm = llm
        self._id = "You are Jessica, an agent for a company called Tri-County Health Services. Your job is to collect important information from the user before their doctor visit. You're talking to Chad Bailey. You should address the user by their first name and be polite and professional. You're not a medical professional, so you shouldn't provide any advice. Keep your responses short. Your job is to collect information to give to a doctor. Don't make assumptions about what values to plug into functions. Ask for clarification if a user response is ambiguous."
        self._acks = ["One sec.", "Let me confirm that.", "Thanks.", "OK."]

        # Create an allowlist of functions that the LLM can call
        self._functions = [
            "verify_birthday",
            "list_prescriptions",
            "list_allergies",
            "list_conditions",
            "list_visit_reasons",
        ]

        self._context.add_message(
            {"role": "system", "content": f"{self._id} {steps[0]['prompt']}"}
        )

        if tools:
            self._context.set_tools(tools)

    def verify_birthday(self, args):
        return args["birthday"] == "1983-01-01"

    def list_prescriptions(self, args):
        # print(f"--- Prescriptions: {args['prescriptions']}\n")
        pass

    def list_allergies(self, args):
        # print(f"--- Allergies: {args['allergies']}\n")
        pass

    def list_conditions(self, args):
        # print(f"--- Medical Conditions: {args['conditions']}")
        pass

    def list_visit_reasons(self, args):
        # print(f"Visit Reasons: {args['visit_reasons']}")
        pass

    async def process_frame(self, frame: Frame) -> AsyncGenerator[Frame, None]:
        global current_step
        this_step = steps[current_step]
        self._context.set_tools(this_step["tools"])
        if isinstance(frame, LLMFunctionStartFrame):
            print(f"... Preparing function call: {frame.function_name}")
            self._function_name = frame.function_name
            if this_step["run_async"]:
                # Get the LLM talking about the next step before getting the rest
                # of the function call completion
                current_step += 1
                self._context.add_message(
                    {"role": "system", "content": steps[current_step]["prompt"]}
                )
                yield OpenAILLMContextFrame(self._context)

                local_context = copy.deepcopy(self._context)
                local_context.set_tool_choice("none")
                async for frame in llm.process_frame(
                    OpenAILLMContextFrame(local_context)
                ):
                    yield frame
            else:
                # Insert a quick response while we run the function
                yield AudioFrame(sounds["ding2.wav"])
                pass
        elif isinstance(frame, LLMFunctionCallFrame):

            if frame.function_name and frame.arguments:
                print(
                    f"--> Calling function: {frame.function_name} with arguments:")
                pretty_json = re.sub(
                    "\n", "\n    ", json.dumps(
                        json.loads(
                            frame.arguments), indent=2))
                print(f"--> {pretty_json}\n")
                if frame.function_name not in self._functions:
                    raise Exception(
                        f"Unknown function.")
                fn = getattr(self, frame.function_name)
                result = fn(json.loads(frame.arguments))

                if not this_step["run_async"]:
                    if result:
                        current_step += 1
                        self._context.add_message(
                            {"role": "system", "content": steps[current_step]["prompt"]}
                        )
                        yield OpenAILLMContextFrame(self._context)

                        local_context = copy.deepcopy(self._context)
                        local_context.set_tool_choice("none")
                        async for frame in llm.process_frame(
                            OpenAILLMContextFrame(local_context)
                        ):
                            yield frame
                    else:
                        self._context.add_message(
                            {"role": "system", "content": this_step["failed"]}
                        )
                        yield OpenAILLMContextFrame(self._context)

                        local_context = copy.deepcopy(self._context)
                        local_context.set_tool_choice("none")
                        async for frame in llm.process_frame(
                            OpenAILLMContextFrame(local_context)
                        ):
                            yield frame
                    print(f"<-- Verify result: {result}\n")

        else:
            yield frame


async def main(room_url: str, token):
    async with aiohttp.ClientSession() as session:
        global transport
        global llm
        global tts

        transport = DailyTransport(
            room_url,
            token,
            "Intake Bot",
            5,
            mic_enabled=True,
            mic_sample_rate=16000,
            camera_enabled=False,
            start_transcription=True,
            vad_enabled=True,
        )

        messages = []

        llm = FireworksLLMService(
            api_key=os.getenv("FIREWORKS_API_KEY"),
            model="accounts/fireworks/models/firefunction-v1"
        )
        # tts = DeepgramTTSService(
        #     aiohttp_session=session,
        #     api_key=os.getenv("DEEPGRAM_API_KEY"),
        #     voice="aura-asteria-en",
        # )
        tts = ElevenLabsTTSService(
            aiohttp_session=session,
            api_key=os.getenv("ELEVENLABS_API_KEY"),
            voice_id="XrExE9yKIg1WjnnlVkGX",
        )
        context = OpenAILLMContext(
            messages=messages,
        )

        checklist = ChecklistProcessor(context, llm)
        fl = FrameLogger("FRAME LOGGER 1:")
        fl2 = FrameLogger("FRAME LOGGER 2:")
        pipeline = Pipeline(processors=[fl, llm, fl2, checklist, tts])

        @transport.event_handler("on_first_other_participant_joined")
        async def on_first_other_participant_joined(transport, participant):
            await pipeline.queue_frames([OpenAILLMContextFrame(context)])

        async def handle_intake():
            await transport.run_interruptible_pipeline(
                pipeline,
                post_processor=OpenAIAssistantContextAggregator(context),
                pre_processor=OpenAIUserContextAggregator(context),
            )

        try:
            await asyncio.gather(transport.run(), handle_intake())
        except (asyncio.CancelledError, KeyboardInterrupt):
            print("whoops")
            transport.stop()


if __name__ == "__main__":
    (url, token) = configure()
    asyncio.run(main(url, token))
