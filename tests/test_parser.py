import os
import pytest
from backend.parser import load_case_pack_transcripts, parse_timestamp_seconds

def test_parse_timestamp_seconds():
    assert parse_timestamp_seconds("00:18") == 18
    assert parse_timestamp_seconds("01:20") == 80
    assert parse_timestamp_seconds("06:08") == 368
    assert parse_timestamp_seconds("01:05:30") == 3930

def test_load_transcripts():
    case_pack_dir = os.path.join(os.path.dirname(__file__), "..", "case_pack")
    transcripts = load_case_pack_transcripts(case_pack_dir)
    
    assert len(transcripts) == 3
    assert "transcript_1_france" in transcripts
    assert "transcript_2_germany" in transcripts
    assert "transcript_3_uk" in transcripts

    fr = transcripts["transcript_1_france"]
    assert fr.metadata.expert_name == "Dr. Jean Martin"
    assert fr.metadata.market == "France"
    assert fr.metadata.role == "Head of Urology"
    assert len(fr.turns) > 0

    de = transcripts["transcript_2_germany"]
    assert de.metadata.expert_name == "Anna Keller"
    assert de.metadata.market == "Germany"
    assert de.metadata.role == "Former Hospital Procurement Director"

    uk = transcripts["transcript_3_uk"]
    assert uk.metadata.expert_name == "Dr. Emily Carter"
    assert uk.metadata.market == "United Kingdom"
    assert uk.metadata.role == "Consultant Urologist"
