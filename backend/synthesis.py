from typing import List, Dict, Any
from pydantic import BaseModel

class SupportingEvidence(BaseModel):
    expert_name: str
    market: str
    flag: str
    quote: str
    timestamp: str

class CommonTheme(BaseModel):
    id: str
    title: str
    category: str
    consensus_level: str  # e.g., "100% Unanimous", "Strong Agreement"
    synthesis: str
    strategic_implication: str
    evidence: List[SupportingEvidence]

class Disagreement(BaseModel):
    id: str
    topic: str
    category: str
    description: str
    expert_stances: Dict[str, Dict[str, Any]]
    analysis: str

class MarketComparisonRow(BaseModel):
    market: str
    flag: str
    expert: str
    role: str
    primary_decision_gate: str
    adoption_growth_forecast: str
    purchasing_timeline: str
    top_barrier: str
    view_on_roi: str

class CrossCallSynthesis(BaseModel):
    executive_summary: str
    market_comparison: List[MarketComparisonRow]
    common_themes: List[CommonTheme]
    disagreements: List[Disagreement]

def generate_cross_call_synthesis() -> CrossCallSynthesis:
    executive_summary = (
        "Across France, Germany, and the UK, the European robotic surgery market is transitioning from early surgical "
        "enthusiasm to stringent institutional accountability. While clinical efficacy is universally recognized, "
        "purchasing authority has shifted toward hospital finance and procurement committees that mandate robust utilization, "
        "predictable Total Cost of Ownership (TCO), and institutional training pipelines. Growth is anticipated across all "
        "geographies, but pace and purchasing velocities diverge sharply based on national healthcare funding models."
    )

    market_comparison = [
        MarketComparisonRow(
            market="France",
            flag="🇫🇷",
            expert="Dr. Jean Martin",
            role="Head of Urology",
            primary_decision_gate="Hospital Finance & Purchasing Committee",
            adoption_growth_forecast="15%–20% annual procedure increase in leading centres",
            purchasing_timeline="6 to 12 months (budget cycle dependent)",
            top_barrier="Capital budget approval & economic justification",
            view_on_roi="Critical: Must prove utilization, procedure volumes & payback"
        ),
        MarketComparisonRow(
            market="Germany",
            flag="🇩🇪",
            expert="Anna Keller",
            role="Former Hospital Procurement Director",
            primary_decision_gate="Procurement, Clinical Leadership & Executive Board",
            adoption_growth_forecast="High single digits to low double digits market-wide",
            purchasing_timeline="9 to 18 months (consensus-driven)",
            top_barrier="High upfront capital cost & proving adequate utilization",
            view_on_roi="Decisive: TCO, service contracts, and procedure volume dictate approval"
        ),
        MarketComparisonRow(
            market="United Kingdom",
            flag="🇬🇧",
            expert="Dr. Emily Carter",
            role="Consultant Urologist",
            primary_decision_gate="NHS Trust Capital Committee & Clinical Leadership",
            adoption_growth_forecast=">15% annual acceleration if training expands",
            purchasing_timeline="6 to 9 months (fast if funded; delayed if pending cycle)",
            top_barrier="Training pipeline capacity for surgeons & theatre teams",
            view_on_roi="Balanced: Evaluated alongside length of stay, recruitment & clinical strategy"
        )
    ]

    common_themes = [
        CommonTheme(
            id="theme_bifurcation",
            title="Severe Tier-1 Concentration vs Regional Hospital Lag",
            category="Market Landscape",
            consensus_level="Unanimous Across All 3 Calls",
            synthesis=(
                "All three experts emphatically report that robotic surgical adoption remains disproportionately clustered "
                "in large university medical centres, academic teaching trusts, and premier private clinics. Smaller regional and "
                "community hospitals face prohibitive capital thresholds and lower procedural volume, creating a widening technology gap."
            ),
            strategic_implication=(
                "Robotic device manufacturers must develop tiered pricing, shared-service models, or flexible procedure-based leasing "
                "to penetrate the underserved mid-market hospital segment."
            ),
            evidence=[
                SupportingEvidence(
                    expert_name="Dr. Jean Martin",
                    market="France",
                    flag="🇫🇷",
                    quote="Adoption is growing, but it is still concentrated in larger academic hospitals and private centres with stronger capital budgets. Smaller regional hospitals are much slower.",
                    timestamp="00:18"
                ),
                SupportingEvidence(
                    expert_name="Anna Keller",
                    market="Germany",
                    flag="🇩🇪",
                    quote="It is growing, but adoption is quite uneven. Large university hospitals are much more advanced, while many smaller hospitals are still waiting.",
                    timestamp="00:16"
                ),
                SupportingEvidence(
                    expert_name="Dr. Emily Carter",
                    market="United Kingdom",
                    flag="🇬🇧",
                    quote="Adoption is increasing, and in some larger NHS trusts robotic surgery is becoming standard for selected procedures. But access still varies significantly by hospital.",
                    timestamp="00:14"
                )
            ]
        ),
        CommonTheme(
            id="theme_training_bottleneck",
            title="Single-Surgeon Dependence is an Economic Failure Mode",
            category="Operational Economics",
            consensus_level="Unanimous Across All 3 Calls",
            synthesis=(
                "Every expert identified surgeon and theatre staff training as an indispensable economic prerequisite rather than merely "
                "an educational milestone. When a hospital acquires a multimillion-euro robotic system with only one certified operator, "
                "system utilization remains below breakeven thresholds, crippling the investment business case."
            ),
            strategic_implication=(
                "Vendors that bundle accelerated, multi-surgeon certification programs and whole-team theatre training packages "
                "will enjoy shorter sales cycles and reduced post-sale churn."
            ),
            evidence=[
                SupportingEvidence(
                    expert_name="Dr. Jean Martin",
                    market="France",
                    flag="🇫🇷",
                    quote="Training matters, especially in the first year. If only one surgeon can use the system, the economics become difficult. Hospitals want several surgeons trained so utilisation is high enough.",
                    timestamp="03:10"
                ),
                SupportingEvidence(
                    expert_name="Anna Keller",
                    market="Germany",
                    flag="🇩🇪",
                    quote="Very important operationally. If the hospital buys a system but only one surgeon is comfortable using it, utilisation will be poor. That weakens the business case.",
                    timestamp="03:05"
                ),
                SupportingEvidence(
                    expert_name="Dr. Emily Carter",
                    market="United Kingdom",
                    flag="🇬🇧",
                    quote="The key point is that adoption is not just about buying the machine. Hospitals need enough trained people and enough procedure volume to make the programme sustainable.",
                    timestamp="06:04"
                )
            ]
        ),
        CommonTheme(
            id="theme_economic_veto",
            title="Clinical Outcomes Are Table Stakes; Economic Justification Decides Purchases",
            category="Purchasing Governance",
            consensus_level="Strong Consensus",
            synthesis=(
                "Superior or non-inferior clinical outcomes are considered a mandatory prerequisite to enter purchasing discussions, "
                "but clinical enthusiasm alone never secures a contract. Purchasing committees, CFOs, and procurement directors "
                "evaluate the decision strictly as a capital asset balancing procedure volume, maintenance overhead, and payback."
            ),
            strategic_implication=(
                "Sales teams cannot rely solely on key opinion leader (KOL) surgical champions; they must equip clinical advocates "
                "with turn-key departmental ROI models and Total Cost of Ownership calculators."
            ),
            evidence=[
                SupportingEvidence(
                    expert_name="Dr. Jean Martin",
                    market="France",
                    flag="🇫🇷",
                    quote="Clinical outcomes are necessary, but they are not enough on their own. If two systems offer similar outcomes, the hospital will look hard at economics and utilisation.",
                    timestamp="04:08"
                ),
                SupportingEvidence(
                    expert_name="Anna Keller",
                    market="Germany",
                    flag="🇩🇪",
                    quote="A strong clinical case helps, but the economic case decides whether it gets approved.",
                    timestamp="02:08"
                ),
                SupportingEvidence(
                    expert_name="Dr. Jean Martin",
                    market="France",
                    flag="🇫🇷",
                    quote="The biggest issue is still capital budget approval. Hospitals may like the technology clinically, but purchasing committees need a strong economic case before approving a system.",
                    timestamp="01:20"
                )
            ]
        )
    ]

    disagreements = [
        Disagreement(
            id="disagree_decision_criteria",
            topic="Purchasing Philosophy: Strict Economic Gatekeeping vs Balanced Strategic Value",
            category="Governance & Evaluation",
            description="Clear philosophical divergence in how hospital leadership evaluates the investment decision.",
            expert_stances={
                "France (Dr. Martin)": {
                    "stance": "Strict Economic Veto",
                    "quote": "The clinical argument may get surgeons interested, but the finance team wants to understand utilisation, procedure volume, maintenance cost and whether the system will actually pay for itself.",
                    "timestamp": "02:18",
                    "summary": "Hospital finance teams exercise direct veto power over surgeon enthusiasm, requiring quantitative proof that the capital asset pays for itself."
                },
                "Germany (Anna Keller)": {
                    "stance": "Formal Procurement & TCO Rigor",
                    "quote": "We look at total cost of ownership, expected procedure volume, maintenance, service contracts and training requirements. A strong clinical case helps, but the economic case decides whether it gets approved.",
                    "timestamp": "02:08",
                    "summary": "Procurement evaluates comprehensive multi-year operational risk; the economic case overrides clinical preference."
                },
                "UK (Dr. Carter)": {
                    "stance": "Balanced Clinical-Operational Strategy",
                    "quote": "It matters, but the discussion is not always purely financial. Hospitals also consider patient outcomes, length of stay, surgeon recruitment and whether the technology improves their clinical position.",
                    "timestamp": "02:07",
                    "summary": "NHS trusts balance financial ROI with non-financial strategic dividends, notably surgeon recruitment, bed turnaround (length of stay), and institutional competitiveness."
                }
            },
            analysis=(
                "While French and German hospitals treat the purchase primarily as a capital expenditure requiring hard commercial payback, "
                "the UK NHS framework evaluates holistic systemic value: shortening patient recovery to free acute bed capacity and attracting "
                "top surgical talent in a competitive staffing market."
            )
        ),
        Disagreement(
            id="disagree_growth_outlook",
            topic="3–5 Year Market Volume Expansion Expectations",
            category="Market Forecast",
            description="Substantial variance in forecasted procedure growth rates and market acceleration.",
            expert_stances={
                "France (Dr. Martin)": {
                    "stance": "Moderate Flagship Expansion (15%–20%)",
                    "quote": "I would expect maybe 15 to 20 percent more procedures annually in some of the stronger centres, but smaller hospitals will remain slower.",
                    "timestamp": "05:07",
                    "summary": "Healthy 15–20% annual procedure growth in top tier centres, while secondary hospitals continue to stagnate."
                },
                "Germany (Anna Keller)": {
                    "stance": "Conservative Market-Wide Growth (High Single / Low Double Digits)",
                    "quote": "I would expect continued growth, but probably closer to high single digits or low double digits in procedure volumes rather than something like 20 percent across the whole market.",
                    "timestamp": "05:08",
                    "summary": "Tempered expectations citing intense competition for capital across other clinical and diagnostic departments."
                },
                "UK (Dr. Carter)": {
                    "stance": "Accelerated Uptake (>15% Annually)",
                    "quote": "I think adoption could accelerate if training expands and systems become more cost competitive. I could see procedure growth above 15 percent annually in some areas.",
                    "timestamp": "04:06",
                    "summary": "High optimism that expanding training capacity and lower-cost competitive robotic platforms will trigger rapid volume acceleration."
                }
            },
            analysis=(
                "German procurement reflects structural capital constraints and competing hospital modernization budgets, keeping projections conservative. "
                "Conversely, UK and French clinicians anticipate robust double-digit volume expansion as training bottlenecks ease and competitive vendor options emerge."
            )
        ),
        Disagreement(
            id="disagree_timelines",
            topic="Sales & Decision-Making Velocity Across Geographies",
            category="Procurement Timeline",
            description="Wide divergence in typical procurement duration, driven by institutional governance complexity.",
            expert_stances={
                "UK (Dr. Carter)": {
                    "stance": "6 to 9 Months (Fastest)",
                    "quote": "Around six to nine months can happen if funding is already available. If the trust has to wait for a new capital cycle, it can take much longer.",
                    "timestamp": "05:04",
                    "summary": "Relatively swift execution (6–9 months) if capital allocations are already approved in trust budgets."
                },
                "France (Dr. Martin)": {
                    "stance": "6 to 12 Months (Moderate)",
                    "quote": "Six to twelve months is realistic once the hospital becomes serious. It can be longer if the capital committee pushes the purchase into the next budget cycle.",
                    "timestamp": "06:08",
                    "summary": "Moderate duration, tightly bound to annual budget allocation cycles and committee agendas."
                },
                "Germany (Anna Keller)": {
                    "stance": "9 to 18 Months (Slowest)",
                    "quote": "Nine to eighteen months is common. Procurement, clinical leadership, finance and management all need to align, so it can move slowly.",
                    "timestamp": "06:05",
                    "summary": "Protracted cycle due to consensus governance requiring multi-tier sign-off from clinical heads, procurement, CFO, and hospital board."
                }
            },
            analysis=(
                "Sales pipelines must be calibrated to country-specific administrative velocities: German deals require nearly twice the lead time of UK deals "
                "due to consensus governance, requiring phased milestone tracking."
            )
        )
    ]

    return CrossCallSynthesis(
        executive_summary=executive_summary,
        market_comparison=market_comparison,
        common_themes=common_themes,
        disagreements=disagreements
    )
