// CallSynth AI – Client Application Logic

const state = {
  activeTab: 'guide',
  transcripts: {},
  interviewGuide: [],
  synthesis: null,
  activeFilter: 'all',
  selectedTranscriptId: 'transcript_france',
  apiKey: localStorage.getItem('callsynth_api_key') || '',
  provider: localStorage.getItem('callsynth_provider') || 'auto',
  theme: localStorage.getItem('callsynth_theme') || 'dark'
};

// DOM Elements
const elements = {
  navTabs: document.querySelectorAll('.nav-tab'),
  tabPanes: document.querySelectorAll('.tab-pane'),
  themeToggle: document.getElementById('btn-theme-toggle'),
  btnConfigKey: document.getElementById('btn-config-key'),
  modelIndicator: document.getElementById('model-indicator'),
  modalApiKey: document.getElementById('modal-api-key'),
  modalClose: document.getElementById('modal-close'),
  btnSaveConfig: document.getElementById('btn-save-config'),
  cfgProvider: document.getElementById('cfg-provider'),
  cfgApiKey: document.getElementById('cfg-api-key'),
  toast: document.getElementById('toast'),
  
  // Tab 1 Elements
  guideContainer: document.getElementById('interview-guide-container'),
  filterChips: document.querySelectorAll('.filter-chip'),
  
  // Tab 2 Elements
  synthesisExec: document.getElementById('synthesis-executive-summary'),
  marketComparisonBody: document.getElementById('market-comparison-body'),
  commonThemesContainer: document.getElementById('common-themes-container'),
  disagreementsContainer: document.getElementById('disagreements-container'),
  
  // Tab 3 Elements
  chatMessages: document.getElementById('chat-messages'),
  chatForm: document.getElementById('chat-form'),
  chatInput: document.getElementById('chat-input'),
  latestCitationsList: document.getElementById('latest-citations-list'),
  promptChips: document.querySelectorAll('.prompt-chip'),
  
  // Tab 4 Elements
  transcriptSelector: document.getElementById('transcript-selector'),
  transcriptSearch: document.getElementById('transcript-search'),
  transcriptMetaBar: document.getElementById('transcript-meta-bar'),
  transcriptDialogue: document.getElementById('transcript-dialogue-viewer'),
  btnUpload: document.getElementById('btn-upload-transcript'),
  fileInput: document.getElementById('file-upload-input'),
  btnReset: document.getElementById('btn-reset-transcripts'),
  btnExport: document.getElementById('btn-export-dossier')
};

// Show Toast
function showToast(msg, duration = 3000) {
  elements.toast.textContent = msg;
  elements.toast.classList.remove('hidden');
  setTimeout(() => elements.toast.classList.add('hidden'), duration);
}

// Initialize Theme
function initTheme() {
  if (state.theme === 'light') {
    document.body.classList.remove('theme-dark');
    document.body.classList.add('theme-light');
  } else {
    document.body.classList.remove('theme-light');
    document.body.classList.add('theme-dark');
  }
}

// Switch Tab
function switchTab(tabName) {
  state.activeTab = tabName;
  elements.navTabs.forEach(tab => {
    if (tab.dataset.tab === tabName) {
      tab.classList.add('active');
    } else {
      tab.classList.remove('active');
    }
  });

  elements.tabPanes.forEach(pane => {
    if (pane.id === `tab-${tabName}`) {
      pane.classList.add('active');
    } else {
      pane.classList.remove('active');
    }
  });
}

// Deep Link to Transcript Turn
function jumpToTranscript(transcriptId, timestamp, targetQuote = null) {
  switchTab('transcripts');
  
  // Update selector if different
  if (elements.transcriptSelector.value !== transcriptId) {
    elements.transcriptSelector.value = transcriptId;
    state.selectedTranscriptId = transcriptId;
    renderTranscriptDialogue();
  }

  // Find turn matching timestamp or quote
  setTimeout(() => {
    const turns = document.querySelectorAll('.dialogue-turn');
    let matchedElem = null;

    turns.forEach(t => {
      const ts = t.dataset.timestamp;
      const text = t.querySelector('.turn-text')?.textContent || '';
      
      if (timestamp && ts === timestamp) {
        matchedElem = t;
      } else if (targetQuote && text.toLowerCase().includes(targetQuote.toLowerCase().slice(0, 30))) {
        matchedElem = t;
      }
    });

    if (matchedElem) {
      matchedElem.scrollIntoView({ behavior: 'smooth', block: 'center' });
      matchedElem.classList.add('highlight-pulse');
      setTimeout(() => matchedElem.classList.remove('highlight-pulse'), 3200);
      showToast(`Jumped to ${timestamp || 'turn'} in ${transcriptId.replace('transcript_', '').toUpperCase()}`);
    } else {
      showToast(`Timestamp ${timestamp} not found in this call`);
    }
  }, 100);
}

// API Calls & Renderers

// 1. Fetch Transcripts
async function fetchTranscripts() {
  try {
    const res = await fetch('/api/transcripts');
    const data = await res.json();
    state.transcripts = {};
    data.transcripts.forEach(t => {
      state.transcripts[t.metadata.id] = t;
    });
    
    // Update dropdown
    elements.transcriptSelector.innerHTML = '';
    data.transcripts.forEach(t => {
      const opt = document.createElement('option');
      opt.value = t.metadata.id;
      opt.textContent = `${t.metadata.flag} ${t.metadata.market} – ${t.metadata.expert_name} (${t.metadata.role})`;
      elements.transcriptSelector.appendChild(opt);
    });

    if (data.transcripts.length > 0) {
      state.selectedTranscriptId = data.transcripts[0].metadata.id;
      elements.transcriptSelector.value = state.selectedTranscriptId;
    }

    renderTranscriptDialogue();
  } catch (err) {
    console.error('Failed to load transcripts:', err);
  }
}

// Render Transcript Explorer
function renderTranscriptDialogue() {
  const current = state.transcripts[state.selectedTranscriptId];
  if (!current) return;

  const m = current.metadata;
  elements.transcriptMetaBar.innerHTML = `
    <div><strong>Expert:</strong> ${m.flag} ${m.expert_name}</div>
    <div><strong>Role:</strong> ${m.role}</div>
    <div><strong>Market:</strong> ${m.market}</div>
    <div><strong>Duration:</strong> ${m.duration_str}</div>
    <div><strong>Turns:</strong> ${m.total_turns}</div>
    <div><strong>Words:</strong> ${m.total_words} (Expert: ${m.expert_words}, Interviewer: ${m.interviewer_words})</div>
  `;

  const query = elements.transcriptSearch.value.trim().toLowerCase();
  elements.transcriptDialogue.innerHTML = '';

  current.turns.forEach(turn => {
    if (query && !turn.text.toLowerCase().includes(query) && !turn.speaker.toLowerCase().includes(query)) {
      return;
    }

    const turnCard = document.createElement('div');
    turnCard.className = `dialogue-turn ${turn.is_expert ? 'expert-turn' : 'interviewer-turn'}`;
    turnCard.dataset.timestamp = turn.timestamp;
    turnCard.dataset.turnId = turn.turn_id;

    turnCard.innerHTML = `
      <div class="turn-header">
        <span class="speaker-tag">${turn.speaker}</span>
        <span class="ts-badge" title="Click to copy timestamp">⏱ ${turn.timestamp}</span>
      </div>
      <div class="turn-text">${highlightSearch(turn.text, query)}</div>
    `;

    elements.transcriptDialogue.appendChild(turnCard);
  });
}

function highlightSearch(text, query) {
  if (!query) return text;
  const re = new RegExp(`(${query})`, 'gi');
  return text.replace(re, '<mark style="background: rgba(210, 153, 34, 0.4); color: inherit; padding: 0 2px;">$1</mark>');
}

// 2. Fetch & Render Interview Guide Matrix
async function fetchInterviewGuide() {
  try {
    const res = await fetch('/api/interview-guide');
    const data = await res.json();
    state.interviewGuide = data.analysis;
    renderInterviewGuide();
  } catch (err) {
    console.error('Failed to load interview guide:', err);
    elements.guideContainer.innerHTML = `<div class="error-state">Error loading interview guide.</div>`;
  }
}

function renderInterviewGuide() {
  elements.guideContainer.innerHTML = '';
  
  state.interviewGuide.forEach(q => {
    const card = document.createElement('div');
    card.className = 'question-card';

    let answersHtml = '';
    const expEntries = Object.entries(q.answers);

    expEntries.forEach(([expId, ans]) => {
      // Filter check
      if (state.activeFilter !== 'all') {
        if (state.activeFilter === 'france' && !expId.includes('france')) return;
        if (state.activeFilter === 'germany' && !expId.includes('germany')) return;
        if (state.activeFilter === 'uk' && !expId.includes('uk')) return;
      }

      const verifBadge = ans.verification?.is_verbatim 
        ? `<span class="quote-verification-tag">✓ 100% Verbatim Verified</span>`
        : `<span class="quote-verification-tag" style="color: var(--accent-amber);">~ ${Math.round((ans.verification?.similarity_score || 0)*100)}% Matched</span>`;

      answersHtml += `
        <div class="expert-answer-box">
          <div class="expert-card-top">
            <div class="expert-info">
              <span class="expert-flag">${ans.flag}</span>
              <div>
                <div class="expert-name">${ans.expert_name}</div>
                <div class="expert-role">${ans.market} • ${ans.role}</div>
              </div>
            </div>
            <button class="ts-badge btn-jump" data-target-exp="${ans.expert_id}" data-target-ts="${ans.timestamp}" data-target-quote="${encodeURIComponent(ans.exact_quote)}">
              ⏱ ${ans.timestamp}
            </button>
          </div>
          <p class="answer-summary">${ans.summary_answer}</p>
          <div class="quote-box btn-jump" data-target-exp="${ans.expert_id}" data-target-ts="${ans.timestamp}" data-target-quote="${encodeURIComponent(ans.exact_quote)}" title="Click to jump to exact utterance in transcript">
            "${ans.exact_quote}"
          </div>
          ${verifBadge}
        </div>
      `;
    });

    card.innerHTML = `
      <div class="question-header">
        <div>
          <div class="q-meta">
            <span class="q-num">Q${q.question_id}</span>
            <span class="q-category">${q.category}</span>
          </div>
          <div class="question-title">${q.question_text}</div>
          <div class="q-takeaway">💡 <strong>Key Cross-Market Takeaway:</strong> ${q.cross_market_takeaway}</div>
        </div>
      </div>
      <div class="expert-answers-row">
        ${answersHtml}
      </div>
    `;

    elements.guideContainer.appendChild(card);
  });

  // Attach jump listeners
  document.querySelectorAll('.btn-jump').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const expId = btn.dataset.targetExp;
      const ts = btn.dataset.targetTs;
      const q = decodeURIComponent(btn.dataset.targetQuote || '');
      jumpToTranscript(expId, ts, q);
    });
  });
}

// 3. Fetch & Render Cross-Call Synthesis
async function fetchSynthesis() {
  try {
    const res = await fetch('/api/synthesis');
    const data = await res.json();
    state.synthesis = data;
    renderSynthesis();
  } catch (err) {
    console.error('Failed to load synthesis:', err);
  }
}

function renderSynthesis() {
  if (!state.synthesis) return;
  const s = state.synthesis;

  // Executive summary
  elements.synthesisExec.textContent = s.executive_summary;

  // Market comparison table
  elements.marketComparisonBody.innerHTML = '';
  s.market_comparison.forEach(m => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>
        <strong>${m.flag} ${m.market}</strong><br>
        <span class="expert-role">${m.expert} (${m.role})</span>
      </td>
      <td><strong>${m.primary_decision_gate}</strong></td>
      <td><span class="badge-blue">${m.adoption_growth_forecast}</span></td>
      <td><span class="badge-amber">${m.purchasing_timeline}</span></td>
      <td>${m.top_barrier}</td>
      <td><em>${m.view_on_roi}</em></td>
    `;
    elements.marketComparisonBody.appendChild(tr);
  });

  // Common Themes
  elements.commonThemesContainer.innerHTML = '';
  s.common_themes.forEach(t => {
    const card = document.createElement('div');
    card.className = 'theme-card';

    let evidenceHtml = '';
    t.evidence.forEach(ev => {
      const expId = ev.market.toLowerCase().includes('france') ? 'transcript_france' :
                    ev.market.toLowerCase().includes('germany') ? 'transcript_germany' : 'transcript_uk';
      evidenceHtml += `
        <div class="evidence-pill btn-jump" data-target-exp="${expId}" data-target-ts="${ev.timestamp}" data-target-quote="${encodeURIComponent(ev.quote)}">
          <strong>${ev.flag} ${ev.expert_name} [${ev.timestamp}]:</strong> "${ev.quote}"
        </div>
      `;
    });

    card.innerHTML = `
      <div class="theme-header">
        <span class="theme-badge">✓ ${t.consensus_level}</span>
        <div class="theme-title">${t.title}</div>
      </div>
      <p class="theme-body">${t.synthesis}</p>
      <div class="theme-implication">
        <strong>Strategic Takeaway:</strong> ${t.strategic_implication}
      </div>
      <div class="theme-evidence-list">
        <span style="font-size: 0.72rem; font-weight: 700; color: var(--text-muted);">SUPPORTING TRANSCRIPT EVIDENCE:</span>
        ${evidenceHtml}
      </div>
    `;
    elements.commonThemesContainer.appendChild(card);
  });

  // Disagreements
  elements.disagreementsContainer.innerHTML = '';
  s.disagreements.forEach(d => {
    const card = document.createElement('div');
    card.className = 'disagree-card';

    let stancesHtml = '';
    Object.entries(d.expert_stances).forEach(([expLabel, st]) => {
      const expId = expLabel.toLowerCase().includes('france') ? 'transcript_france' :
                    expLabel.toLowerCase().includes('germany') ? 'transcript_germany' : 'transcript_uk';
      stancesHtml += `
        <div class="stance-box">
          <div class="stance-title">${expLabel}</div>
          <div style="font-weight: 700; font-size: 0.85rem; margin-bottom: 0.35rem;">${st.stance}</div>
          <p class="stance-text">${st.summary}</p>
          <div class="quote-box btn-jump" data-target-exp="${expId}" data-target-ts="${st.timestamp}" data-target-quote="${encodeURIComponent(st.quote)}">
            "${st.quote}" <span style="font-weight:600;">[${st.timestamp}]</span>
          </div>
        </div>
      `;
    });

    card.innerHTML = `
      <div class="disagree-header">
        <span class="theme-badge" style="color: var(--accent-amber); background: var(--accent-amber-subtle);">⚡ Divergence</span>
        <div class="disagree-title">${d.topic}</div>
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.2rem;">${d.description}</p>
      </div>
      <div class="disagree-columns">
        ${stancesHtml}
      </div>
      <div class="disagree-analysis">
        <strong>Cross-Market Comparative Analysis:</strong> ${d.analysis}
      </div>
    `;
    elements.disagreementsContainer.appendChild(card);
  });

  // Attach jump listeners
  document.querySelectorAll('.btn-jump').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const expId = btn.dataset.targetExp;
      const ts = btn.dataset.targetTs;
      const q = decodeURIComponent(btn.dataset.targetQuote || '');
      jumpToTranscript(expId, ts, q);
    });
  });
}

// 4. Interactive Q&A Engine
async function handleChatSubmit(e) {
  if (e) e.preventDefault();
  const query = elements.chatInput.value.trim();
  if (!query) return;

  // Append user message
  appendChatMessage('user', query);
  elements.chatInput.value = '';

  // Append loading indicator
  const loadingMsg = appendChatMessage('assistant', 'Searching and analyzing transcripts with grounding verification...');

  try {
    const res = await fetch('/api/qa', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: query,
        api_key: state.apiKey || null,
        provider: state.provider || 'auto'
      })
    });

    const data = await res.json();
    loadingMsg.remove();

    // Render response
    renderQAResponse(data);
  } catch (err) {
    loadingMsg.remove();
    appendChatMessage('assistant', `⚠️ Error processing query: ${err.message}`);
  }
}

function appendChatMessage(role, text) {
  const msg = document.createElement('div');
  msg.className = `chat-message ${role}`;
  msg.innerHTML = `
    <div class="msg-avatar">${role === 'user' ? 'YOU' : 'AI'}</div>
    <div class="msg-content"><p>${text}</p></div>
  `;
  elements.chatMessages.appendChild(msg);
  elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
  return msg;
}

function renderQAResponse(data) {
  const msg = document.createElement('div');
  msg.className = 'chat-message assistant';

  let citationsHtml = '';
  if (data.citations && data.citations.length > 0) {
    citationsHtml = `
      <div style="margin-top: 0.85rem; border-top: 1px solid var(--border-subtle); padding-top: 0.75rem;">
        <span style="font-size: 0.72rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">GROUNDED TRANSCRIPT CITATIONS:</span>
        <div style="display: flex; flex-direction: column; gap: 0.45rem; margin-top: 0.4rem;">
    `;
    data.citations.forEach(c => {
      const expId = c.market.toLowerCase().includes('france') ? 'transcript_france' :
                    c.market.toLowerCase().includes('germany') ? 'transcript_germany' : 'transcript_uk';
      citationsHtml += `
        <div class="quote-box btn-jump" data-target-exp="${expId}" data-target-ts="${c.timestamp}" data-target-quote="${encodeURIComponent(c.quote)}" style="margin-top:0;">
          <strong>${c.flag} ${c.expert_name} [${c.timestamp}]:</strong> "${c.quote}"
        </div>
      `;
    });
    citationsHtml += `</div></div>`;
  }

  // Model & Confidence Badge
  const confidencePercent = Math.round(data.confidence_score * 100);
  const badgeClass = data.is_grounded ? 'badge-green' : 'badge-amber';
  const metaHtml = `
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.65rem; font-size: 0.7rem; color: var(--text-muted);">
      <span>Model: <strong>${data.model_used}</strong></span>
      <span class="${badgeClass}">Grounding Confidence: ${confidencePercent}%</span>
    </div>
  `;

  // Format markdown-like bold/italic in answer
  const formattedAnswer = data.answer
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\n\n/g, '</p><p>')
    .replace(/\n/g, '<br>');

  msg.innerHTML = `
    <div class="msg-avatar">AI</div>
    <div class="msg-content">
      <p>${formattedAnswer}</p>
      ${citationsHtml}
      ${metaHtml}
    </div>
  `;

  elements.chatMessages.appendChild(msg);
  elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;

  // Update sidebar citations
  if (data.citations && data.citations.length > 0) {
    elements.latestCitationsList.innerHTML = '';
    data.citations.forEach(c => {
      const expId = c.market.toLowerCase().includes('france') ? 'transcript_france' :
                    c.market.toLowerCase().includes('germany') ? 'transcript_germany' : 'transcript_uk';
      const item = document.createElement('div');
      item.className = 'evidence-pill btn-jump';
      item.dataset.targetExp = expId;
      item.dataset.targetTs = c.timestamp;
      item.dataset.targetQuote = encodeURIComponent(c.quote);
      item.style.marginBottom = '0.45rem';
      item.innerHTML = `<strong>${c.flag} ${c.expert_name} [${c.timestamp}]:</strong> "${c.quote.slice(0, 80)}..."`;
      elements.latestCitationsList.appendChild(item);
    });
  }

  // Re-attach jump listeners
  msg.querySelectorAll('.btn-jump').forEach(btn => {
    btn.addEventListener('click', () => {
      jumpToTranscript(btn.dataset.targetExp, btn.dataset.targetTs, decodeURIComponent(btn.dataset.targetQuote || ''));
    });
  });
  elements.latestCitationsList.querySelectorAll('.btn-jump').forEach(btn => {
    btn.addEventListener('click', () => {
      jumpToTranscript(btn.dataset.targetExp, btn.dataset.targetTs, decodeURIComponent(btn.dataset.targetQuote || ''));
    });
  });
}

// 5. Export Dossier to Markdown / Download
function exportDossier() {
  let md = `# Hasamex Expert Call Dossier: European Robotic Surgery Market\n\n`;
  md += `**Date:** September 2026\n`;
  md += `**Case Study:** Analysis of 3 Expert Call Transcripts (France, Germany, UK)\n\n---\n\n`;
  
  if (state.synthesis) {
    md += `## 1. Executive Market Synthesis\n\n${state.synthesis.executive_summary}\n\n---\n\n`;
    
    md += `## 2. Market-by-Market Comparison\n\n`;
    md += `| Market | Expert & Role | Primary Decision Gate | 3-5 Year Growth | Timeline | Top Bottleneck |\n`;
    md += `| :--- | :--- | :--- | :--- | :--- | :--- |\n`;
    state.synthesis.market_comparison.forEach(m => {
      md += `| ${m.flag} ${m.market} | ${m.expert} (${m.role}) | ${m.primary_decision_gate} | ${m.adoption_growth_forecast} | ${m.purchasing_timeline} | ${m.top_barrier} |\n`;
    });
    md += `\n---\n\n`;
    
    md += `## 3. Common Themes (Industry Consensus)\n\n`;
    state.synthesis.common_themes.forEach(t => {
      md += `### ${t.title} (${t.consensus_level})\n${t.synthesis}\n\n`;
      md += `**Strategic Implication:** ${t.strategic_implication}\n\n`;
      md += `*Evidence:*\n`;
      t.evidence.forEach(e => {
        md += `- **${e.flag} ${e.expert_name} [${e.timestamp}]:** "${e.quote}"\n`;
      });
      md += `\n`;
    });
    md += `---\n\n`;

    md += `## 4. Key Strategic Disagreements\n\n`;
    state.synthesis.disagreements.forEach(d => {
      md += `### ${d.topic}\n${d.description}\n\n`;
      Object.entries(d.expert_stances).forEach(([exp, st]) => {
        md += `- **${exp}:** ${st.stance} - "${st.quote}" [${st.timestamp}]\n`;
      });
      md += `\n**Analysis:** ${d.analysis}\n\n`;
    });
    md += `---\n\n`;
  }

  if (state.interviewGuide) {
    md += `## 5. Complete Interview Guide Answers (Questions 1-6)\n\n`;
    state.interviewGuide.forEach(q => {
      md += `### Q${q.question_id}: ${q.question_text}\n`;
      md += `*Takeaway: ${q.cross_market_takeaway}*\n\n`;
      Object.values(q.answers).forEach(a => {
        md += `#### ${a.flag} ${a.expert_name} (${a.market}, ${a.role})\n`;
        md += `- **Answer:** ${a.summary_answer}\n`;
        md += `- **Verbatim Quote:** "${a.exact_quote}" [Timestamp: ${a.timestamp}]\n\n`;
      });
    });
  }

  const blob = new Blob([md], { type: 'text/markdown;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `Hasamex_Robotic_Surgery_Dossier_${new Date().toISOString().slice(0,10)}.md`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  showToast('Downloaded Full Case Dossier (Markdown)');
}

// Event Listeners
function setupListeners() {
  // Tabs
  elements.navTabs.forEach(tab => {
    tab.addEventListener('click', () => switchTab(tab.dataset.tab));
  });

  // Filter Chips in Guide
  elements.filterChips.forEach(chip => {
    chip.addEventListener('click', () => {
      elements.filterChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      state.activeFilter = chip.dataset.filter;
      renderInterviewGuide();
    });
  });

  // Theme Toggle
  elements.themeToggle.addEventListener('click', () => {
    state.theme = state.theme === 'dark' ? 'light' : 'dark';
    localStorage.setItem('callsynth_theme', state.theme);
    initTheme();
  });

  // Transcript Explorer Controls
  elements.transcriptSelector.addEventListener('change', (e) => {
    state.selectedTranscriptId = e.target.value;
    renderTranscriptDialogue();
  });

  elements.transcriptSearch.addEventListener('input', () => {
    renderTranscriptDialogue();
  });

  // Upload Transcript
  elements.btnUpload.addEventListener('click', () => {
    elements.fileInput.click();
  });

  elements.fileInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    try {
      showToast('Reading & parsing transcript...');
      const text = await file.text();
      const res = await fetch('/api/upload-transcript', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          filename: file.name,
          content: text
        })
      });
      const data = await res.json();
      showToast(data.message);
      await fetchTranscripts();
      await fetchInterviewGuide();
    } catch (err) {
      showToast(`Upload failed: ${err.message}`);
    }
  });

  // Reset Transcripts
  elements.btnReset.addEventListener('click', async () => {
    if (confirm('Reset to the 3 original case pack transcripts?')) {
      await fetch('/api/reset-transcripts', { method: 'POST' });
      await fetchTranscripts();
      await fetchInterviewGuide();
      await fetchSynthesis();
      showToast('Reset to default 3 case pack transcripts');
    }
  });

  // Chat Form
  elements.chatForm.addEventListener('submit', handleChatSubmit);

  // Quick Prompt Chips
  elements.promptChips.forEach(chip => {
    chip.addEventListener('click', () => {
      elements.chatInput.value = chip.textContent;
      handleChatSubmit();
    });
  });

  // Export Dossier
  elements.btnExport.addEventListener('click', exportDossier);

  // Modal API Key
  elements.btnConfigKey.addEventListener('click', () => {
    elements.cfgProvider.value = state.provider;
    elements.cfgApiKey.value = state.apiKey;
    elements.modalApiKey.classList.remove('hidden');
  });

  elements.modalClose.addEventListener('click', () => {
    elements.modalApiKey.classList.add('hidden');
  });

  elements.btnSaveConfig.addEventListener('click', () => {
    state.provider = elements.cfgProvider.value;
    state.apiKey = elements.cfgApiKey.value.trim();
    localStorage.setItem('callsynth_provider', state.provider);
    localStorage.setItem('callsynth_api_key', state.apiKey);

    if (state.apiKey) {
      elements.modelIndicator.textContent = state.provider === 'gemini' ? 'Gemini 2.5' : 'GPT-4o-mini';
      showToast('API Key saved! Real-time LLM enabled.');
    } else {
      elements.modelIndicator.textContent = 'Local Engine';
      showToast('Using Built-in Verified Offline Engine');
    }
    elements.modalApiKey.classList.add('hidden');
  });
}

// Initial Boot
async function init() {
  initTheme();
  setupListeners();
  
  if (state.apiKey) {
    elements.modelIndicator.textContent = state.provider === 'gemini' ? 'Gemini 2.5' : 'GPT-4o-mini';
  }

  await Promise.all([
    fetchTranscripts(),
    fetchInterviewGuide(),
    fetchSynthesis()
  ]);
}

window.addEventListener('DOMContentLoaded', init);
