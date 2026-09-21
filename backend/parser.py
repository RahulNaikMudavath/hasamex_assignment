import os
import re
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class TranscriptTurn(BaseModel):
    turn_id: int
    timestamp: str  # MM:SS
    seconds: int
    speaker: str
    is_expert: bool
    text: str

class TranscriptMetadata(BaseModel):
    id: str
    filename: str
    expert_name: str
    role: str
    market: str
    flag: str
    total_turns: int
    total_words: int
    expert_words: int
    interviewer_words: int
    duration_str: str
    duration_seconds: int

class ParsedTranscript(BaseModel):
    metadata: TranscriptMetadata
    turns: List[TranscriptTurn]
    raw_text: str

def parse_timestamp_seconds(ts: str) -> int:
    parts = ts.strip().split(':')
    if len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    elif len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    return 0

def parse_transcript_text(raw_text: str, filename: str = "transcript.txt") -> ParsedTranscript:
    lines = raw_text.strip().splitlines()
    
    expert_name = "Unknown Expert"
    role = "Specialist"
    market = "Europe"
    flag = "🌐"
    
    content_start_idx = 0
    
    # Parse header metadata
    for idx, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            continue
        
        if line_clean.lower().startswith("expert") or "dr." in line_clean.lower() or "anna" in line_clean.lower():
            # e.g. "Expert 1 – Dr. Jean Martin"
            parts = re.split(r'[–-]', line_clean, maxsplit=1)
            if len(parts) > 1:
                expert_name = parts[1].strip()
            else:
                expert_name = line_clean
        elif line_clean.lower().startswith("role:"):
            role = line_clean.split(":", 1)[1].strip()
        elif line_clean.lower().startswith("market:"):
            market = line_clean.split(":", 1)[1].strip()
            content_start_idx = idx + 1
            break
    
    if "france" in market.lower():
        flag = "🇫🇷"
    elif "germany" in market.lower():
        flag = "🇩🇪"
    elif "united kingdom" in market.lower() or "uk" in market.lower():
        flag = "🇬🇧"
        
    transcript_id = re.sub(r'[^a-zA-Z0-9_]', '_', filename.replace('.txt', '').lower())
    
    # Parse turns
    turns: List[TranscriptTurn] = []
    current_ts = "00:00"
    current_speaker = ""
    current_text_lines: List[str] = []
    turn_id = 1
    
    ts_pattern = re.compile(r'^(\d{1,2}:\d{2}(?::\d{2})?)$')
    speaker_pattern = re.compile(r'^([A-Za-z0-9\.\s]+):\s*(.*)$')
    
    def save_current_turn():
        nonlocal turn_id, current_ts, current_speaker, current_text_lines
        if current_speaker and current_text_lines:
            text = " ".join(current_text_lines).strip()
            is_expert = "interviewer" not in current_speaker.lower()
            turns.append(TranscriptTurn(
                turn_id=turn_id,
                timestamp=current_ts,
                seconds=parse_timestamp_seconds(current_ts),
                speaker=current_speaker,
                is_expert=is_expert,
                text=text
            ))
            turn_id += 1
            current_text_lines = []

    remaining_lines = lines[content_start_idx:]
    for line in remaining_lines:
        line_s = line.strip()
        if not line_s:
            continue
            
        # Check if line is a timestamp
        if ts_pattern.match(line_s):
            save_current_turn()
            current_ts = line_s
            continue
            
        # Check if line begins with Speaker:
        sm = speaker_pattern.match(line_s)
        if sm:
            save_current_turn()
            current_speaker = sm.group(1).strip()
            first_sentence = sm.group(2).strip()
            if first_sentence:
                current_text_lines.append(first_sentence)
            continue
            
        # Continuation line
        current_text_lines.append(line_s)
        
    save_current_turn()
    
    # Statistics
    total_words = 0
    expert_words = 0
    interviewer_words = 0
    max_seconds = 0
    
    for t in turns:
        words = len(t.text.split())
        total_words += words
        if t.is_expert:
            expert_words += words
        else:
            interviewer_words += words
        if t.seconds > max_seconds:
            max_seconds = t.seconds
            
    mins = max_seconds // 60
    secs = max_seconds % 60
    duration_str = f"{mins:02d}:{secs:02d}"
    
    metadata = TranscriptMetadata(
        id=transcript_id,
        filename=filename,
        expert_name=expert_name,
        role=role,
        market=market,
        flag=flag,
        total_turns=len(turns),
        total_words=total_words,
        expert_words=expert_words,
        interviewer_words=interviewer_words,
        duration_str=duration_str,
        duration_seconds=max_seconds
    )
    
    return ParsedTranscript(
        metadata=metadata,
        turns=turns,
        raw_text=raw_text
    )

def load_case_pack_transcripts(case_pack_dir: str) -> Dict[str, ParsedTranscript]:
    transcripts = {}
    files = {
        "transcript_france": "Transcript_1_France.txt",
        "transcript_germany": "Transcript_2_Germany.txt",
        "transcript_uk": "Transcript_3_UK.txt"
    }
    for key, fname in files.items():
        p = os.path.join(case_pack_dir, fname)
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                content = f.read()
            parsed = parse_transcript_text(content, filename=fname)
            transcripts[parsed.metadata.id] = parsed
    return transcripts
