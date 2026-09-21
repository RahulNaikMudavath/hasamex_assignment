import os
import pytest
from backend.parser import load_case_pack_transcripts
from backend.interview_guide import RAW_EXPERT_ANSWERS, get_complete_interview_guide_analysis
from backend.verifier import verify_quote_in_transcript

def test_all_interview_guide_quotes_are_verbatim():
    case_pack_dir = os.path.join(os.path.dirname(__file__), "..", "case_pack")
    transcripts = load_case_pack_transcripts(case_pack_dir)
    
    # Map keys
    t_map = {
        "transcript_france": transcripts["transcript_1_france"],
        "transcript_germany": transcripts["transcript_2_germany"],
        "transcript_uk": transcripts["transcript_3_uk"]
    }

    for qid, exp_dict in RAW_EXPERT_ANSWERS.items():
        for exp_key, data in exp_dict.items():
            t = t_map[exp_key]
            quote = data["exact_quote"]
            ts = data["timestamp"]
            
            res = verify_quote_in_transcript(quote, t.raw_text, t.turns)
            assert res.is_verbatim is True, f"Quote for Q{qid} {exp_key} was not found verbatim: '{quote}'"
            assert res.matched_timestamp == ts, f"Timestamp mismatch for Q{qid} {exp_key}: expected {ts}, got {res.matched_timestamp}"
            assert res.similarity_score >= 0.98

def test_full_analysis_structure():
    case_pack_dir = os.path.join(os.path.dirname(__file__), "..", "case_pack")
    transcripts = load_case_pack_transcripts(case_pack_dir)
    analysis = get_complete_interview_guide_analysis(transcripts)
    
    assert len(analysis) == 6
    for q in analysis:
        assert len(q.answers) == 3
        for exp_id, ans in q.answers.items():
            assert ans.verification.is_verbatim is True
            assert ans.timestamp != ""
            assert ans.exact_quote != ""
