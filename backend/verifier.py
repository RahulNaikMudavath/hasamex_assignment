import re
from typing import Dict, Any, Optional
from pydantic import BaseModel

class QuoteVerificationResult(BaseModel):
    quote: str
    is_verbatim: bool
    similarity_score: float
    start_char: int
    end_char: int
    matched_turn_id: Optional[int]
    matched_speaker: Optional[str]
    matched_timestamp: Optional[str]

def normalize_text(text: str) -> str:
    # Normalize whitespaces and quotes
    text = re.sub(r'[\u2018\u2019]', "'", text)
    text = re.sub(r'[\u201c\u201d]', '"', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def verify_quote_in_transcript(quote: str, raw_text: str, turns: list = None) -> QuoteVerificationResult:
    clean_quote = normalize_text(quote)
    clean_raw = normalize_text(raw_text)
    
    # 1. Exact string search
    idx = clean_raw.find(clean_quote)
    if idx != -1:
        start_char = idx
        end_char = idx + len(clean_quote)
        
        # Determine turn
        matched_turn_id = None
        matched_speaker = None
        matched_timestamp = None
        
        if turns:
            for turn in turns:
                norm_turn = normalize_text(turn.text)
                if clean_quote in norm_turn or clean_quote[:30] in norm_turn:
                    matched_turn_id = turn.turn_id
                    matched_speaker = turn.speaker
                    matched_timestamp = turn.timestamp
                    break
                    
        return QuoteVerificationResult(
            quote=quote,
            is_verbatim=True,
            similarity_score=1.0,
            start_char=start_char,
            end_char=end_char,
            matched_turn_id=matched_turn_id,
            matched_speaker=matched_speaker,
            matched_timestamp=matched_timestamp
        )
        
    # 2. Case-insensitive exact search
    lower_raw = clean_raw.lower()
    lower_quote = clean_quote.lower()
    idx = lower_raw.find(lower_quote)
    if idx != -1:
        matched_turn_id = None
        matched_speaker = None
        matched_timestamp = None
        if turns:
            for turn in turns:
                if lower_quote in normalize_text(turn.text).lower():
                    matched_turn_id = turn.turn_id
                    matched_speaker = turn.speaker
                    matched_timestamp = turn.timestamp
                    break
                    
        return QuoteVerificationResult(
            quote=quote,
            is_verbatim=True,
            similarity_score=0.98,
            start_char=idx,
            end_char=idx + len(clean_quote),
            matched_turn_id=matched_turn_id,
            matched_speaker=matched_speaker,
            matched_timestamp=matched_timestamp
        )
        
    # 3. Fuzzy partial check (word overlap)
    quote_words = set(lower_quote.split())
    best_turn = None
    best_overlap = 0.0
    
    if turns:
        for turn in turns:
            turn_words = set(normalize_text(turn.text).lower().split())
            if not quote_words:
                continue
            overlap = len(quote_words.intersection(turn_words)) / len(quote_words)
            if overlap > best_overlap:
                best_overlap = overlap
                best_turn = turn
                
    if best_overlap >= 0.8 and best_turn:
        return QuoteVerificationResult(
            quote=quote,
            is_verbatim=False,
            similarity_score=round(best_overlap, 2),
            start_char=-1,
            end_char=-1,
            matched_turn_id=best_turn.turn_id,
            matched_speaker=best_turn.speaker,
            matched_timestamp=best_turn.timestamp
        )
        
    return QuoteVerificationResult(
        quote=quote,
        is_verbatim=False,
        similarity_score=0.0,
        start_char=-1,
        end_char=-1,
        matched_turn_id=None,
        matched_speaker=None,
        matched_timestamp=None
    )
