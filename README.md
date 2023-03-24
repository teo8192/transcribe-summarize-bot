# Goal

A discord bot that transcribes and summarizes discord conversations.

# Using pycord instead of discord.py

This is because it is able to record audio?

# setup

You need to create an app and a bot with discord.
Then place the key of the bot in the file `.env` (demo file below).

Then you need to configure [Azure speech-to-text](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/get-started-speech-to-text?tabs=linux%2Cterminal&pivots=programming-language-python), and add the key and region to the `.env` file.
The same with [Azure document summarization](https://learn.microsoft.com/en-us/azure/cognitive-services/language-service/summarization/quickstart?pivots=programming-language-python&tabs=document-summarization), but note that this needs the endpoint and not the region.

If you want a language that is not norwegian, change the `LANGUAGE` constant in `config.py`.
Supported languages are [the ones supported by the speech service in Azure](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/supported-languages).

`.env`:
```
DISCORD_TOKEN=<your-token-goes-here>
SPEECH_KEY=<your-key-goes-here>
SPEECH_REGION=<the-region>
TEXT_ANALYTICS_KEY=<the-second-key>
TEXT_ANALYTICS_ENDPOINT=<text-analytics-endpoint>
```

# Usage

Just run the bot, then use the commands `!start @transcription` and `!stop @transcription`.
The audio recordings are saved in the `recordings` directory.
The full transcription is sent on discord, and also saved in the recordings directory.

The summarization should also be sent on discord, when that works.

Run with `python client.py`.
