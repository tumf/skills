# youtube-summarizer

Summarize YouTube videos by extracting and analyzing auto-generated subtitles.

Use when the user provides a YouTube URL and asks to summarize, explain, or analyze a video's content. Supports both Japanese and English videos.

## Install

```bash
npx skills add tumf/skills --skill youtube-summarizer
```

## Prerequisites

- `yt-dlp` must be installed (`pip install yt-dlp`)

## Usage

Provide a YouTube URL and ask for a summary:

```
Summarize this video: https://www.youtube.com/watch?v=EXAMPLE
```

The skill extracts auto-generated subtitles via `yt-dlp`, cleans the transcript, and produces a structured summary.

See [SKILL.md](./SKILL.md) for the full workflow documentation.
