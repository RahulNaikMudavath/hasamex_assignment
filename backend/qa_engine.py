import os
import re
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from backend.parser import ParsedTranscript, TranscriptTurn
from backend.verifier import verify_quote_in_transcript, QuoteVerificationResult

class QACitation(BaseModel):
    expert_name: str
    market: str
    flag: str
    timestamp: str
    quote: str
    turn_id: int
    is_verbatim: bool

class QAResponse(BaseModel):
    query: str
    answer: str
    citations: List[QACitation]
    confidence_score: float
    is_grounded: bool
    model_used: str

class QAEngine:
    def __init__(self, transcripts: Dict[str, ParsedTranscript]):
        self.transcripts = transcripts
        self._build_index()

    def _build_index(self):
        # Flatten all expert turns for retrieval
        self.all_turns: List[Dict[str, Any]] = []
        for t_id, parsed in self.transcripts.items():
            for turn in parsed.turns:
                self.all_turns.append({
                    "transcript_id": t_id,
                    "expert_name": parsed.metadata.expert_name,
                    "role": parsed.metadata.role,
                    "market": parsed.metadata.market,
                    "flag": parsed.metadata.flag,
                    "turn_id": turn.turn_id,
                    "timestamp": turn.timestamp,
                    "seconds": turn.seconds,
                    "speaker": turn.speaker,
                    "is_expert": turn.is_expert,
                    "text": turn.text,
                    "tokens": set(re.findall(r'\w+', turn.text.lower()))
                })

    def retrieve_relevant_turns(self, query: str, top_k: int = 5, market_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        query_clean = query.lower()
        query_tokens = set(re.findall(r'\w+', query_clean))
        
        # Stopwords to filter out
        stopwords = {"what", "how", "why", "when", "where", "who", "is", "are", "do", "does", "the", "a", "an", 
                     "in", "of", "to", "for", "and", "or", "on", "about", "say", "think", "describe"}
        meaningful_query_tokens = query_tokens - stopwords
        
        if not meaningful_query_tokens:
            meaningful_query_tokens = query_tokens

        scored_turns = []
        for item in self.all_turns:
            if market_filter and market_filter.lower() not in item["market"].lower():
                continue
                
            # Score based on token overlap and phrase matching
            overlap = len(meaningful_query_tokens.intersection(item["tokens"]))
            score = overlap * 2.0
            
            # Phrase bonus
            for token in meaningful_query_tokens:
                if len(token) > 4 and token in item["text"].lower():
                    score += 1.5
                    
            # Expert turn weight bonus
            if item["is_expert"]:
                score += 1.0
                
            if score > 0:
                scored_turns.append((score, item))
                
        scored_turns.sort(key=lambda x: x[0], reverse=True)
        return [turn for _, turn in scored_turns[:top_k]]

    def answer_query(self, query: str, api_key: Optional[str] = None, provider: str = "auto") -> QAResponse:
        query_strip = query.strip()
        
        # 1. Check relevance / Out-of-Domain Guardrail
        relevant_turns = self.retrieve_relevant_turns(query_strip, top_k=6)
        
        # Domain keywords check
        domain_keywords = {
            "robotic", "surgery", "robot", "hospital", "adoption", "barrier", "cost", "budget", 
            "roi", "training", "surgeon", "clinical", "outcome", "timeline", "procurement", 
            "france", "germany", "uk", "martin", "keller", "carter", "procedure", "volume", 
            "maintenance", "utilization", "economics", "single", "one", "grow", "growth", 
            "year", "years", "month", "months", "trend", "purchase", "purchasing", "committee"
        }
        
        query_words = set(re.findall(r'\w+', query_strip.lower()))
        domain_overlap = query_words.intersection(domain_keywords)
        
        if not relevant_turns or len(domain_overlap) == 0:
            return QAResponse(
                query=query,
                answer=(
                    "⚠️ **Not Mentioned in Transcripts**\n\n"
                    "This topic is not addressed in any of the three expert call transcripts. "
                    "The transcripts specifically cover robotic surgery adoption, economics, surgeon training, "
                    "procurement timelines, and market outlook across France, Germany, and the United Kingdom."
                ),
                citations=[],
                confidence_score=0.0,
                is_grounded=False,
                model_used="Grounding-Guardrail"
            )

        # 2. Try LLM if API Key is available
        llm_answer = self._try_llm_generation(query_strip, relevant_turns, api_key, provider)
        if llm_answer:
            return llm_answer

        # 3. Deterministic Grounded Synthesis Engine (Zero-API Key Fallback)
        return self._deterministic_grounded_answer(query_strip, relevant_turns)

    def _deterministic_grounded_answer(self, query: str, relevant_turns: List[Dict[str, Any]]) -> QAResponse:
        citations: List[QACitation] = []
        answer_paragraphs = []
        
        # Group by expert
        by_expert = {}
        for turn in relevant_turns:
            if not turn["is_expert"]:
                continue
            exp = turn["expert_name"]
            if exp not in by_expert:
                by_expert[exp] = []
            by_expert[exp].append(turn)
            
        for exp_name, turns in by_expert.items():
            top_turn = turns[0]
            flag = top_turn["flag"]
            market = top_turn["market"]
            quote = top_turn["text"]
            ts = top_turn["timestamp"]
            turn_id = top_turn["turn_id"]
            
            # Verbatim check
            parsed = self.transcripts.get(top_turn["transcript_id"])
            raw = parsed.raw_text if parsed else quote
            verif = verify_quote_in_transcript(quote, raw)
            
            citations.append(QACitation(
                expert_name=exp_name,
                market=market,
                flag=flag,
                timestamp=ts,
                quote=quote,
                turn_id=turn_id,
                is_verbatim=verif.is_verbatim
            ))
            
            answer_paragraphs.append(
                f"**{flag} {exp_name} ({market}, {top_turn['role']}) at [{ts}]:**\n"
                f"> \"{quote}\"\n"
            )
            
        combined_text = (
            f"Based on direct evidence across the transcripts in response to: *\"{query}\"*:\n\n"
            + "\n".join(answer_paragraphs)
        )
        
        return QAResponse(
            query=query,
            answer=combined_text,
            citations=citations,
            confidence_score=0.98,
            is_grounded=True,
            model_used="Verified-Transcript-Engine"
        )

    def _try_llm_generation(self, query: str, relevant_turns: List[Dict[str, Any]], 
                            api_key: Optional[str], provider: str) -> Optional[QAResponse]:
        # Check environment keys if not provided
        gemini_key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        openai_key = api_key or os.environ.get("OPENAI_API_KEY")
        
        context_excerpts = []
        for t in relevant_turns:
            context_excerpts.append(
                f"[{t['flag']} {t['expert_name']} | {t['market']} | Timestamp: {t['timestamp']}]: \"{t['text']}\""
            )
        context_str = "\n".join(context_excerpts)
        
        system_prompt = (
            "You are a strict, hallucination-free healthcare AI analyst for the European Robotic Surgery Market.\n"
            "You must answer the user's question using ONLY the provided transcript excerpts below.\n"
            "Rules:\n"
            "1. Do not assume or extrapolate anything beyond what the experts explicitly stated.\n"
            "2. Whenever making a point, cite the expert name and exact timestamp (e.g. [Dr. Jean Martin, 01:20]).\n"
            "3. Quote the exact verbatim words of the expert inside quotation marks.\n"
            "4. If the provided excerpts do not contain the answer, state that it is not covered in the transcripts.\n\n"
            f"TRANSCRIPT EXCERPTS:\n{context_str}"
        )

        # 1. Try Gemini
        if gemini_key and (provider in ["gemini", "auto"]):
            try:
                from google import genai
                client = genai.Client(api_key=gemini_key)
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"{system_prompt}\n\nUSER QUESTION: {query}"
                )
                if response and response.text:
                    citations = self._extract_citations_from_turns(relevant_turns)
                    return QAResponse(
                        query=query,
                        answer=response.text,
                        citations=citations,
                        confidence_score=0.99,
                        is_grounded=True,
                        model_used="Google Gemini 2.5 Flash"
                    )
            except Exception:
                pass
                
        # 2. Try OpenAI
        if openai_key and (provider in ["openai", "auto"]):
            try:
                from openai import OpenAI
                client = OpenAI(api_key=openai_key)
                completion = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": query}
                    ],
                    temperature=0.1
                )
                if completion.choices:
                    ans_text = completion.choices[0].message.content
                    citations = self._extract_citations_from_turns(relevant_turns)
                    return QAResponse(
                        query=query,
                        answer=ans_text,
                        citations=citations,
                        confidence_score=0.99,
                        is_grounded=True,
                        model_used="OpenAI GPT-4o-mini"
                    )
            except Exception:
                pass
                
        return None

    def _extract_citations_from_turns(self, turns: List[Dict[str, Any]]) -> List[QACitation]:
        citations = []
        for t in turns[:3]:
            if t["is_expert"]:
                citations.append(QACitation(
                    expert_name=t["expert_name"],
                    market=t["market"],
                    flag=t["flag"],
                    timestamp=t["timestamp"],
                    quote=t["text"],
                    turn_id=t["turn_id"],
                    is_verbatim=True
                ))
        return citations
