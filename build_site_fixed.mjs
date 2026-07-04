import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const cardsPath = path.join(root, "mayuan_cards_500.json");
const indexPath = path.join(root, "index.html");
const quizPath = path.join(root, "quiz.html");

const cards = JSON.parse(fs.readFileSync(cardsPath, "utf8"));

const chapterCounts = Object.create(null);
for (const card of cards) {
  chapterCounts[card.chapter] = (chapterCounts[card.chapter] || 0) + 1;
}
const chapters = [];
for (const card of cards) {
  if (!chapters.includes(card.chapter)) chapters.push(card.chapter);
}

const quizItems = [];
for (let i = 0; i < cards.length && quizItems.length < 12; i += 1) {
  const card = cards[i];
  const distractors = [];
  for (const other of cards) {
    if (other.answer !== card.answer && !distractors.includes(other.answer)) {
      distractors.push(other.answer);
    }
    if (distractors.length === 3) break;
  }
  if (distractors.length < 3) continue;
  const options = [card.answer, ...distractors];
  const shift = i % 4;
  const rotated = options.slice(shift).concat(options.slice(0, shift));
  quizItems.push({
    question: card.question,
    chapter: card.chapter,
    options: rotated,
    answer: rotated.indexOf(card.answer),
    explain: `这题对应 ${card.chapter}，标准表述要锁定原答案。`
  });
}

const json = (value) => JSON.stringify(value).replace(/</g, "\\u003c");

function commonHead(title) {
  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>${title}</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f5eee6;
      --paper: rgba(255, 251, 246, 0.9);
      --paper-strong: rgba(255, 251, 246, 0.97);
      --ink: #1f2535;
      --muted: #7a7f8d;
      --line: rgba(31, 37, 53, 0.1);
      --accent: #3467e8;
      --accent-deep: #2853bf;
      --accent-soft: rgba(52, 103, 232, 0.12);
      --green: #22a34d;
      --green-soft: rgba(34, 163, 77, 0.14);
      --shadow: 0 24px 60px rgba(83, 66, 45, 0.12);
      --radius: 28px;
      --max: 1180px;
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top right, rgba(52, 103, 232, 0.1), transparent 22%),
        radial-gradient(circle at left 12%, rgba(34, 163, 77, 0.08), transparent 18%),
        linear-gradient(180deg, #f7f1e8 0%, #efe5d9 100%);
    }
    a { color: inherit; text-decoration: none; }
    button, select { font: inherit; }
    .shell { width: min(calc(100% - 24px), var(--max)); margin: 18px auto 36px; }
    .topbar, .progress-card, .card-shell, .quiz-card, .result-card {
      border-radius: var(--radius);
      border: 1px solid rgba(255, 255, 255, 0.72);
      background: var(--paper);
      box-shadow: var(--shadow);
      backdrop-filter: blur(14px);
    }
    .topbar {
      position: sticky;
      top: 10px;
      z-index: 10;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      padding: 12px 16px;
      margin-bottom: 18px;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      min-width: 0;
    }
    .seal {
      width: 44px;
      height: 44px;
      border-radius: 50%;
      display: grid;
      place-items: center;
      color: #fffaf4;
      font-weight: 800;
      background: linear-gradient(135deg, #d66f4d, #ae3917);
    }
    .brand strong, .brand span {
      display: block;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .brand strong { letter-spacing: 0.04em; }
    .brand span { font-size: 12px; color: var(--muted); }
    .nav {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }
    .nav a {
      padding: 10px 14px;
      border-radius: 999px;
      color: var(--muted);
    }
    .nav a.active {
      background: var(--accent-soft);
      color: var(--accent-deep);
    }
    .nav a:hover {
      background: rgba(0, 0, 0, 0.05);
      color: var(--ink);
    }
    .section-head {
      margin-bottom: 14px;
    }
    .section-head h1, .section-head h2 {
      margin: 0 0 8px;
      font-size: clamp(28px, 4vw, 42px);
      letter-spacing: -0.04em;
    }
    .section-head p {
      margin: 0;
      color: var(--muted);
      line-height: 1.7;
    }
    .eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 10px 14px;
      border-radius: 999px;
      background: rgba(0, 0, 0, 0.05);
      color: var(--muted);
      font-size: 12px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }
    .tools {
      display: grid;
      grid-template-columns: 1.2fr 1fr 1fr;
      gap: 10px;
      margin-bottom: 16px;
    }
    select, button {
      border: 1px solid var(--line);
      background: rgba(255, 255, 255, 0.94);
      color: var(--ink);
      border-radius: 999px;
      padding: 12px 14px;
    }
    button {
      cursor: pointer;
      transition: transform 0.18s ease, background 0.18s ease, border-color 0.18s ease;
    }
    button:hover { transform: translateY(-1px); }
    .toggle.active {
      background: var(--accent-soft);
      border-color: rgba(52, 103, 232, 0.24);
      color: var(--accent-deep);
    }
    .progress-card {
      padding: 18px 20px;
      margin-bottom: 16px;
      background: var(--paper-strong);
    }
    .progress-card-head {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      gap: 14px;
      margin-bottom: 10px;
    }
    .progress-card-head strong {
      font-size: 18px;
    }
    .progress-card-head span {
      color: var(--muted);
      font-size: 15px;
    }
    .progress-track {
      width: 100%;
      height: 10px;
      border-radius: 999px;
      overflow: hidden;
      background: rgba(0, 0, 0, 0.08);
    }
    .progress-fill {
      display: block;
      width: 0;
      height: 100%;
      border-radius: 999px;
      background: linear-gradient(90deg, var(--green), #4b7767);
    }
    .card-shell {
      overflow: hidden;
      background: linear-gradient(180deg, rgba(255,255,255,0.95), rgba(249,242,235,0.96));
    }
    .card-stage {
      position: relative;
    }
    .card {
      position: relative;
      min-height: clamp(430px, 72vh, 620px);
      cursor: pointer;
      overflow: hidden;
      touch-action: pan-y;
    }
    .card-main {
      min-height: clamp(430px, 72vh, 620px);
      padding: 22px 22px 18px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .card-top {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 12px;
    }
    .pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 10px 12px;
      border-radius: 999px;
      background: rgba(0, 0, 0, 0.05);
      color: var(--muted);
      font-size: 13px;
    }
    .helper-bar {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .mini-toggle {
      padding: 10px 14px;
      white-space: nowrap;
    }
    .helper-chip {
      padding: 10px 14px;
      border-radius: 999px;
      background: rgba(255,255,255,0.88);
      border: 1px solid rgba(52, 103, 232, 0.08);
      color: #8890a5;
      font-size: 13px;
      white-space: nowrap;
    }
    .mastery-btn {
      width: 52px;
      height: 52px;
      border-radius: 50%;
      border: none;
      background: var(--green-soft);
      color: var(--green);
      font-size: 22px;
      font-weight: 700;
    }
    .mastery-btn.active {
      background: var(--green);
      color: #f3fff5;
    }
    .question-wrap {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 8px 18px 18px;
      transition: transform 0.42s cubic-bezier(0.2, 0.7, 0.2, 1), opacity 0.32s ease;
    }
    .question-index {
      color: var(--accent);
      font-size: 18px;
      font-weight: 800;
      letter-spacing: 0.16em;
      text-transform: uppercase;
    }
    .question-wrap h2 {
      margin: 14px 0 0;
      max-width: 11ch;
      font-size: clamp(30px, 3.8vw, 52px);
      line-height: 1.12;
      letter-spacing: -0.05em;
      transition: transform 0.42s cubic-bezier(0.2, 0.7, 0.2, 1), font-size 0.32s ease;
    }
    .question-foot {
      padding: 0 10px 0;
      color: var(--muted);
      line-height: 1.7;
      text-align: center;
      font-size: 14px;
    }
    .answer-panel {
      position: absolute;
      left: 0;
      right: 0;
      bottom: 0;
      height: min(30vh, 240px);
      background: linear-gradient(180deg, rgba(52, 103, 232, 0.98), rgba(44, 92, 214, 0.98));
      color: #f6f9ff;
      transition: opacity 0.28s ease, transform 0.46s cubic-bezier(0.2, 0.7, 0.2, 1);
      opacity: 0;
      transform: translateY(100%);
      padding: 22px 28px 26px;
      text-align: center;
      border-top-left-radius: 28px;
      border-top-right-radius: 28px;
    }
    .answer-panel-inner {
      min-height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      gap: 14px;
    }
    .answer-label {
      font-size: 16px;
      font-weight: 800;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      opacity: 0.85;
    }
    .answer-text {
      font-size: clamp(24px, 3.2vw, 44px);
      line-height: 1.24;
      letter-spacing: -0.04em;
      font-weight: 800;
    }
    .card.show .question-wrap {
      transform: translateY(-88px) scale(0.92);
      opacity: 0.98;
    }
    .card.show .question-wrap h2 {
      transform: scale(0.84);
    }
    .card.show .answer-panel {
      opacity: 1;
      transform: translateY(0);
    }
    .card-actions {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      justify-content: center;
      margin-top: 18px;
    }
    .nav-floats {
      position: absolute;
      inset: 0;
      pointer-events: none;
    }
    .nav-float {
      position: absolute;
      top: 50%;
      width: 64px;
      height: 64px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      transform: translateY(-50%);
      pointer-events: auto;
      box-shadow: 0 14px 28px rgba(83, 66, 45, 0.14);
      padding: 0;
    }
    .nav-float.prev { left: -84px; }
    .nav-float.next { right: -84px; }
    .nav-float:hover { transform: translateY(-50%) scale(1.04); }
    .nav-float:active { transform: translateY(-50%) scale(0.96); }
    .nav-float svg {
      width: 24px;
      height: 24px;
      stroke: currentColor;
      stroke-width: 3.2;
      fill: none;
      stroke-linecap: round;
      stroke-linejoin: round;
    }
    .quiz-layout {
      display: grid;
      grid-template-columns: 1.1fr 0.9fr;
      gap: 18px;
    }
    .quiz-card, .result-card {
      padding: 18px;
      background: var(--paper-strong);
    }
    .quiz-card h3, .result-card h3 {
      margin: 0 0 8px;
      font-size: 18px;
    }
    .quiz-step {
      margin-bottom: 12px;
    }
    .quiz-question {
      margin: 0 0 10px;
      font-size: clamp(28px, 4vw, 40px);
      line-height: 1.18;
      letter-spacing: -0.04em;
    }
    .quiz-options {
      display: grid;
      gap: 10px;
      margin-top: 18px;
    }
    .quiz-options button {
      text-align: left;
      border-radius: 18px;
      padding: 14px 16px;
      background: rgba(255, 255, 255, 0.78);
    }
    .quiz-options button.selected {
      background: rgba(47, 94, 79, 0.16);
      border-color: rgba(47, 94, 79, 0.28);
    }
    .quiz-actions {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-top: 14px;
    }
    .score {
      display: flex;
      align-items: baseline;
      gap: 6px;
      margin-bottom: 10px;
    }
    .score strong {
      font-size: 54px;
      line-height: 1;
    }
    .mistake {
      margin-top: 12px;
      padding: 14px;
      border-radius: 18px;
      background: rgba(255, 255, 255, 0.68);
      border: 1px solid var(--line);
    }
    .muted {
      color: var(--muted);
      line-height: 1.7;
    }
    footer {
      padding: 14px 0 6px;
      text-align: center;
      color: var(--muted);
    }
    @media (max-width: 980px) {
      .tools, .quiz-layout {
        grid-template-columns: 1fr;
      }
      .topbar {
        position: static;
        flex-direction: column;
        align-items: stretch;
        gap: 14px;
        padding: 18px;
      }
      .brand {
        width: 100%;
      }
      .nav {
        display: grid;
        grid-template-columns: 1fr 1fr;
      }
      .nav a {
        text-align: center;
      }
      .section-head {
        margin-bottom: 10px;
      }
      .progress-card-head {
        flex-direction: column;
        align-items: flex-start;
      }
      .card-stage {
        overflow: hidden;
      }
      .card-top {
        flex-direction: column;
        align-items: stretch;
      }
      .question-wrap h2, .quiz-question {
        max-width: none;
      }
      .helper-bar {
        width: 100%;
        justify-content: space-between;
        gap: 10px;
      }
      .helper-chip {
        flex: 1;
        min-width: 0;
        white-space: normal;
        text-align: center;
      }
      .card,
      .card-main {
        min-height: clamp(420px, 66svh, 620px);
      }
      .nav-float {
        display: none;
      }
      .question-wrap {
        padding: 12px 10px 14px;
      }
      .question-wrap h2 {
        font-size: clamp(26px, 7.4vw, 42px);
      }
      .answer-panel {
        height: min(28svh, 220px);
      }
      .answer-text {
        font-size: clamp(22px, 5.6vw, 34px);
      }
      .card-actions {
        display: grid;
        grid-template-columns: 1fr;
      }
      .card-actions button,
      .mini-toggle {
        width: 100%;
      }
    }
    @media (max-width: 640px) {
      .shell {
        width: min(calc(100% - 16px), var(--max));
        margin: 10px auto 24px;
      }
      .topbar,
      .progress-card,
      .card-shell,
      .quiz-card,
      .result-card {
        border-radius: 24px;
      }
      .brand strong {
        font-size: 18px;
      }
      .brand span {
        font-size: 13px;
      }
      .section-head h1 {
        font-size: clamp(24px, 8vw, 34px);
      }
      .pill {
        align-self: flex-start;
      }
      .mastery-btn {
        width: 48px;
        height: 48px;
      }
      .question-wrap h2 {
        font-size: clamp(24px, 8.8vw, 38px);
        line-height: 1.18;
      }
      .question-index {
        font-size: 16px;
      }
      .question-foot {
        padding-bottom: 4px;
      }
      .answer-panel {
        padding: 18px 18px 22px;
      }
    }
  </style>
</head>`;
}

function buildIndexHtml() {
  return `${commonHead("马原手卡")}
<body>
  <div class="shell">
    <div class="topbar">
      <div class="brand">
        <div class="seal">马原</div>
        <div>
          <strong>马原知识手卡</strong>
          <span>500 张知识卡，直接开刷</span>
        </div>
      </div>
      <nav class="nav">
        <a href="index.html" class="active">手卡</a>
        <a href="quiz.html">自测</a>
      </nav>
    </div>

    <section class="section-head">
      <span class="eyebrow">WHZNB</span>
      <h1>速记手卡</h1>
    </section>

    <div class="tools">
      <select id="chapterFilter"></select>
      <button id="modeAll" class="toggle active" type="button">显示全部</button>
      <button id="modeWeak" class="toggle" type="button">只看未掌握</button>
    </div>

    <div class="progress-card">
      <div class="progress-card-head">
        <strong>当前掌握度</strong>
        <span id="masteryText"></span>
      </div>
      <div class="progress-track">
        <span class="progress-fill" id="masteryBar"></span>
      </div>
    </div>

    <div class="card-stage">
      <button class="nav-float prev" id="prevBtn" type="button" aria-label="上一题">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 18 9 12l6-6"></path></svg>
      </button>
      <button class="nav-float next" id="nextBtn" type="button" aria-label="下一题">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="m9 18 6-6-6-6"></path></svg>
      </button>
      <div class="card-shell">
        <div class="card" id="flashcard">
        <div class="card-main">
          <div class="card-top">
            <span class="pill" id="flashStep">QUESTION 1</span>
            <div class="helper-bar">
              <span class="helper-chip">⌨ 空格翻答案 / ← → 切换</span>
              <button class="mastery-btn" id="masteryBtn" type="button">★</button>
            </div>
          </div>

            <div class="question-wrap">
              <span class="question-index" id="flashChapter">导论</span>
              <h2 id="flashQuestion"></h2>
            </div>

          <p class="question-foot">点击显示答案</p>
          </div>

        <div class="answer-panel" id="answerPanel">
          <div class="answer-panel-inner">
            <span class="answer-label">Answer</span>
            <div class="answer-text" id="flashAnswer"></div>
          </div>
          </div>
        </div>
      </div>
    </div>

    <div class="card-actions">
      <button id="pinAnswerBtn" class="toggle mini-toggle" type="button">保持答案</button>
      <button id="shuffleBtn" type="button">随机重排</button>
      <button id="resetMasteryBtn" type="button">清空掌握记录</button>
    </div>
  </div>

  <script>
    const cards = ${json(cards)};
    const chapters = ${json(chapters)};
    const chapterCounts = ${json(chapterCounts)};
    const storageKeys = {
      mastery: "mayuan_mastery_v7"
    };

    const state = {
      chapter: "all",
      mode: "all",
      currentId: cards[0] ? cards[0].id : null,
      pinAnswer: false,
      showAnswer: false,
      shuffleOrder: cards.map((card) => card.id),
      mastered: readJson(storageKeys.mastery, [])
    };

    const el = {
      chapterFilter: document.getElementById("chapterFilter"),
      modeAll: document.getElementById("modeAll"),
      modeWeak: document.getElementById("modeWeak"),
      pinAnswerBtn: document.getElementById("pinAnswerBtn"),
      flashcard: document.getElementById("flashcard"),
      flashStep: document.getElementById("flashStep"),
      flashChapter: document.getElementById("flashChapter"),
      flashQuestion: document.getElementById("flashQuestion"),
      flashAnswer: document.getElementById("flashAnswer"),
      masteryBtn: document.getElementById("masteryBtn"),
      masteryText: document.getElementById("masteryText"),
      masteryBar: document.getElementById("masteryBar"),
      prevBtn: document.getElementById("prevBtn"),
      nextBtn: document.getElementById("nextBtn"),
      shuffleBtn: document.getElementById("shuffleBtn"),
      resetMasteryBtn: document.getElementById("resetMasteryBtn")
    };
    const swipe = {
      startX: 0,
      startY: 0,
      tracking: false,
      suppressClick: false
    };

    function syncAnswerMode() {
      const keepAnswerVisible = state.pinAnswer || state.showAnswer;
      el.pinAnswerBtn.classList.toggle("active", state.pinAnswer);
      el.pinAnswerBtn.textContent = state.pinAnswer ? "隐藏答案" : "保持答案";
      el.pinAnswerBtn.setAttribute("aria-pressed", state.pinAnswer ? "true" : "false");
      el.flashcard.classList.toggle("show", keepAnswerVisible);
      const foot = document.querySelector(".question-foot");
      if (foot) {
        foot.textContent = state.pinAnswer ? "当前保持显示答案" : "点击显示答案";
      }
    }

    function readJson(key, fallback) {
      try {
        const raw = localStorage.getItem(key);
        return raw ? JSON.parse(raw) : fallback;
      } catch {
        return fallback;
      }
    }

    function saveJson(key, value) {
      localStorage.setItem(key, JSON.stringify(value));
    }

    function filteredCards() {
      let list = cards.slice();
      if (state.chapter !== "all") list = list.filter((card) => card.chapter === state.chapter);
      if (state.mode === "weak") list = list.filter((card) => !state.mastered.includes(card.id));
      return list.sort((a, b) => state.shuffleOrder.indexOf(a.id) - state.shuffleOrder.indexOf(b.id));
    }

    function currentCard(list) {
      if (!list.length) return null;
      const found = list.find((card) => card.id === state.currentId);
      if (found) return found;
      state.currentId = list[0].id;
      return list[0];
    }

    function renderFilter() {
      el.chapterFilter.innerHTML = ['<option value="all">全部章节</option>']
        .concat(chapters.map((chapter) => '<option value="' + chapter + '">' + chapter + '（' + chapterCounts[chapter] + '）</option>'))
        .join("");
      el.chapterFilter.value = state.chapter;
    }

    function renderCards() {
      const list = filteredCards();
      const card = currentCard(list);
      const masteryRate = cards.length ? (state.mastered.length / cards.length) * 100 : 0;

      el.masteryText.textContent = "已掌握 " + state.mastered.length + " / " + cards.length;
      el.masteryBar.style.width = masteryRate + "%";
      el.modeAll.classList.toggle("active", state.mode === "all");
      el.modeWeak.classList.toggle("active", state.mode === "weak");
      syncAnswerMode();

      if (!card) {
        el.flashStep.textContent = "EMPTY";
        el.flashChapter.textContent = "暂无卡片";
        el.flashQuestion.textContent = "当前筛选下没有待复习内容。";
        el.flashAnswer.textContent = "切回“显示全部”或者换个章节继续刷。";
        el.masteryBtn.classList.remove("active");
        syncAnswerMode();
        return;
      }

      const currentIndex = list.findIndex((item) => item.id === card.id) + 1;
      el.flashStep.textContent = "QUESTION " + currentIndex;
      el.flashChapter.textContent = card.chapter;
      el.flashQuestion.textContent = card.question;
      el.flashAnswer.textContent = card.answer;
      el.masteryBtn.classList.toggle("active", state.mastered.includes(card.id));
      syncAnswerMode();
    }

    function moveCard(step) {
      const list = filteredCards();
      if (!list.length) return;
      const index = list.findIndex((card) => card.id === state.currentId);
      const next = (index + step + list.length) % list.length;
      state.currentId = list[next].id;
      state.showAnswer = state.pinAnswer;
      renderCards();
    }

    function toggleMastery() {
      const list = filteredCards();
      const card = currentCard(list);
      if (!card) return;
      if (state.mastered.includes(card.id)) {
        state.mastered = state.mastered.filter((id) => id !== card.id);
      } else {
        state.mastered = state.mastered.concat(card.id);
      }
      saveJson(storageKeys.mastery, state.mastered);
      renderCards();
    }

    function bind() {
      function isInteractiveTarget(target) {
        return Boolean(target.closest("button, select, a, input, textarea, label"));
      }

      el.chapterFilter.addEventListener("change", (event) => {
        state.chapter = event.target.value;
        state.showAnswer = state.pinAnswer;
        renderCards();
      });
      el.modeAll.addEventListener("click", () => {
        state.mode = "all";
        state.showAnswer = state.pinAnswer;
        renderCards();
      });
      el.modeWeak.addEventListener("click", () => {
        state.mode = "weak";
        state.showAnswer = state.pinAnswer;
        renderCards();
      });
      el.pinAnswerBtn.addEventListener("click", (event) => {
        state.pinAnswer = !state.pinAnswer;
        state.showAnswer = state.pinAnswer;
        if (!state.pinAnswer) {
          el.flashcard.classList.remove("show");
        }
        renderCards();
      });
      el.flashcard.addEventListener("click", () => {
        if (swipe.suppressClick) {
          swipe.suppressClick = false;
          return;
        }
        if (state.pinAnswer) return;
        state.showAnswer = !state.showAnswer;
        renderCards();
      });
      el.flashcard.addEventListener("touchstart", (event) => {
        if (event.touches.length !== 1 || isInteractiveTarget(event.target)) {
          swipe.tracking = false;
          return;
        }
        const touch = event.touches[0];
        swipe.startX = touch.clientX;
        swipe.startY = touch.clientY;
        swipe.tracking = true;
      }, { passive: true });
      el.flashcard.addEventListener("touchend", (event) => {
        if (!swipe.tracking || event.changedTouches.length !== 1) return;
        swipe.tracking = false;
        const touch = event.changedTouches[0];
        const deltaX = touch.clientX - swipe.startX;
        const deltaY = touch.clientY - swipe.startY;
        if (Math.abs(deltaX) < 56 || Math.abs(deltaX) < Math.abs(deltaY) * 1.2) {
          return;
        }
        swipe.suppressClick = true;
        moveCard(deltaX < 0 ? 1 : -1);
        setTimeout(() => {
          swipe.suppressClick = false;
        }, 260);
      }, { passive: true });
      el.masteryBtn.addEventListener("click", (event) => {
        event.stopPropagation();
        toggleMastery();
      });
      el.prevBtn.addEventListener("click", () => moveCard(-1));
      el.nextBtn.addEventListener("click", () => moveCard(1));
      el.shuffleBtn.addEventListener("click", () => {
        state.shuffleOrder = cards.map((card) => card.id).sort(() => Math.random() - 0.5);
        state.showAnswer = state.pinAnswer;
        renderCards();
      });
      el.resetMasteryBtn.addEventListener("click", () => {
        state.mastered = [];
        saveJson(storageKeys.mastery, state.mastered);
        renderCards();
      });
      document.addEventListener("keydown", (event) => {
        if (event.code === "Space") {
          event.preventDefault();
          if (state.pinAnswer) return;
          state.showAnswer = !state.showAnswer;
          renderCards();
        } else if (event.code === "ArrowRight") {
          moveCard(1);
        } else if (event.code === "ArrowLeft") {
          moveCard(-1);
        }
      });
    }

    renderFilter();
    renderCards();
    bind();
  </script>
</body>
</html>`;
}

function buildQuizHtml() {
  return `${commonHead("马原即时自测")}
<body>
  <div class="shell">
    <div class="topbar">
      <div class="brand">
        <div class="seal">马原</div>
        <div>
          <strong>马原即时自测</strong>
          <span>独立页面，专门回刺</span>
        </div>
      </div>
      <nav class="nav">
        <a href="index.html">手卡</a>
        <a href="quiz.html" class="active">自测</a>
      </nav>
    </div>

    <section class="section-head">
      <span class="eyebrow">Quick Quiz</span>
      <h1>单独做一轮自测</h1>
      <p>这里不掺手卡，只保留即时自测。做完就能看当前错题，回去再针对性补卡。</p>
    </section>

    <div class="quiz-layout">
      <div class="quiz-card">
        <div class="pill quiz-step" id="quizStep">第 1 题 / 12</div>
        <h2 class="quiz-question" id="quizQuestion"></h2>
        <p class="muted" id="quizChapter"></p>
        <div class="quiz-options" id="quizOptions"></div>
        <div class="quiz-actions">
          <button id="quizPrevBtn" type="button">上一题</button>
          <button id="quizNextBtn" type="button">下一题</button>
        </div>
      </div>

      <div class="result-card">
        <h3>当前成绩</h3>
        <div class="score">
          <strong id="scoreValue">0</strong>
          <span>分</span>
        </div>
        <p class="muted" id="scoreText">先把题做完，再看哪块最薄弱。</p>
        <button id="resetQuizBtn" type="button">重做这一轮</button>
        <div id="mistakeList"></div>
      </div>
    </div>

    <footer>想继续翻卡，点右上角“手卡”返回主页面。</footer>
  </div>

  <script>
    const quizItems = ${json(quizItems)};
    const storageKeys = {
      quiz: "mayuan_quiz_v7"
    };

    const state = {
      quizIndex: 0,
      quizAnswers: readJson(storageKeys.quiz, Array(quizItems.length).fill(null))
    };

    const el = {
      quizStep: document.getElementById("quizStep"),
      quizQuestion: document.getElementById("quizQuestion"),
      quizChapter: document.getElementById("quizChapter"),
      quizOptions: document.getElementById("quizOptions"),
      quizPrevBtn: document.getElementById("quizPrevBtn"),
      quizNextBtn: document.getElementById("quizNextBtn"),
      scoreValue: document.getElementById("scoreValue"),
      scoreText: document.getElementById("scoreText"),
      resetQuizBtn: document.getElementById("resetQuizBtn"),
      mistakeList: document.getElementById("mistakeList")
    };

    function readJson(key, fallback) {
      try {
        const raw = localStorage.getItem(key);
        return raw ? JSON.parse(raw) : fallback;
      } catch {
        return fallback;
      }
    }

    function saveJson(key, value) {
      localStorage.setItem(key, JSON.stringify(value));
    }

    function renderQuiz() {
      const item = quizItems[state.quizIndex];
      if (!item) return;
      el.quizStep.textContent = "第 " + (state.quizIndex + 1) + " 题 / " + quizItems.length;
      el.quizQuestion.textContent = item.question;
      el.quizChapter.textContent = item.chapter;
      el.quizOptions.innerHTML = item.options.map((option, index) => {
        const selected = state.quizAnswers[state.quizIndex] === index ? "selected" : "";
        return '<button type="button" class="' + selected + '" data-index="' + index + '">' + String.fromCharCode(65 + index) + ". " + option + "</button>";
      }).join("");
      Array.from(el.quizOptions.querySelectorAll("button")).forEach((button) => {
        button.addEventListener("click", () => {
          state.quizAnswers[state.quizIndex] = Number(button.dataset.index);
          saveJson(storageKeys.quiz, state.quizAnswers);
          renderQuiz();
          renderResult();
        });
      });
    }

    function renderResult() {
      let correct = 0;
      const mistakes = [];
      quizItems.forEach((item, index) => {
        if (state.quizAnswers[index] === item.answer) {
          correct += 1;
        } else if (state.quizAnswers[index] !== null) {
          mistakes.push(item);
        }
      });
      const score = quizItems.length ? Math.round((correct / quizItems.length) * 100) : 0;
      el.scoreValue.textContent = String(score);
      el.scoreText.textContent = score >= 80
        ? "这一轮已经很能打了，下一步重点回看错题对应的模块。"
        : "先别焦虑，错题越集中，回去补卡越高效。";

      if (!mistakes.length) {
        el.mistakeList.innerHTML = '<div class="mistake"><p class="muted">当前还没有已暴露错题，继续做完整轮看看。</p></div>';
        return;
      }

      el.mistakeList.innerHTML = mistakes.map((item) => {
        return '<div class="mistake"><strong>' + item.question + '</strong><p class="muted">正确答案：' + item.options[item.answer] + '</p><p class="muted">' + item.explain + '</p></div>';
      }).join("");
    }

    function bind() {
      el.quizPrevBtn.addEventListener("click", () => {
        state.quizIndex = Math.max(0, state.quizIndex - 1);
        renderQuiz();
      });
      el.quizNextBtn.addEventListener("click", () => {
        state.quizIndex = Math.min(quizItems.length - 1, state.quizIndex + 1);
        renderQuiz();
      });
      el.resetQuizBtn.addEventListener("click", () => {
        state.quizIndex = 0;
        state.quizAnswers = Array(quizItems.length).fill(null);
        saveJson(storageKeys.quiz, state.quizAnswers);
        renderQuiz();
        renderResult();
      });
    }

    renderQuiz();
    renderResult();
    bind();
  </script>
</body>
</html>`;
}

fs.writeFileSync(indexPath, buildIndexHtml(), "utf8");
fs.writeFileSync(quizPath, buildQuizHtml(), "utf8");

console.log("wrote index.html and quiz.html");
