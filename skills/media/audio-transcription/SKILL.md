---
name: audio-transcription
description: "Use when transcribing audio. Use the requested model safely."
---

# Audio transcription

Use this skill whenever the user sends an audio/video attachment and expects its spoken content to be read, summarized, acted on, or recorded.

## Workflow

1. Identify the local attachment path supplied by the platform. Do not ask the user to resend or describe an accessible file.
2. Use the explicitly requested provider/model. For Dr. Vinícius, the default is OpenAI `gpt-4o-transcribe`, with language `pt` / pt-BR when the speech is Portuguese.
3. Keep credentials out of terminal output and chat. Read them only from the approved environment configuration.
4. Resolve the OpenAI key from the profile config, and treat the two configured names as candidates: the voice-scoped `VOICE_TOOLS_OPENAI_KEY` and the general `OPENAI_API_KEY`. If one returns `401`, try the other before reporting a credential problem — only report `válida` / `ausente` / the HTTP status, never the value. Do not silently substitute a different provider or model.
5. Return the transcription verbatim enough to retain meaning, correcting only obvious punctuation/capitalization. If the user asks for a summary, provide it after the transcript—not instead of it.
6. If the provider returns an authorization/permission failure, state the concrete status succinctly. Ask authorization before changing the requested transcription method.

## OpenAI transcription request

Submit a multipart request to `POST https://api.openai.com/v1/audio/transcriptions` with:

- `file`: the original attachment
- `model`: `gpt-4o-transcribe`
- `language`: `pt` for Portuguese audio
- `response_format`: `json`

Keep the response body out of logs if it could contain sensitive material. Confirm that the returned JSON contains transcription text before delivering it.

## Pitfalls

- **“Could not be transcribed automatically” is not a dead end.** The attachment arrives with a usable local path; the automatic step failing says nothing about the file. Run the request yourself end to end and only report the concrete stage and status if it still fails. Asking the user to describe or resend an accessible file wastes the turn.
- **Check the audio actually matches the expected piece before acting on it.** `ffprobe` the duration and format first: a duration that does not fit the piece (a few seconds where tens were expected, or a length that matches a different script) means the wrong asset was sent. Report the mismatch and ask which piece to prepare instead of cutting or stretching audio to fit.
- **Never infer a voice clone from a supplied recording.** A transcription request tells you the words, not that the speaker authorized reuse — and in a lip-sync pipeline the recording is the literal speech, not a reusable voice sample.
- **Do not inline multi-line Python into `python3 -c` from a shell string.** Escaped newlines in the `-c` payload produce `SyntaxError: unexpected character after line continuation character`. Write a small script file or use a heredoc when the snippet needs loops or a dict comprehension.

## Output format

For a direct transcription request, reply with just:

**Transcrição**

<texto>

For failure, name the stage and HTTP status, without exposing secrets or inventing a transcript.
