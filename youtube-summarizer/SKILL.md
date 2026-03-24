---
name: youtube-summarizer
description: >
  Summarize YouTube videos by extracting and analyzing auto-generated subtitles.
  Use when the user provides a YouTube URL and asks to summarize, explain, or
  analyze a video's content. Triggers on patterns like "this video summarize",
  "summarize this YouTube", "what does this video say", or any request involving
  a youtube.com or youtu.be URL combined with summarization/analysis intent.
  Supports both Japanese and English videos.
---

# YouTube Summarizer

## Prerequisites

- `yt-dlp` must be installed (`pip install yt-dlp`)

## Workflow

### 1. Extract transcript

Run the bundled script to fetch and clean the transcript:

```bash
python scripts/fetch_transcript.py "<YOUTUBE_URL>" --lang <LANG> 2>/tmp/yt_meta.json > /tmp/yt_transcript.txt
```

- `--lang ja` (default) for Japanese videos, `--lang en` for English.
- The script auto-detects original-language captions first, then falls back.
- **stdout**: cleaned plain-text transcript.
- **stderr**: JSON metadata `{"video_id", "title", "language"}`.
- If no subtitles exist, the script exits with code 1.

### 2. Read transcript and metadata

Read `/tmp/yt_meta.json` for the title and language, then read `/tmp/yt_transcript.txt` for the full text.

### 3. Summarize

Produce a structured summary in the user's language. Use the following structure as a guide (adapt headings to fit the content):

- **Title / topic** (one line)
- **Core concept** (1-2 paragraphs explaining the main idea)
- **Key sections** (3-5 sections with subheadings, covering the major points)
- **Conclusion / takeaway**

Keep the summary concise but comprehensive. Preserve technical terms and proper nouns from the original.

### 4. Clean up

Remove temporary files after summarization:

```bash
rm -f /tmp/yt_transcript.txt /tmp/yt_meta.json
```
