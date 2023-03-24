# Goal

A discord bot that transcribes and summarizes discord conversations.

# Using pycord instead of discord.py

This is because it is able to record audio?

# setup

You need to create an app and a bot with discord.
Then place the key of the bot in the file `.env` (demo file below).

Then you need to configure [Azure speech-to-text](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/get-started-speech-to-text?tabs=linux%2Cterminal&pivots=programming-language-python), and add the key and region to the `.env` file.
The same with [Azure document summarization](https://learn.microsoft.com/en-us/azure/cognitive-services/language-service/summarization/quickstart?pivots=programming-language-python&tabs=document-summarization).

`.env`:
```
DISCORD_TOKEN=<your-token-goes-here>
SPEECH_KEY=<your-key-goes-here>
SPEECH_REGION=<the-region>
TEXT_ANALYTICS_KEY=<the-second-key>
TEXT_ANALYTICS_REGION=<the-second-region>
```

# Usage

Just run the bot, then use the commands `!start @transcription` and `!stop @transcription`.
The audio recordings are saved in the `recordings` folder, and also sent on discord.
The full transcription is also sent on discord (should maybe save this to a file as well?).

The summarization should also be sent on discord, when that works.
