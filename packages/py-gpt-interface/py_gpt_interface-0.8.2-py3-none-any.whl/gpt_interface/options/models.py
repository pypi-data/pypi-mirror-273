from dataclasses import dataclass


@dataclass
class Model:
    name: str
    max_tokens: int
    description: str
    deprecated: bool
    legacy_chat_api: bool
    vision_enabled: bool = False


# from https://platform.openai.com/docs/models
# TODO: notify when trying to use deprecated model
# TODO: do something with model description
known_models = [
    Model(
        name="gpt-4o",
        description="GPT-4o: Our most advanced, multimodal flagship model that’s cheaper and faster than GPT-4 Turbo. Currently points to gpt-4o-2024-05-13.",
        max_tokens=128_000,
        deprecated=False,
        legacy_chat_api=False,
    ),
    Model(
        name="gpt-4o-2024-05-13",
        description="gpt-4o currently points to this version.",
        max_tokens=128_000,
        deprecated=False,
        legacy_chat_api=False,
    ),
    Model(
        name="gpt-4-turbo",
        description="GPT-4 Turbo with Vision: The latest GPT-4 Turbo model with vision capabilities. Vision requests can now use JSON mode and function calling. Currently points to gpt-4-turbo-2024-04-09.",
        max_tokens=128_000,
        deprecated=False,
        legacy_chat_api=False,
    ),
    Model(
        name="gpt-4-turbo-2024-04-09",
        description="GPT-4 Turbo with Vision model. Vision requests can now use JSON mode and function calling. gpt-4-turbo currently points to this version.",
        max_tokens=128_000,
        deprecated=False,
        legacy_chat_api=False,
    ),
    Model(
        name="gpt-4-0125-preview",
        description="GPT-4 Turbo: The latest GPT-4 model intended to reduce cases of “laziness” where the model doesn’t complete a task. Returns a maximum of 4,096 output tokens.",
        max_tokens=128_000,
        deprecated=False,
        legacy_chat_api=False,
    ),
    Model(
        name="gpt-4-turbo-preview",
        description="Currently points to gpt-4-0125-preview.",
        max_tokens=128_000,
        deprecated=False,
        legacy_chat_api=False,
    ),
    Model(
        name="gpt-4-1106-preview",
        description="The latest GPT-4 model with improved instruction following, JSON mode, reproducible outputs, parallel function calling, and more. Returns a maximum of 4,096 output tokens. This preview model is not yet suited for production traffic. Learn more.",
        max_tokens=128_000,
        deprecated=False,
        legacy_chat_api=False,
    ),
    Model(
        name="gpt-4-vision-preview",
        description="Ability to understand images, in addition to all other GPT-4 Turbo capabilties. Returns a maximum of 4,096 output tokens. This is a preview model version and not suited yet for production traffic. Learn more.",
        max_tokens=128_000,
        deprecated=False,
        legacy_chat_api=False,
        vision_enabled=True,
    ),
    Model(
        name="gpt-4",
        description="Currently points to gpt-4-0613. See continuous model upgrades.",
        max_tokens=8_192,
        deprecated=False,
        legacy_chat_api=False,
    ),
    Model(
        name="gpt-4-32k",
        description="Currently points to gpt-4-32k-0613. See continuous model upgrades.",
        max_tokens=32_768,
        deprecated=False,
        legacy_chat_api=False,
    ),
    Model(
        name="gpt-4-0613",
        description="Snapshot of gpt-4 from June 13th 2023 with improved function calling support.",
        max_tokens=8_192,
        deprecated=False,
        legacy_chat_api=False,
    ),
    Model(
        name="gpt-4-32k-0613",
        description="Snapshot of gpt-4-32k from June 13th 2023 with improved function calling support.",
        max_tokens=32_768,
        deprecated=False,
        legacy_chat_api=False,
    ),
    Model(
        name="gpt-4-0314",
        description="Snapshot of gpt-4 from March 14th 2023 with function calling support. This model version will be deprecated on June 13th 2024.",
        max_tokens=8_192,
        deprecated=False,
        legacy_chat_api=False,
    ),
    Model(
        name="gpt-4-32k-0314",
        description="Snapshot of gpt-4-32k from March 14th 2023 with function calling support. This model version will be deprecated on June 13th 2024.",
        max_tokens=32_768,
        deprecated=False,
        legacy_chat_api=False,
    ),
    Model(
        name="gpt-3.5-turbo-1106",
        description="The latest GPT-3.5 Turbo model with improved instruction following, JSON mode, reproducible outputs, parallel function calling, and more. Returns a maximum of 4,096 output tokens. Learn more.",
        max_tokens=16_385,
        deprecated=False,
        legacy_chat_api=False,
    ),
    Model(
        name="gpt-3.5-turbo",
        description="Currently points to gpt-3.5-turbo-0613. Will point to gpt-3.5-turbo-1106 starting Dec 11, 2023. See continuous model upgrades.",
        max_tokens=4_096,
        deprecated=False,
        legacy_chat_api=False,
    ),
    Model(
        name="gpt-3.5-turbo-16k",
        description="Currently points to gpt-3.5-turbo-0613. Will point to gpt-3.5-turbo-1106 starting Dec 11, 2023. See continuous model upgrades.",
        max_tokens=16_385,
        deprecated=False,
        legacy_chat_api=False,
    ),
    Model(
        name="gpt-3.5-turbo-instruct",
        description="Similar capabilities as text-davinci-003 but compatible with legacy Completions endpoint and not Chat Completions.",
        max_tokens=4_096,
        deprecated=False,
        legacy_chat_api=True,
    ),
    Model(
        name="gpt-3.5-turbo-0613",
        description="Snapshot of gpt-3.5-turbo from June 13th 2023. Will be deprecated on June 13, 2024.",
        max_tokens=4_096,
        deprecated=False,
        legacy_chat_api=True,
    ),
    Model(
        name="gpt-3.5-turbo-16k-0613",
        description="Snapshot of gpt-3.5-16k-turbo from June 13th 2023. Will be deprecated on June 13, 2024.",
        max_tokens=16_385,
        deprecated=False,
        legacy_chat_api=True,
    ),
    Model(
        name="gpt-3.5-turbo-0301",
        description="Snapshot of gpt-3.5-turbo from March 1st 2023. Will be deprecated on June 13th 2024.",
        max_tokens=4_096,
        deprecated=False,
        legacy_chat_api=True,
    ),
    Model(
        name="text-davinci-003",
        description="Can do language tasks with better quality and consistency than the curie, babbage, or ada models. Will be deprecated on Jan 4th 2024.",
        max_tokens=4_096,
        deprecated=True,
        legacy_chat_api=True,
    ),
    Model(
        name="text-davinci-002",
        description="Similar capabilities to text-davinci-003 but trained with supervised fine-tuning instead of reinforcement learning. Will be deprecated on Jan 4th 2024.",
        max_tokens=4_096,
        deprecated=True,
        legacy_chat_api=True,
    ),
    Model(
        name="code-davinci-002",
        description="Optimized for code-completion tasks. Will be deprecated on Jan 4th 2024.",
        max_tokens=8_001,
        deprecated=True,
        legacy_chat_api=True,
    ),
    Model(
        name="babbage-002",
        description="Replacement for the GPT-3 ada and babbage base models.",
        max_tokens=16_384,
        deprecated=True,
        legacy_chat_api=True,
    ),
    Model(
        name="davinci-002",
        description="Replacement for the GPT-3 curie and davinci base models.",
        max_tokens=16_384,
        deprecated=True,
        legacy_chat_api=True,
    ),
    Model(
        name="text-curie-001",
        description="Very capable, faster and lower cost than Davinci.",
        max_tokens=2_049,
        deprecated=True,
        legacy_chat_api=True,
    ),
    Model(
        name="text-babbage-001",
        description="Capable of straightforward tasks, very fast, and lower cost.",
        max_tokens=2_049,
        deprecated=True,
        legacy_chat_api=True,
    ),
    Model(
        name="text-ada-001",
        description="Capable of very simple tasks, usually the fastest model in the GPT-3 series, and lowest cost.",
        max_tokens=2_049,
        deprecated=True,
        legacy_chat_api=True,
    ),
    Model(
        name="davinci",
        description="Most capable GPT-3 model. Can do any task the other models can do, often with higher quality.",
        max_tokens=2_049,
        deprecated=True,
        legacy_chat_api=True,
    ),
    Model(
        name="curie",
        description="Very capable, but faster and lower cost than Davinci.",
        max_tokens=2_049,
        deprecated=True,
        legacy_chat_api=True,
    ),
    Model(
        name="babbage",
        description="Capable of straightforward tasks, very fast, and lower cost.",
        max_tokens=2_049,
        deprecated=True,
        legacy_chat_api=True,
    ),
    Model(
        name="ada",
        description="Capable of very simple tasks, usually the fastest model in the GPT-3 series, and lowest cost.",
        max_tokens=2_049,
        deprecated=True,
        legacy_chat_api=True,
    ),
]
