import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(40, 805, "CallSynth AI – Hasamex Technical Demo Presentation Script")
            self.drawRightString(555, 805, "Candidate: Rahul Naik Mudavath")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.5)
            self.line(40, 798, 555, 798)
            
        # Footer
        text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(555, 30, text)
        self.drawString(40, 30, "CONFIDENTIAL – Hasamex AI Engineer Technical Evaluation (Round 2)")
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(40, 40, 555, 40)
        
        self.restoreState()

def build_pdf():
    pdf_path = os.path.join(os.path.dirname(__file__), "Hasamex_Demo_Presentation_Guide.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=50,
        bottomMargin=50
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=4
    )
    
    sub_title_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#2563eb'),
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=10,
        spaceAfter=6
    )

    badge_style = ParagraphStyle(
        'BadgeText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#1e40af'),
        alignment=1
    )

    meta_label_style = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#64748b')
    )

    meta_val_style = ParagraphStyle(
        'MetaVal',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=colors.HexColor('#0f172a')
    )

    th_style = ParagraphStyle(
        'THStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.white
    )

    td_style = ParagraphStyle(
        'TDStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#1e293b')
    )

    td_bold_style = ParagraphStyle(
        'TDBoldStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#1e293b')
    )

    cue_style = ParagraphStyle(
        'CueStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#1e40af')
    )

    script_style = ParagraphStyle(
        'ScriptStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor('#334155')
    )

    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#334155'),
        leftIndent=12,
        spaceAfter=3
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph("CallSynth AI – Demo Video Presentation Guide", title_style))
    story.append(Paragraph("Hasamex AI Engineer Technical Case Study • Round 2 Submission Walkthrough", sub_title_style))
    
    # Meta Grid Table
    meta_data = [
        [
            Paragraph("CANDIDATE", meta_label_style),
            Paragraph("MARKET CONTEXT", meta_label_style),
            Paragraph("DURATION / FORMAT", meta_label_style),
            Paragraph("TEST COVERAGE", meta_label_style)
        ],
        [
            Paragraph("Rahul Naik Mudavath", meta_val_style),
            Paragraph("European Robotic Surgery", meta_val_style),
            Paragraph("6–8 Mins (Picture-in-Picture)", meta_val_style),
            Paragraph("10/10 Passed (pytest)", meta_val_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[120, 140, 140, 115])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Timing Table
    story.append(Paragraph("PRESENTATION TIMING & ON-SCREEN ACTION MATRIX", h1_style))
    timing_data = [
        [
            Paragraph("Timestamp", th_style),
            Paragraph("Section", th_style),
            Paragraph("On-Screen Action", th_style),
            Paragraph("Core Objective / Takeaway", th_style)
        ],
        [
            Paragraph("0:00 – 1:00", td_bold_style),
            Paragraph("1. Problem & Context", td_style),
            Paragraph("Homepage hero + 3 expert cards", td_style),
            Paragraph("Solves manual extraction, loss of quotes, and cross-market blindness", td_style)
        ],
        [
            Paragraph("1:00 – 2:15", td_bold_style),
            Paragraph("2. Architecture & Design", td_style),
            Paragraph("Architecture tab (Sections 1 & 2)", td_style),
            Paragraph("4 decoupled layers: Parser, Verifier, Synthesis, and Q&A Engine", td_style)
        ],
        [
            Paragraph("2:15 – 3:30", td_bold_style),
            Paragraph("3. Tech Stack & Models", td_style),
            Paragraph("Architecture tab (Tech stack cards)", td_style),
            Paragraph("FastAPI, Python 3.14, Gemini 2.5 Flash / GPT-4o-mini, offline engine", td_style)
        ],
        [
            Paragraph("3:30 – 4:45", td_bold_style),
            Paragraph("4. Hallucination Guardrails", td_style),
            Paragraph("Section 4 (Reduction Strategy)", td_style),
            Paragraph("Closed-domain prompts, out-of-domain refusal, verbatim match", td_style)
        ],
        [
            Paragraph("4:45 – 5:45", td_bold_style),
            Paragraph("5. Engineering Challenges", td_style),
            Paragraph("Transcripts Explorer (Turns & Search)", td_style),
            Paragraph("Regex parsing, bidirectional DOM deep-linking, zero-install setup", td_style)
        ],
        [
            Paragraph("5:45 – 7:15", td_bold_style),
            Paragraph("6. Live Application Demo", td_style),
            Paragraph("Click 01:20 badge, Cross-Call, Ask AI", td_style),
            Paragraph("Live deep-link jump, consensus & divergences, query refusal test", td_style)
        ],
        [
            Paragraph("7:15 – 8:00", td_bold_style),
            Paragraph("7. Scaling (3 to 30+ Calls)", td_style),
            Paragraph("Section 5 (Enterprise Roadmap)", td_style),
            Paragraph("pgvector hybrid search, Map-Reduce clustering, Whisper diarization", td_style)
        ],
        [
            Paragraph("8:00 – 8:30", td_bold_style),
            Paragraph("8. AI Disclosure & Wrap-up", td_style),
            Paragraph("GitHub Repo / Terminal", td_style),
            Paragraph("Transparent AI tooling disclosure; 11 feature commits on GitHub", td_style)
        ],
    ]
    t_table = Table(timing_data, colWidths=[65, 110, 150, 190])
    t_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_table)
    story.append(Spacer(1, 10))

    def make_section_card(title, time_str, screen_cue, script_text, bullet_points=None):
        card_elements = []
        
        # Header table
        hdr_table = Table([
            [Paragraph(f"<b>{title}</b>", ParagraphStyle('HdrTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#0f172a'))),
             Paragraph(f"<b>{time_str}</b>", ParagraphStyle('HdrTime', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, textColor=colors.white, alignment=2))]
        ], colWidths=[430, 85])
        hdr_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
            ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#2563eb')),
            ('TOPPADDING', (0, 0), (-1, 0), 4),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
            ('LEFTPADDING', (0, 0), (-1, 0), 6),
            ('RIGHTPADDING', (0, 0), (-1, 0), 6),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1'))
        ]))
        card_elements.append(hdr_table)
        
        # Body elements
        body_data = []
        body_data.append([Paragraph(f"<b>Visual Cue:</b> {screen_cue}", cue_style)])
        body_data.append([Paragraph(f'"{script_text}"', script_style)])
        
        if bullet_points:
            b_text = ""
            for bp in bullet_points:
                b_text += f"• <b>{bp[0]}:</b> {bp[1]}<br/>"
            body_data.append([Paragraph(b_text, bullet_style)])
            
        b_table = Table(body_data, colWidths=[515])
        b_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#ffffff')),
            ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#eff6ff')),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        card_elements.append(b_table)
        card_elements.append(Spacer(1, 9))
        return KeepTogether(card_elements)

    # Section 1
    story.append(make_section_card(
        "1. Problem Understanding & Operational Bottlenecks",
        "0:00 – 1:00",
        "Show application homepage on http://localhost:8000 with the 3 expert country cards visible.",
        "Hi everyone, thank you for reviewing my technical case study submission for the AI Engineer role at Hasamex.<br/><br/>In private equity due diligence and strategic consulting, expert calls are the primary source of qualitative truth. However, synthesizing qualitative calls suffers from three major bottlenecks: 1) Time-consuming manual extraction across interview guides; 2) Loss of traceability, where summaries lack verbatim quotes and timestamps; and 3) Thematic blindness, where spotting international market divergences is difficult when calls are read in isolation.<br/><br/>To solve this, I built CallSynth AI—an intelligence engine that ingests the 3 expert calls, auto-answers the 6-question guide with exact quotes and timestamps, synthesizes common themes and disagreements, and enables hallucination-proof cross-transcript Q&A."
    ))

    # Section 2
    story.append(make_section_card(
        "2. Architecture & Traceability Design",
        "1:00 – 2:15",
        "Click the Architecture & Scale tab in the top navigation bar; scroll to Section 1 & 2.",
        "When planning this application, my primary guiding principle was strict traceability and zero hallucination. The case brief explicitly stated: 'Do not invent information. Every important answer should be traceable to the transcript.' To enforce this, I engineered a 4-tier decoupled pipeline:",
        [
            ("Turn Segmentation Engine (backend/parser.py)", "Segments transcripts into conversational turns with exact MM:SS timestamps, speaker tags, and talk-time ratios."),
            ("Verbatim Verification Layer (backend/verifier.py)", "Character-level substring matching ensures 100% verbatim accuracy against raw transcript text."),
            ("Dual-Engine Q&A Pipeline (backend/qa_engine.py)", "Hybrid system supporting cloud LLMs (Gemini / GPT-4o-mini) and an offline deterministic engine requiring zero API keys."),
            ("Deep-Linked Single-Page Interface (static/)", "Every citation and timestamp is a clickable trigger that auto-navigates and highlights source turns in the transcript explorer.")
        ]
    ))

    story.append(PageBreak())

    # Section 3
    story.append(make_section_card(
        "3. Technology Stack & Model Decisions",
        "2:15 – 3:30",
        "Remain on Architecture tab, highlighting the Tech Stack and Model Choice cards.",
        "For our technology stack, I prioritized high performance, auditability, and zero setup friction:",
        [
            ("Backend Architecture", "Built on FastAPI, Python 3.14, and Pydantic V2 for sub-10ms response times and strict schema contracts."),
            ("Zero-Dependency Frontend", "Vanilla JavaScript & CSS SPA served directly via FastAPI. No node_modules or build scripts required—runs with 'python main.py'."),
            ("Test Coverage", "A comprehensive pytest suite with 10 unit and integration tests covering parser accuracy, quote verification, and API endpoints."),
            ("Generative Models", "Gemini 2.5 Flash and GPT-4o-mini for sub-350ms TTFT and large context windows, paired with an offline verified fallback.")
        ]
    ))

    # Section 4
    story.append(make_section_card(
        "4. Hallucination Mitigation & Guardrails",
        "3:30 – 4:45",
        "Scroll down to Section 4 (Hallucination Reduction Strategy) on the Architecture tab.",
        "In healthcare research and strategic investments, hallucinations are fatal. CallSynth implements three defense layers:",
        [
            ("Closed-Domain Constrained Prompting", "The LLM operates under a closed-world system prompt: strictly forbidden from extrapolating external facts, with mandatory citations."),
            ("Semantic Domain Guardrails", "Pre-screens queries for relevance. Out-of-scope topics (e.g. 'Da Vinci pricing in Japan') are caught and refused rather than hallucinated."),
            ("Mathematical Substring Matching", "Quotes are validated programmatically at runtime, ensuring a 100% verbatim rate in our automated tests.")
        ]
    ))

    # Section 5
    story.append(make_section_card(
        "5. Key Engineering Challenges & Solutions",
        "4:45 – 5:45",
        "Click to Transcripts Explorer tab, showcasing speaker badges, search filtering, and clean turn divisions.",
        "The primary technical hurdles solved during development were: 1) Non-standard Transcript Formats: Handled irregular timestamps and multi-line utterances using a custom regex segmentation engine that also computes speaker talk ratios; 2) Bidirectional Deep-Linking: Synchronized cross-tab navigation and DOM scrolling with pulsing CSS keyframe animations upon citation click; 3) Zero-Friction Portability: Engineered the application without external database dependencies so any reviewer can clone and run it in 30 seconds."
    ))

    # Section 6
    story.append(make_section_card(
        "6. Live Application Walkthrough (The Demonstration)",
        "5:45 – 7:15",
        "Follow this exact sequence of clicks on screen to demonstrate system capabilities:",
        [
            ("Step 1 – Interview Guide", "Show all 6 questions mapped across France, Germany, and UK with summaries, quotes, and timestamps."),
            ("Step 2 – Deep-Link Jump", "Click '01:20' under Dr. Jean Martin. Watch app jump to France transcript and pulse the exact turn in gold."),
            ("Step 3 – Cross-Call Synthesis", "Show executive matrix, 3 unanimous consensus themes (single-surgeon failure), and strategic divergences (procurement speed)."),
            ("Step 4 – Interactive Q&A", "Click quick chip: 'What do experts say about training only one surgeon?' Show multi-call citations and 98% grounding score."),
            ("Step 5 – Hallucination Guardrail", "Type: 'What is the price of Da Vinci in Japan?' Show explicit refusal message preventing hallucination."),
            ("Step 6 – Export Dossier", "Click 'Export Dossier' to instantly generate and download a clean Markdown report.")
        ]
    ))

    story.append(PageBreak())

    # Section 7
    story.append(make_section_card(
        "7. Scaling from 3 to 30+ Transcripts (Enterprise Roadmap)",
        "7:15 – 8:00",
        "Return to Architecture tab, Section 5: 'Enterprise Scaling Roadmap (3 to 30+ Calls)'.",
        "To scale CallSynth from 3 transcripts to 30+ or 300+ in production:",
        [
            ("Vector Database & Hybrid Search", "Migrate to pgvector or Qdrant, chunking calls by turn and indexing with hybrid dense (text-embedding-3-small) + sparse (BM25) search."),
            ("Hierarchical Map-Reduce Clustering", "Execute parallel 'Map' extractions per interview question, followed by 'Reduce' HDBSCAN clustering to discover emergent themes and statistical outliers."),
            ("Automated Diarization Pipeline", "Ingest raw MP3/WAV audio via Whisper or Google Speech-to-Text with automated speaker diarization."),
            ("Continuous Observability (RAGAS)", "Monitor hallucination rates, context recall, and faithfulness across continuous integration pipelines.")
        ]
    ))

    # Section 8
    story.append(make_section_card(
        "8. AI Transparency Disclosure & Submission Wrap-Up",
        "8:00 – 8:30",
        "Show terminal with 10 passed tests, git log with 11 commits, or the GitHub repository page.",
        "In compliance with Hasamex's submission instructions, I would like to disclose that AI coding tools were utilized to accelerate boilerplate generation, UI styling, and test scaffolding. All architectural decisions, verification mechanics, schema definitions, and analytical synthesis reflect my own engineering logic.<br/><br/>The complete codebase is committed feature-by-feature across 11 clean commits on GitHub, and passes all 10 automated unit tests. Thank you for your time and consideration!"
    ))

    # Checklist Card
    check_elements = []
    ch_header = Table([[Paragraph("<b>RECORDING CHECKLIST & EXECUTIVE PRO-TIPS</b>", ParagraphStyle('ChHdr', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor('#166534')))]], colWidths=[515])
    ch_header.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#dcfce7')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#86efac'))
    ]))
    check_elements.append(ch_header)
    
    ch_body = Table([[
        Paragraph(
            "• <b>Picture-in-Picture Format:</b> Keep webcam visible in the corner using Loom, OBS, or Zoom cloud recording.<br/>"
            "• <b>Full 1080p Resolution:</b> Keep browser maximized so the 3-column interview guide matrix fits side-by-side without horizontal scrolling.<br/>"
            "• <b>Highlight Pause:</b> When clicking '01:20', pause for 2 seconds to let the golden pulse animation be clearly appreciated.<br/>"
            "• <b>Audio Quality:</b> Use a headset or dedicated mic for crisp audio as requested in the submission criteria.<br/>"
            "• <b>Repository Link:</b> https://github.com/RahulNaikMudavath/hasamex_assignment.git",
            ParagraphStyle('ChBody', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=11.5, textColor=colors.HexColor('#14532d'))
        )
    ]], colWidths=[515])
    ch_body.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0fdf4')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#86efac')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    check_elements.append(ch_body)
    story.append(KeepTogether(check_elements))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF built successfully: {pdf_path}")

if __name__ == "__main__":
    build_pdf()
