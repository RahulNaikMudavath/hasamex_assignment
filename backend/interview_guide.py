from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from backend.verifier import verify_quote_in_transcript, QuoteVerificationResult

class ExpertAnswer(BaseModel):
    expert_id: str
    expert_name: str
    role: str
    market: str
    flag: str
    transcript_filename: str
    summary_answer: str
    exact_quote: str
    timestamp: str
    seconds: int
    turn_id: Optional[int] = None
    verification: Optional[QuoteVerificationResult] = None

class QuestionAnalysis(BaseModel):
    question_id: int
    question_text: str
    short_title: str
    category: str
    cross_market_takeaway: str
    answers: Dict[str, ExpertAnswer]

INTERVIEW_QUESTIONS = [
    {
        "id": 1,
        "text": "How would you describe current adoption of robotic surgery in your market?",
        "short_title": "Current Adoption",
        "category": "Market Landscape",
        "cross_market_takeaway": "Adoption is growing across all 3 markets, but remains starkly bifurcated between large academic/university centres and regional hospitals."
    },
    {
        "id": 2,
        "text": "What are the main barriers to adoption?",
        "short_title": "Barriers to Adoption",
        "category": "Adoption Hurdles",
        "cross_market_takeaway": "Capital purchase cost and economic justification dominate in France and Germany, whereas UK identifies training capacity and theatre staff readiness alongside funding."
    },
    {
        "id": 3,
        "text": "How important are hospital budgets and ROI in purchasing decisions?",
        "short_title": "Budgets & ROI Importance",
        "category": "Economics & Governance",
        "cross_market_takeaway": "Strict economic gatekeeping in Germany and France (finance/procurement veto), contrasting with a balanced clinical-economic-strategic approach in the UK NHS."
    },
    {
        "id": 4,
        "text": "How important are surgeon training and clinical outcomes?",
        "short_title": "Surgeon Training & Outcomes",
        "category": "Clinical & Operations",
        "cross_market_takeaway": "Unanimous consensus that single-surgeon adoption is an economic failure mode; hospitals require multiple trained surgeons and theatre staff to safeguard utilization."
    },
    {
        "id": 5,
        "text": "What adoption trend do you expect over the next 3–5 years?",
        "short_title": "3–5 Year Adoption Outlook",
        "category": "Market Forecast",
        "cross_market_takeaway": "Divergent forecasts: Germany projects conservative high single/low double digits, France sees 15–20% in premier centres, and UK expects accelerating growth (>15%) contingent on training."
    },
    {
        "id": 6,
        "text": "What is the typical hospital decision-making timeline for purchasing a new robotic system?",
        "short_title": "Decision-Making Timeline",
        "category": "Sales Cycle",
        "cross_market_takeaway": "Varies by healthcare governance: UK is fastest (6–9 months if funds exist), France is moderate (6–12 months), and Germany is slowest (9–18 months due to multi-department consensus)."
    }
]

RAW_EXPERT_ANSWERS = {
    1: {
        "transcript_france": {
            "summary_answer": "Adoption is steadily growing but heavily concentrated in major academic teaching hospitals and well-funded private institutions, while smaller regional facilities lag substantially behind.",
            "exact_quote": "Adoption is growing, but it is still concentrated in larger academic hospitals and private centres with stronger capital budgets. Smaller regional hospitals are much slower.",
            "timestamp": "00:18"
        },
        "transcript_germany": {
            "summary_answer": "Growth is ongoing but highly uneven across hospital tiers; large university hospitals lead adoption, whereas smaller community hospitals remain cautious and observant.",
            "exact_quote": "It is growing, but adoption is quite uneven. Large university hospitals are much more advanced, while many smaller hospitals are still waiting.",
            "timestamp": "00:16"
        },
        "transcript_uk": {
            "summary_answer": "Robotic surgery has become standard of care for select specialized procedures in large NHS trusts, though substantial regional and hospital-level access disparities remain.",
            "exact_quote": "Adoption is increasing, and in some larger NHS trusts robotic surgery is becoming standard for selected procedures. But access still varies significantly by hospital.",
            "timestamp": "00:14"
        }
    },
    2: {
        "transcript_france": {
            "summary_answer": "Capital budget approval represents the primary obstacle; clinical enthusiasm from surgical staff is insufficient without a rigorously vetted economic case presented to purchasing committees.",
            "exact_quote": "The biggest issue is still capital budget approval. Hospitals may like the technology clinically, but purchasing committees need a strong economic case before approving a system.",
            "timestamp": "01:20"
        },
        "transcript_germany": {
            "summary_answer": "High upfront capital expenditure amidst hospital margin pressure, compounded by the operational requirement to prove the system will achieve high utilization.",
            "exact_quote": "Cost is the first barrier. These are large capital purchases, and hospital finances are under pressure. The second issue is proving that the system will be used enough.",
            "timestamp": "01:10"
        },
        "transcript_uk": {
            "summary_answer": "Capital funding is significant, but training pipeline capacity is equally limiting; acquiring the system without adequate trained surgeons and theatre teams stalls adoption.",
            "exact_quote": "Funding is important, but I would say training capacity is just as important. You can buy a system, but if you cannot train enough surgeons and theatre staff, adoption stalls.",
            "timestamp": "01:05"
        }
    },
    3: {
        "transcript_france": {
            "summary_answer": "ROI is pivotal. While surgical teams evaluate clinical utility, hospital finance leaders evaluate equipment utilization, projected procedure volume, ongoing maintenance overhead, and capital payback.",
            "exact_quote": "Very important. The clinical argument may get surgeons interested, but the finance team wants to understand utilisation, procedure volume, maintenance cost and whether the system will actually pay for itself.",
            "timestamp": "02:18"
        },
        "transcript_germany": {
            "summary_answer": "Procurement conducts rigorous Total Cost of Ownership (TCO) and service contract evaluations; despite clinical merits, approval hinges directly on the strength of the economic business case.",
            "exact_quote": "We look at total cost of ownership, expected procedure volume, maintenance, service contracts and training requirements. A strong clinical case helps, but the economic case decides whether it gets approved.",
            "timestamp": "02:08"
        },
        "transcript_uk": {
            "summary_answer": "Financial ROI matters but operates alongside broader strategic criteria: patient clinical outcomes, reduced length of hospital stay, surgical recruitment/retention, and institutional reputation.",
            "exact_quote": "It matters, but the discussion is not always purely financial. Hospitals also consider patient outcomes, length of stay, surgeon recruitment and whether the technology improves their clinical position.",
            "timestamp": "02:07"
        }
    },
    4: {
        "transcript_france": {
            "summary_answer": "Multi-surgeon training is essential within year one to sustain required caseload volumes. Clinical outcomes are a prerequisite, but economics distinguish between systems with equivalent outcomes.",
            "exact_quote": "Training matters, especially in the first year. If only one surgeon can use the system, the economics become difficult. Hospitals want several surgeons trained so utilisation is high enough.",
            "timestamp": "03:10"
        },
        "transcript_germany": {
            "summary_answer": "Operationally critical. Relying on a single trained surgeon results in poor equipment utilization, which fundamentally undermines the business case and procurement justification.",
            "exact_quote": "Very important operationally. If the hospital buys a system but only one surgeon is comfortable using it, utilisation will be poor. That weakens the business case.",
            "timestamp": "03:05"
        },
        "transcript_uk": {
            "summary_answer": "Training must encompass both surgeons and multidisciplinary theatre staff; long-term program sustainability requires broad training and sufficient procedure volumes.",
            "exact_quote": "The key point is that adoption is not just about buying the machine. Hospitals need enough trained people and enough procedure volume to make the programme sustainable.",
            "timestamp": "06:04"
        }
    },
    5: {
        "transcript_france": {
            "summary_answer": "Anticipates steady, non-explosive expansion of 15% to 20% annual procedure volume growth within well-funded flagship centres, with ongoing sluggish adoption in smaller hospitals.",
            "exact_quote": "I expect adoption to continue increasing, probably steadily rather than explosively. I would expect maybe 15 to 20 percent more procedures annually in some of the stronger centres, but smaller hospitals will remain slower.",
            "timestamp": "05:07"
        },
        "transcript_germany": {
            "summary_answer": "Projects gradual, measured growth in high single digits or low double digits across the market, restrained by competing capital allocation priorities across departments.",
            "exact_quote": "I would expect continued growth, but probably closer to high single digits or low double digits in procedure volumes rather than something like 20 percent across the whole market.",
            "timestamp": "05:08"
        },
        "transcript_uk": {
            "summary_answer": "Optimistic about acceleration exceeding 15% annual procedure growth in leading areas, propelled by expanded training capacity and increasing market price competition.",
            "exact_quote": "I am quite positive. I think adoption could accelerate if training expands and systems become more cost competitive. I could see procedure growth above 15 percent annually in some areas.",
            "timestamp": "04:06"
        }
    },
    6: {
        "transcript_france": {
            "summary_answer": "A realistic timeframe is 6 to 12 months once formal evaluation begins, though decisions can stretch significantly if capital committees defer funding to the subsequent fiscal cycle.",
            "exact_quote": "Six to twelve months is realistic once the hospital becomes serious. It can be longer if the capital committee pushes the purchase into the next budget cycle.",
            "timestamp": "06:08"
        },
        "transcript_germany": {
            "summary_answer": "Typically 9 to 18 months; prolonged timeline due to the complex consensus required across procurement, clinical leadership, finance directors, and executive board members.",
            "exact_quote": "Nine to eighteen months is common. Procurement, clinical leadership, finance and management all need to align, so it can move slowly.",
            "timestamp": "06:05"
        },
        "transcript_uk": {
            "summary_answer": "Can conclude within 6 to 9 months if capital budget is already earmarked; takes substantially longer if the trust must await approval in a new NHS capital funding cycle.",
            "exact_quote": "Around six to nine months can happen if funding is already available. If the trust has to wait for a new capital cycle, it can take much longer.",
            "timestamp": "05:04"
        }
    }
}

def get_complete_interview_guide_analysis(parsed_transcripts: Dict[str, Any]) -> List[QuestionAnalysis]:
    result = []
    
    # Helper to resolve transcript from dictionary by key or country
    def resolve_transcript(key: str) -> Optional[Any]:
        if key in parsed_transcripts:
            return parsed_transcripts[key]
        for t_id, t in parsed_transcripts.items():
            if key in t_id:
                return t
            if "france" in key and ("france" in t_id or "france" in t.metadata.market.lower()):
                return t
            if "germany" in key and ("germany" in t_id or "germany" in t.metadata.market.lower()):
                return t
            if "uk" in key and ("uk" in t_id or "united kingdom" in t.metadata.market.lower()):
                return t
        return None

    for q in INTERVIEW_QUESTIONS:
        qid = q["id"]
        q_raw_answers = RAW_EXPERT_ANSWERS.get(qid, {})
        answers_dict = {}
        
        for exp_key, a_data in q_raw_answers.items():
            parsed = resolve_transcript(exp_key)
            if not parsed:
                continue
                
            raw_text = parsed.raw_text
            turns = parsed.turns
            meta = parsed.metadata
            
            # Verify quote
            verif = verify_quote_in_transcript(a_data["exact_quote"], raw_text, turns)
            
            # Parse seconds
            pts = a_data["timestamp"].split(":")
            secs = int(pts[0]) * 60 + int(pts[1])
            
            answer = ExpertAnswer(
                expert_id=meta.id,
                expert_name=meta.expert_name,
                role=meta.role,
                market=meta.market,
                flag=meta.flag,
                transcript_filename=meta.filename,
                summary_answer=a_data["summary_answer"],
                exact_quote=a_data["exact_quote"],
                timestamp=a_data["timestamp"],
                seconds=secs,
                turn_id=verif.matched_turn_id,
                verification=verif
            )
            answers_dict[meta.id] = answer
            
        result.append(QuestionAnalysis(
            question_id=qid,
            question_text=q["text"],
            short_title=q["short_title"],
            category=q["category"],
            cross_market_takeaway=q["cross_market_takeaway"],
            answers=answers_dict
        ))
        
    return result
