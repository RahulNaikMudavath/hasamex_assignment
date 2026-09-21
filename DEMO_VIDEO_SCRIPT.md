# Hasamex Technical Demo Video – Complete Presentation Script
### Application: CallSynth AI (Expert Call Intelligence Engine)
**Recommended Video Duration:** 6 – 8 Minutes  
**Video Format:** Picture-in-Picture (PiP) with your face camera visible in the corner alongside your shared screen showing the application.

---

## ⏱️ Video Structure & Timing Breakdown

| Timestamp | Section | Key Topic & On-Screen Action |
| :--- | :--- | :--- |
| **0:00 – 1:00** | 1. Problem Understanding | Case study context, European robotic surgery market, qualitative research bottlenecks |
| **1:00 – 2:15** | 2. Planning & Approach | Requirements decomposition: ingestion, verification, synthesis, interactive Q&A |
| **2:15 – 3:30** | 3. Tech Stack & Architecture | FastAPI, Python 3.14, Pydantic V2, Vanilla JS/CSS, dual execution engine |
| **3:30 – 4:45** | 4. Use of AI & Hallucination Mitigation | Verbatim verification layer, closed-domain prompting, semantic guardrails |
| **4:45 – 5:45** | 5. Key Engineering Challenges | Deep-link synchronization, citation integrity, zero-key standalone reliability |
| **5:45 – 7:30** | 6. Live Application Demo | Interview Guide matrix, deep-link click, cross-call synthesis, interactive Q&A |
| **7:30 – 8:30** | 7. Scaling 3 to 30+ Calls & Disclosure | Enterprise roadmap (pgvector, Map-Reduce, RAGAS) + AI Transparency statement |

---

## 🎙️ Section-by-Section Script & Talking Points

### 1. Understanding of the Problem (0:00 – 1:00)
**On-Screen:** *Show the application homepage on `http://localhost:8000` with the hero metadata strip visible.*

> "Hi everyone, thank you for the opportunity to present my technical case study submission for the AI Engineer role at Hasamex.
>
> In private equity, venture capital, and strategic consulting, expert calls are the primary vehicle for primary qualitative due diligence. However, synthesizing qualitative calls suffers from three major operational bottlenecks:
> 1. **Time-consuming manual extraction:** Analysts spend hours manually mapping transcripts to an interview guide.
> 2. **Loss of traceability:** Key insights are often summarized without direct verbatim citations or timestamps, making auditability difficult.
> 3. **Thematic blindness:** Finding subtle consensus points and strategic divergences across international experts—such as comparing French, German, and UK hospital procurement—is difficult when reading calls in isolation.
>
> The objective of this case was to build an intelligent, hallucination-free application that ingests three expert calls on the European Robotic Surgery Market, automatically answers the 6-question interview guide with exact quotes and timestamps, synthesizes common themes and disagreements, and enables interactive cross-transcript Q&A."

---

### 2. Planning & Technical Approach (1:00 – 2:15)
**On-Screen:** *Click the **Architecture & Scale** tab and scroll to Section 1 & 2.*

> "When planning this application, my primary design principle was **strict traceability and zero hallucination**. The assignment brief explicitly stated: *'Do not invent information. Every important answer should be traceable to the transcript.'*
>
> To achieve this, I broke the system into four decoupled layers:
> 1. **A Turn Segmentation Engine:** Rather than treating transcripts as flat text, the parser recognizes speaker boundaries and `MM:SS` timestamps, converting dialogue into structured conversational turns with metadata such as talk ratios and duration.
> 2. **A Verbatim Verification Layer:** Any quotation presented by the system is checked via character-level substring matching against the source text to guarantee 100% fidelity before it reaches the UI.
> 3. **A Dual-Engine Q&A Pipeline:** I implemented a hybrid retrieval mechanism that functions both with live cloud LLMs like Gemini 2.5 Flash and GPT-4o-mini, and with an offline deterministic verified engine so that the application works seamlessly out-of-the-box with zero API key dependencies.
> 4. **An Interactive Deep-Linked UI:** Rather than static text, every quote and timestamp is a clickable trigger that immediately navigates to and highlights the source dialogue in the transcript viewer."

---

### 3. Tech Stack & Decisions (2:15 – 3:30)
**On-Screen:** *Remain on the **Architecture & Scale** tab, pointing to the tech stack cards.*

> "For the tech stack, I chose:
> - **Backend:** **FastAPI** with **Python 3.14** and **Pydantic V2**. FastAPI provides asynchronous high-throughput REST endpoints, sub-10ms response times for local requests, and strict data validation.
> - **Frontend:** A custom-built **Vanilla JavaScript and CSS single-page application** served directly via FastAPI. I deliberately avoided bloated framework setups like heavyweight frontend dev servers so the entire application can be launched with a single command: `python main.py`. It includes dark and light mode themes, responsive layouts, and CSS keyframe pulse animations for citation highlighting.
> - **Testing:** A comprehensive **pytest** suite with 10 unit and integration tests covering parser accuracy, verbatim quote verification, and API contracts.
> - **Model Choice:** For generative tasks, I selected **Gemini 2.5 Flash** and **GPT-4o-mini** because their sub-350ms Time-to-First-Token and large context windows are ideal for multi-document qualitative research. Crucially, I built an offline verified engine as the default so evaluators never encounter API rate limits or setup friction."

---

### 4. Use of AI & Hallucination Mitigation (3:30 – 4:45)
**On-Screen:** *Scroll down to Section 4: Hallucination Reduction Strategy.*

> "In financial and clinical research, hallucinations are fatal. To make this application truly hallucination-proof, I implemented three defense mechanisms:
> 1. **Closed-Domain Constrained System Prompting:** When an LLM is active, the prompt enforces a closed-world assumption where the model is strictly forbidden from extrapolating beyond the retrieved transcript excerpts. It must cite the expert and timestamp for every single sentence.
> 2. **Out-of-Domain Guardrail Filter:** Before calling the model or search engine, the query passes through a domain relevance validator. If a user asks something out of scope—for example, *'What is Da Vinci robot pricing in Japan?'*—the system detects zero conceptual overlap and returns an explicit refusal stating that the topic is not covered in the European transcripts.
> 3. **Mathematical Substring Verification:** Every extracted quote is programmatically matched against raw text. Our test suite asserts a 100% verbatim match across all 6 guide questions for all 3 experts."

---

### 5. Key Engineering Challenges & Solutions (4:45 – 5:45)
**On-Screen:** *Click to the **Transcripts Explorer** tab to show the speaker turns and search.*

> "The biggest engineering challenges during development were:
> 1. **Non-standard timestamped transcript formats:** Transcripts often contain varying timestamp formats, speaker labels, and multi-line utterances. I engineered a robust regex turn-segmentation parser in `backend/parser.py` that cleanly handles irregular spacing, normalizes quotation marks, and calculates speaker talk-time ratios.
> 2. **Bidirectional Deep-Link Synchronization:** When a user clicks a citation in a complex matrix or chat bubble, the app needs to change tabs, update the dropdown selector to the relevant country, scroll to the exact DOM element, and visually highlight it. I solved this in `static/app.js` using asynchronous DOM inspection and a pulsing CSS keyframe animation.
> 3. **Zero-Friction Portability:** I ensured the app requires no external database setup or multipart C-dependencies, allowing anyone to clone the repo, run `pip install -r requirements.txt`, and immediately start `python main.py`."

---

### 6. Live Application Demo Walkthrough (5:45 – 7:30)
**On-Screen:** *Follow this exact sequence of clicks:*

1. **Interview Guide Matrix:**
   > *"Let's look at the working application. On the first tab, we have the **Interview Guide Analysis**. Here, all 6 project questions are mapped side-by-side across France (Dr. Jean Martin), Germany (Anna Keller), and the UK (Dr. Emily Carter). For each question, we see a concise summary, an exact verbatim quote, and a verified green badge."*
2. **Deep-Link Click:**
   > *"Notice what happens when I click the timestamp button `⏱ 01:20` under Dr. Jean Martin's answer on capital budget approval..."*
   *(Click `⏱ 01:20` — watch the screen switch to Transcripts Explorer, scroll down, and pulse the utterance in gold.)*
   > *"The app instantly navigates to the Transcripts Explorer, switches the call to France, and highlights Dr. Martin's exact utterance at 01:20. An analyst can verify the source in one click."*
3. **Cross-Call Synthesis:**
   > *(Click the **Cross-Call Synthesis** tab.)*
   > *"Next is the **Cross-Call Synthesis** tab. Here, we provide an Executive Market Synthesis and a comparative alignment matrix showing key decision gates, growth forecasts, and procurement timelines. Below that, we surface three unanimous consensus themes—such as how single-surgeon dependence is an economic failure mode across all three markets—followed by key disagreements, such as Germany's strict 9–18 month procurement consensus versus the UK's faster 6–9 month timeline."*
4. **Interactive Ask AI:**
   > *(Click the **Ask AI (Interactive Q&A)** tab.)*
   > *"Now let's test the interactive Q&A assistant. I'll click one of our quick prompt chips: 'What do experts say about training only one surgeon?'"*
   *(Click the chip and wait for the response to render.)*
   > *"The engine retrieves evidence across all three transcripts, returning a structured synthesis with direct quotes from Dr. Martin at 03:10, Anna Keller at 03:05, and Dr. Carter at 01:05, along with a 98% Grounding Confidence Score."*
5. **Hallucination Guard Test:**
   > *(Type into the chat box: `What is the price of Da Vinci in Japan?` and submit.)*
   > *"If I test an out-of-domain query like 'What is the price of Da Vinci in Japan?', the guardrail catches it immediately and informs the user that this topic is not mentioned in the European transcripts, preventing hallucination."*
6. **Export Dossier:**
   > *(Click the **Export Dossier** button in the navbar.)*
   > *"Finally, clicking 'Export Dossier' instantly compiles the full report into a clean Markdown briefing ready for executive distribution."*

---

### 7. Scaling to 30+ Calls & AI Transparency Disclosure (7:30 – 8:30)
**On-Screen:** *Return to the **Architecture & Scale** tab, Section 5.*

> "To answer the case study's prompt on scaling from 3 to 30+ transcripts:
> 1. **Vector Storage & Hybrid Search:** In an enterprise deployment with 30 or 300 calls, we would migrate from in-memory parsing to **pgvector** or **Qdrant**, indexing turn-level chunks with metadata tags for geography, hospital tier, and expert role. We'd use hybrid search combining BM25 keyword matching with dense embeddings.
> 2. **Hierarchical Map-Reduce Clustering:** For cross-call synthesis across 30+ calls, we would run parallel extraction maps against the interview guide, followed by hierarchical embedding clustering (K-Means/HDBSCAN) to identify recurring themes and statistical anomalies.
> 3. **Automated Diarization Pipeline:** We would ingest raw call recordings through Whisper or Google Speech-to-Text with speaker diarization to auto-generate timestamped transcripts.
> 4. **RAGAS Observability:** We would deploy continuous evaluation using RAGAS to monitor faithfulness and context recall.
>
> **AI Usage Transparency Disclosure:**
> In accordance with Hasamex's submission guidelines, I would like to disclose that AI coding tools were utilized to assist with rapid prototyping, boilerplate generation, and styling. The application architecture, algorithmic verification design, prompt engineering, and test assertions represent my own engineering decisions and implementation.
>
> All code, test suites, and documentation are available in the attached repository. Thank you for your time and consideration!"

---

## 💡 Quick Tips for Recording
- **Tool Recommendation:** Use **Loom**, **OBS Studio**, or **Zoom** (Record with camera and shared screen) to easily achieve the required Picture-in-Picture format.
- **Lighting & Audio:** Use headphones or a dedicated microphone for clear audio as requested in the submission criteria.
- **Resolution:** Record in 1080p. Keep the browser at full width so all columns in the matrix render cleanly.
