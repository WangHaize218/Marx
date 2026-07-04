import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CARDS_PATH = ROOT / "mayuan_cards_500.json"
OUTPUT_PATH = ROOT / "index.html"


cards = json.loads(CARDS_PATH.read_text(encoding="utf-8"))
chapter_counts = Counter(card["chapter"] for card in cards)
chapters = [chapter for chapter, _ in chapter_counts.most_common()]

chapter_desc = {
    "\u5bfc\u8bba": "\u5148\u6293\u4f4f\u9a6c\u514b\u601d\u4e3b\u4e49\u662f\u4ec0\u4e48\u3001\u4ece\u54ea\u91cc\u6765\u3001\u4e3a\u4ec0\u4e48\u884c\u3002",
    "\u552f\u7269\u8bba\u4e0e\u54f2\u5b66\u57fa\u672c\u95ee\u9898": "\u91cd\u70b9\u7a33\u4f4f\u7269\u8d28\u7b2c\u4e00\u6027\u3001\u610f\u8bc6\u7b2c\u4e8c\u6027\u3001\u89c4\u5f8b\u4e0e\u80fd\u52a8\u6027\u7684\u7edf\u4e00\u3002",
    "\u552f\u7269\u8fa9\u8bc1\u6cd5": "\u9ad8\u9891\u4e2d\u7684\u9ad8\u9891\uff0c\u6838\u5fc3\u662f\u8054\u7cfb\u3001\u53d1\u5c55\u548c\u77db\u76fe\u5206\u6790\u65b9\u6cd5\u3002",
    "\u4e94\u5bf9\u57fa\u672c\u8303\u7574": "\u9002\u5408\u505a\u6982\u5ff5\u5bf9\u7167\u9898\u548c\u8fa8\u6790\u9898\uff0c\u5bb9\u6613\u5728\u9009\u62e9\u9898\u91cc\u6df7\u3002",
    "\u8ba4\u8bc6\u8bba": "\u5b9e\u8df5\u3001\u8ba4\u8bc6\u3001\u68c0\u9a8c\u6807\u51c6\u8fd9\u6761\u7ebf\u8981\u7279\u522b\u7a33\u3002",
    "\u771f\u7406\u4e0e\u4ef7\u503c": "\u8981\u5206\u6e05\u771f\u7406\u6807\u51c6\u3001\u4ef7\u503c\u8bc4\u4ef7\u3001\u771f\u7406\u7edd\u5bf9\u6027\u548c\u76f8\u5bf9\u6027\u3002",
    "\u552f\u7269\u53f2\u89c2": "\u8981\u6293\u4f4f\u793e\u4f1a\u5b58\u5728\u3001\u793e\u4f1a\u610f\u8bc6\u3001\u793e\u4f1a\u57fa\u672c\u77db\u76fe\u548c\u4eba\u6c11\u7fa4\u4f17\u3002",
    "\u8d44\u672c\u4e3b\u4e49\u672c\u8d28\u53ca\u89c4\u5f8b": "\u5546\u54c1\u3001\u4ef7\u503c\u3001\u5269\u4f59\u4ef7\u503c\u548c\u5371\u673a\u662f\u9009\u62e9\u9898\u5927\u5757\u5934\u3002",
    "\u8d44\u672c\u4e3b\u4e49\u7684\u53d1\u5c55\u53ca\u5176\u8d8b\u52bf": "\u57c4\u65ad\u3001\u91d1\u878d\u8d44\u672c\u3001\u56fd\u5bb6\u57c4\u65ad\u8d44\u672c\u4e3b\u4e49\u548c\u5168\u7403\u5316\u662f\u4e3b\u8f74\u3002",
    "\u793e\u4f1a\u4e3b\u4e49\u4e0e\u5171\u4ea7\u4e3b\u4e49": "\u4ece\u7a7a\u60f3\u5230\u79d1\u5b66\uff0c\u518d\u5230\u793e\u4f1a\u4e3b\u4e49\u53d1\u5c55\u89c4\u5f8b\u548c\u5171\u4ea7\u4e3b\u4e49\u76ee\u6807\u3002",
}

overview = [
    {
        "title": chapter,
        "count": chapter_counts[chapter],
        "desc": chapter_desc.get(chapter, "\u8fd9\u4e2a\u6a21\u5757\u7684\u5361\u7247\u5df2\u63a5\u5165\uff0c\u9002\u5408\u96c6\u4e2d\u6253\u3002"),
    }
    for chapter in chapters
]

quiz = []
for idx, card in enumerate(cards):
    if len(quiz) >= 12:
        break
    same = [item for item in cards if item["chapter"] == card["chapter"] and item["answer"] != card["answer"]]
    other = [item for item in cards if item["chapter"] != card["chapter"] and item["answer"] != card["answer"]]
    distractors = []
    for pool in (same, other):
        for item in pool:
            if item["answer"] not in distractors:
                distractors.append(item["answer"])
            if len(distractors) == 3:
                break
        if len(distractors) == 3:
            break
    if len(distractors) < 3:
        continue
    options = [card["answer"], distractors[0], distractors[1], distractors[2]]
    shift = idx % 4
    options = options[shift:] + options[:shift]
    quiz.append(
        {
            "question": card["question"],
            "chapter": card["chapter"],
            "options": options,
            "answer": options.index(card["answer"]),
            "explain": f"\\u8fd9\\u9898\\u5bf9\\u5e94 {card['chapter']} \\u6a21\\u5757\\uff0c\\u6807\\u51c6\\u8868\\u8ff0\\u8981\\u9501\\u5b9a\\u539f\\u7b54\\u6848\\u3002",
        }
    )

ui = {
    "title": "\u9a6c\u539f\u7a81\u56f4\u6218\u672f\u677f",
    "brand_main": "\u9a6c\u514b\u601d\u4e3b\u4e49\u57fa\u672c\u539f\u7406\u7a81\u56f4\u6218\u672f\u677f",
    "brand_sub": "\u79bb\u7ebf\u53ef\u7528 \u00b7 500 \u5f20\u77e5\u8bc6\u5361 \u00b7 \u7ffb\u5361\u8bb0\u5fc6 \u00b7 \u5373\u65f6\u81ea\u6d4b",
    "nav_overview": "\u603b\u89c8",
    "nav_flashcards": "\u624b\u5361",
    "nav_quiz": "\u81ea\u6d4b",
    "hero_eyebrow": "Reading Room \u00b7 Exam Mode",
    "hero_title": "\u628a\u9a6c\u539f\u7684\u4e94\u767e\u4e2a\u9ad8\u9891\u77e5\u8bc6\u70b9\uff0c\u53d8\u6210\u4e00\u5957\u771f\u80fd\u53cd\u590d\u5237\u7684\u5361\u7ec4\u3002",
    "hero_lead": "\u73b0\u5728\u8fd9\u7248\u5df2\u7ecf\u63a5\u5165\u5b8c\u6574\u9898\u5e93\u3002\u4f60\u53ef\u4ee5\u6309\u7ae0\u8282\u96c6\u4e2d\u6253\uff0c\u4e5f\u53ef\u4ee5\u968f\u673a\u5237\u5361\u3001\u53ea\u770b\u672a\u638c\u63e1\uff0c\u8fd8\u80fd\u987a\u624b\u505a\u4e00\u8f6e\u5373\u65f6\u81ea\u6d4b\u3002",
    "hero_cta_cards": "\u76f4\u63a5\u5f00\u59cb\u7ffb\u5361",
    "hero_cta_quiz": "\u5148\u505a\u4e00\u8f6e\u81ea\u6d4b",
    "metric_cards_label": "\u5f53\u524d\u63a5\u5165\u7684\u77e5\u8bc6\u5361\u603b\u6570\uff0c\u5df2\u7ecf\u8986\u76d6\u6838\u5fc3\u6a21\u5757\u3002",
    "metric_mastery_label": "\u4f60\u5df2\u7ecf\u6807\u8bb0\u4e3a\u638c\u63e1\u7684\u6bd4\u4f8b\uff0c\u6d4f\u89c8\u5668\u4f1a\u81ea\u52a8\u8bb0\u4f4f\u3002",
    "metric_quiz_label": "\u672c\u8f6e\u81ea\u6d4b\u8fdb\u5ea6\uff0c\u505a\u5b8c\u5c31\u80fd\u770b\u9519\u9898\u56de\u523a\u3002",
    "route_title": "\u590d\u4e60\u8def\u7ebf",
    "route_1": "1. \u5148\u6253\u603b\u8bba\u548c\u552f\u7269\u8bba",
    "route_1_tip": "\u7acb\u4f4f\u603b\u6846\u67b6",
    "route_2": "2. \u518d\u6253\u8fa9\u8bc1\u6cd5\u548c\u8ba4\u8bc6\u8bba",
    "route_2_tip": "\u6293\u9ad8\u9891\u65b9\u6cd5\u8bba",
    "route_3": "3. \u63a5\u7740\u552f\u7269\u53f2\u89c2",
    "route_3_tip": "\u7a33\u4f4f\u793e\u4f1a\u53d1\u5c55\u903b\u8f91",
    "route_4": "4. \u6700\u540e\u8d44\u672c\u4e0e\u793e\u4f1a\u4e3b\u4e49",
    "route_4_tip": "\u6e05\u7406\u7ecf\u6d4e\u548c\u5236\u5ea6\u677f\u5757",
    "chapter_count_title": "\u7ae0\u8282\u5361\u91cf",
    "choice_hint_title": "\u9009\u62e9\u9898\u63d0\u9192",
    "choice_hint_body": "\u8fd9\u5957\u5361\u7684\u95ee\u6cd5\u5df2\u7ecf\u5c3d\u91cf\u538b\u6210\u9009\u62e9\u9898\u80cc\u8bf5\u5411\u3002\u5237\u7684\u65f6\u5019\u4e0d\u8981\u53ea\u80cc\u53e5\u5b50\uff0c\u8981\u987a\u624b\u8bb0\u4f4f\u5b83\u5728\u8003\u201c\u5b9a\u4e49\u3001\u5730\u4f4d\u3001\u7279\u5f81\u3001\u5173\u7cfb\u3001\u4f5c\u7528\u201d\u91cc\u7684\u54ea\u4e00\u7c7b\u3002",
    "overview_title": "\u6a21\u5757\u603b\u89c8",
    "overview_body": "\u6309\u7ae0\u8282\u96c6\u4e2d\u5237\uff0c\u6bd4\u4e71\u5e8f\u5543\u66f4\u5feb\u51fa\u6548\u679c\u3002",
    "flashcards_title": "\u77e5\u8bc6\u5361\u7247",
    "flashcards_body": "\u70b9\u51fb\u5361\u7247\u7ffb\u7b54\u6848\uff0c\u6309\u7a7a\u683c\u4e5f\u80fd\u7ffb\u3002\u4f60\u53ef\u4ee5\u6309\u7ae0\u8282\u5207\u3001\u968f\u673a\u5237\u3001\u53ea\u770b\u672a\u638c\u63e1\u3002",
    "filter_all": "\u5168\u90e8\u7ae0\u8282",
    "mode_all": "\u663e\u793a\u5168\u90e8",
    "mode_unmastered": "\u53ea\u770b\u672a\u638c\u63e1",
    "flash_hint": "\u70b9\u51fb\u5361\u7247\u67e5\u770b\u7b54\u6848\uff0c\u6216\u6309\u7a7a\u683c\u7ffb\u9762\u3002",
    "answer_label": "Answer",
    "progress_title": "\u5f53\u524d\u638c\u63e1\u5ea6",
    "source_title": "\u6765\u6e90\u4fe1\u606f",
    "actions_title": "\u5237\u9898\u52a8\u4f5c",
    "actions_body": "\u5148\u81ea\u5df1\u5728\u8111\u5b50\u91cc\u4f5c\u7b54\uff0c\u518d\u7ffb\u9762\u6838\u5bf9\u6807\u51c6\u8868\u8ff0\uff0c\u6700\u540e\u6807\u8bb0\u662f\u5426\u638c\u63e1\u3002",
    "prev": "\u4e0a\u4e00\u9898",
    "next": "\u4e0b\u4e00\u9898",
    "shuffle": "\u968f\u673a\u91cd\u6392",
    "reset_mastery": "\u6e05\u7a7a\u638c\u63e1\u8bb0\u5f55",
    "quiz_title": "\u5373\u65f6\u81ea\u6d4b",
    "quiz_body": "\u8fd9\u91cc\u4e0d\u662f\u6b63\u5f0f\u9898\u5e93\uff0c\u53ea\u662f\u4ece\u77e5\u8bc6\u5361\u91cc\u62bd\u4e86 12 \u9053\u505a\u5feb\u901f\u56de\u523a\u3002",
    "score_suffix": "\u5206",
    "score_default": "\u5148\u628a\u9898\u505a\u5b8c\uff0c\u518d\u770b\u81ea\u5df1\u8584\u5f31\u70b9\u96c6\u4e2d\u5728\u54ea\u4e2a\u6a21\u5757\u3002",
    "reset_quiz": "\u91cd\u505a\u8fd9\u4e00\u8f6e",
    "footer": "\u5f53\u524d\u7248\u672c\u5df2\u5185\u7f6e 500 \u5f20\u77e5\u8bc6\u5361\uff0c\u9002\u5408\u76f4\u63a5\u79bb\u7ebf\u6253\u5f00\u53cd\u590d\u5237\u3002",
    "empty_title": "\u5168\u90e8\u638c\u63e1",
    "empty_question": "\u8fd9\u4e00\u7b5b\u9009\u6761\u4ef6\u4e0b\u5df2\u7ecf\u6ca1\u6709\u5f85\u590d\u4e60\u5185\u5bb9\u4e86\u3002",
    "empty_answer": "\u5207\u56de\u663e\u793a\u5168\u90e8\uff0c\u6216\u8005\u6362\u4e00\u4e2a\u7ae0\u8282\u7ee7\u7eed\u8865\u6d1e\u3002",
    "empty_source": "\u4f60\u53ef\u4ee5\u5f00\u59cb\u505a\u4e0b\u9762\u7684\u81ea\u6d4b\uff0c\u770b\u770b\u662f\u4e0d\u662f\u771f\u7684\u7a33\u4e86\u3002",
    "mistake_none_title": "\u5f53\u524d\u6ca1\u6709\u5df2\u66b4\u9732\u9519\u9898",
    "mistake_none_body": "\u7ee7\u7eed\u505a\u5b8c\u5168\u90e8\u9898\uff0c\u6216\u8005\u56de\u5230\u4e0a\u9762\u7684\u5361\u7247\u533a\u7ee7\u7eed\u5237\u3002",
    "correct_answer": "\u6b63\u786e\u7b54\u6848\uff1a",
    "source_prefix": "\u6765\u6e90\uff1a",
    "mastery_template": "\u4f60\u5df2\u6807\u8bb0 {mastered} / {total} \u5f20\u5361\u4e3a\u5df2\u638c\u63e1\u3002",
    "quiz_step_template": "\u7b2c {current} \u9898 / {total}",
    "flash_step_template": "{current} / {total}",
}

template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Mayuan Board</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #efe7dc;
      --paper: #fbf7f1;
      --ink: #171410;
      --muted: #6c665d;
      --line: rgba(23, 20, 16, 0.12);
      --soft-line: rgba(255, 255, 255, 0.62);
      --accent: #bb431d;
      --accent-deep: #8e2e14;
      --accent-soft: rgba(187, 67, 29, 0.12);
      --forest: #2f5c49;
      --shadow: 0 24px 60px rgba(70, 46, 26, 0.14);
      --shadow-soft: 0 12px 30px rgba(70, 46, 26, 0.08);
      --radius: 24px;
      --max: 1240px;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans SC", sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top right, rgba(187, 67, 29, 0.18), transparent 28%),
        radial-gradient(circle at 10% 20%, rgba(47, 92, 73, 0.12), transparent 24%),
        linear-gradient(180deg, #f3ece3 0%, #eee5db 100%);
    }}
    a {{ color: inherit; text-decoration: none; }}
    button, select {{ font: inherit; }}
    .shell {{ width: min(var(--max), calc(100% - 24px)); margin: 16px auto 40px; }}
    .topbar {{
      position: sticky; top: 10px; z-index: 20; display: flex; justify-content: space-between;
      align-items: center; gap: 16px; padding: 12px 16px; border-radius: 999px;
      border: 1px solid var(--soft-line); background: rgba(251, 247, 241, 0.82);
      backdrop-filter: blur(18px); box-shadow: var(--shadow-soft);
    }}
    .brand {{ display: flex; align-items: center; gap: 12px; min-width: 0; }}
    .seal {{
      width: 44px; height: 44px; border-radius: 50%; display: grid; place-items: center;
      color: #fff8f0; font-weight: 800;
      background: radial-gradient(circle at 30% 30%, #d86a49, #b43418 72%);
      box-shadow: inset 0 1px 0 rgba(255,255,255,0.35);
    }}
    .brand strong, .brand span {{
      display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }}
    .brand strong {{ font-size: 14px; letter-spacing: 0.12em; }}
    .brand span {{ color: var(--muted); font-size: 12px; }}
    .nav {{ display: flex; gap: 8px; flex-wrap: wrap; justify-content: flex-end; }}
    .nav a {{ padding: 10px 14px; border-radius: 999px; color: var(--muted); }}
    .nav a:hover {{ background: rgba(23, 20, 16, 0.06); color: var(--ink); }}
    .hero {{ display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 20px; padding: 28px 0 18px; min-height: calc(100dvh - 120px); }}
    .panel, .section-card, .flashcard, .sidebar-card, .quiz-card, .result-card {{
      border-radius: var(--radius); border: 1px solid var(--soft-line);
      background: rgba(251, 247, 241, 0.9); box-shadow: var(--shadow);
    }}
    .panel {{
      position: relative; overflow: hidden; padding: 34px;
      background: linear-gradient(135deg, rgba(251,247,241,0.95), rgba(246,238,228,0.88)), var(--paper);
    }}
    .panel::before {{
      content: ""; position: absolute; width: 300px; height: 300px; right: -120px; top: -120px;
      border-radius: 50%; background: radial-gradient(circle, rgba(187,67,29,0.18), transparent 68%);
    }}
    .eyebrow {{
      display: inline-flex; align-items: center; gap: 8px; padding: 10px 14px; border-radius: 999px;
      background: rgba(23, 20, 16, 0.05); color: var(--muted); font-size: 13px; letter-spacing: 0.08em; text-transform: uppercase;
    }}
    .hero h1 {{ margin: 18px 0 14px; max-width: 11ch; font-size: clamp(40px, 7vw, 74px); line-height: 0.96; letter-spacing: -0.05em; }}
    .lead {{ margin: 0; max-width: 34ch; font-size: 18px; line-height: 1.7; color: rgba(23,20,16,0.78); }}
    .hero-actions, .flash-actions {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 22px; }}
    .btn {{ border: none; border-radius: 999px; padding: 14px 18px; cursor: pointer; transition: transform 0.18s ease, background 0.18s ease; }}
    .btn:active {{ transform: scale(0.98); }}
    .btn-primary {{ background: var(--accent); color: #fff9f2; box-shadow: 0 14px 30px rgba(187, 67, 29, 0.22); }}
    .btn-primary:hover {{ background: var(--accent-deep); transform: translateY(-1px); }}
    .btn-ghost {{ background: rgba(23, 20, 16, 0.05); color: var(--ink); }}
    .btn-ghost:hover {{ background: rgba(23, 20, 16, 0.09); transform: translateY(-1px); }}
    .hero-metrics {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 28px; }}
    .metric {{ padding: 16px; border-radius: 18px; background: rgba(255,255,255,0.62); border: 1px solid rgba(23,20,16,0.06); }}
    .metric strong {{ display: block; font-size: 30px; margin-bottom: 6px; letter-spacing: -0.04em; }}
    .metric span {{ color: var(--muted); font-size: 13px; line-height: 1.5; }}
    .hero-aside {{ display: grid; gap: 16px; padding: 20px; color: #eff4ef; border-radius: var(--radius); background: linear-gradient(180deg, rgba(26,31,27,0.94), rgba(39,48,41,0.94)); box-shadow: var(--shadow); }}
    .aside-card {{ padding: 18px; border-radius: 18px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.08); }}
    .aside-card h2, .aside-card h3 {{ margin: 0 0 10px; font-size: 18px; }}
    .aside-card p, .aside-card li {{ margin: 0; font-size: 14px; line-height: 1.7; color: rgba(239,244,239,0.78); }}
    .chapter-list, .road-list, .quiz-options {{ list-style: none; padding: 0; margin: 0; display: grid; gap: 10px; }}
    .chapter-list li, .road-list li {{ display: flex; justify-content: space-between; gap: 10px; padding: 12px 14px; border-radius: 14px; background: rgba(255,255,255,0.05); }}
    section {{ padding-top: 18px; }}
    .section-head {{ margin-bottom: 16px; }}
    .section-head h2 {{ margin: 0 0 8px; font-size: clamp(28px, 4vw, 42px); letter-spacing: -0.04em; }}
    .section-head p {{ margin: 0; max-width: 52ch; color: var(--muted); line-height: 1.7; }}
    .section-card {{ padding: 22px; }}
    .overview-grid {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; }}
    .overview-item {{ min-height: 210px; padding: 20px; border-radius: 20px; background: rgba(255,255,255,0.62); border: 1px solid rgba(23,20,16,0.08); display: flex; flex-direction: column; justify-content: space-between; }}
    .overview-tag {{ align-self: flex-start; padding: 8px 12px; border-radius: 999px; background: var(--accent-soft); color: var(--accent-deep); font-size: 12px; }}
    .overview-item strong {{ font-size: 17px; }}
    .overview-item p {{ margin: 8px 0 0; font-size: 14px; line-height: 1.7; color: var(--muted); }}
    .tools {{ display: grid; grid-template-columns: 1.2fr 1fr 1fr; gap: 10px; margin-bottom: 18px; }}
    .field, .pill {{ border-radius: 999px; border: 1px solid var(--line); background: rgba(255,255,255,0.82); padding: 12px 14px; color: var(--ink); }}
    .pill {{ cursor: pointer; text-align: center; }}
    .pill.active {{ background: var(--accent-soft); border-color: rgba(187,67,29,0.24); color: var(--accent-deep); }}
    .flash-layout {{ display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 18px; }}
    .flashcard {{ position: relative; min-height: 500px; overflow: hidden; cursor: pointer; background: linear-gradient(180deg, rgba(255,255,255,0.9), rgba(249,241,233,0.94)); }}
    .flashcard-inner {{ position: relative; min-height: 500px; padding: 28px; }}
    .flash-front {{ min-height: 440px; display: flex; flex-direction: column; justify-content: space-between; transition: opacity 0.26s ease, transform 0.26s ease; }}
    .flash-back {{ position: absolute; left: 0; right: 0; bottom: 0; min-height: 230px; padding: 22px 28px 28px; background: linear-gradient(180deg, rgba(187,67,29,0.98), rgba(142,46,20,0.98)); color: #fff9f2; transform: translateY(100%); opacity: 0; transition: opacity 0.26s ease, transform 0.26s ease; }}
    .flashcard.show .flash-back {{ transform: translateY(0); opacity: 1; }}
    .flashcard.show .flash-front {{ opacity: 0.18; transform: translateY(-10px); }}
    .flash-top {{ display: flex; align-items: flex-start; justify-content: space-between; gap: 14px; }}
    .flash-no {{ display: inline-flex; align-items: center; gap: 8px; padding: 10px 12px; border-radius: 999px; background: rgba(23,20,16,0.05); color: var(--muted); font-size: 13px; }}
    .mastery-btn {{ width: 46px; height: 46px; border: none; border-radius: 50%; background: rgba(47,92,73,0.12); color: var(--forest); cursor: pointer; }}
    .mastery-btn.active {{ background: var(--forest); color: #eef5ef; }}
    .flash-front h3 {{ margin: 24px 0 12px; font-size: clamp(30px, 4vw, 44px); line-height: 1.18; letter-spacing: -0.04em; max-width: 12ch; }}
    .flash-back strong {{ display: block; margin-bottom: 10px; font-size: 14px; color: rgba(255,249,242,0.74); letter-spacing: 0.1em; text-transform: uppercase; }}
    .flash-front p, .flash-back p, .sidebar-card p, .result-card p {{ margin: 0; line-height: 1.7; }}
    .flash-hint {{ color: var(--muted); font-size: 14px; }}
    .flash-side {{ display: grid; gap: 16px; }}
    .sidebar-card {{ padding: 18px; border-radius: 18px; background: rgba(255,255,255,0.72); border: 1px solid rgba(23,20,16,0.08); }}
    .sidebar-card h3 {{ margin: 0 0 8px; font-size: 18px; }}
    .sidebar-card p {{ color: var(--muted); font-size: 14px; }}
    .progress-track {{ width: 100%; height: 10px; margin-top: 14px; border-radius: 999px; background: rgba(23,20,16,0.08); overflow: hidden; }}
    .progress-fill {{ height: 100%; width: 0; border-radius: 999px; background: linear-gradient(90deg, var(--forest), #4c7865); transition: width 0.3s ease; }}
    .quiz-layout {{ display: grid; grid-template-columns: 1.05fr 0.95fr; gap: 18px; }}
    .quiz-card, .result-card {{ padding: 24px; }}
    .quiz-meta {{ display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 18px; }}
    .quiz-card h3 {{ margin: 0 0 14px; font-size: clamp(28px, 4vw, 40px); line-height: 1.18; letter-spacing: -0.04em; }}
    .quiz-options button {{ width: 100%; text-align: left; padding: 16px 18px; border-radius: 18px; border: 1px solid rgba(23,20,16,0.1); background: rgba(255,255,255,0.78); cursor: pointer; }}
    .quiz-options button.selected {{ background: var(--accent-soft); border-color: rgba(187,67,29,0.3); }}
    .result-score {{ display: flex; align-items: flex-end; gap: 10px; margin-bottom: 12px; }}
    .result-score strong {{ font-size: 56px; line-height: 1; letter-spacing: -0.06em; color: var(--accent-deep); }}
    .mistake-list {{ display: grid; gap: 10px; margin-top: 18px; }}
    .mistake-item {{ padding: 14px; border-radius: 16px; background: rgba(187,67,29,0.06); border: 1px solid rgba(187,67,29,0.1); }}
    .mistake-item strong {{ display: block; margin-bottom: 6px; font-size: 15px; }}
    .footer {{ padding: 26px 10px 12px; text-align: center; color: var(--muted); font-size: 13px; }}
    @media (max-width: 1024px) {{
      .hero, .overview-grid, .flash-layout, .quiz-layout {{ grid-template-columns: 1fr; }}
      .hero {{ min-height: auto; }}
      .tools {{ grid-template-columns: 1fr; }}
    }}
    @media (max-width: 720px) {{
      .shell {{ width: min(var(--max), calc(100% - 16px)); }}
      .topbar {{ border-radius: 22px; padding: 12px; flex-direction: column; align-items: stretch; }}
      .nav {{ justify-content: flex-start; }}
      .panel, .hero-aside, .section-card, .quiz-card, .result-card {{ padding: 18px; }}
      .hero-metrics {{ grid-template-columns: 1fr; }}
      .flashcard, .flashcard-inner {{ min-height: 460px; }}
    }}
  </style>
</head>
<body>
  <div class="shell">
    <header class="topbar">
      <div class="brand">
        <div class="seal" id="seal-text"></div>
        <div>
          <strong id="brand-main"></strong>
          <span id="brand-sub"></span>
        </div>
      </div>
      <nav class="nav">
        <a href="#overview" id="nav-overview"></a>
        <a href="#flashcards" id="nav-flashcards"></a>
        <a href="#quiz" id="nav-quiz"></a>
      </nav>
    </header>

    <main>
      <section class="hero">
        <article class="panel">
          <div class="eyebrow" id="hero-eyebrow"></div>
          <h1 id="hero-title"></h1>
          <p class="lead" id="hero-lead"></p>
          <div class="hero-actions">
            <a class="btn btn-primary" href="#flashcards" id="hero-cta-cards"></a>
            <a class="btn btn-ghost" href="#quiz" id="hero-cta-quiz"></a>
          </div>
          <div class="hero-metrics">
            <div class="metric">
              <strong id="metricCards"></strong>
              <span id="metric-cards-label"></span>
            </div>
            <div class="metric">
              <strong id="metricMastery"></strong>
              <span id="metric-mastery-label"></span>
            </div>
            <div class="metric">
              <strong id="metricQuiz"></strong>
              <span id="metric-quiz-label"></span>
            </div>
          </div>
        </article>

        <aside class="hero-aside">
          <div class="aside-card">
            <h2 id="route-title"></h2>
            <ul class="road-list">
              <li><span id="route-1"></span><span id="route-1-tip"></span></li>
              <li><span id="route-2"></span><span id="route-2-tip"></span></li>
              <li><span id="route-3"></span><span id="route-3-tip"></span></li>
              <li><span id="route-4"></span><span id="route-4-tip"></span></li>
            </ul>
          </div>
          <div class="aside-card">
            <h3 id="chapter-count-title"></h3>
            <ul class="chapter-list" id="chapterSummary"></ul>
          </div>
          <div class="aside-card">
            <h3 id="choice-hint-title"></h3>
            <p id="choice-hint-body"></p>
          </div>
        </aside>
      </section>

      <section id="overview">
        <div class="section-head">
          <h2 id="overview-title"></h2>
          <p id="overview-body"></p>
        </div>
        <div class="section-card">
          <div class="overview-grid" id="overviewGrid"></div>
        </div>
      </section>

      <section id="flashcards">
        <div class="section-head">
          <h2 id="flashcards-title"></h2>
          <p id="flashcards-body"></p>
        </div>
        <div class="section-card">
          <div class="tools">
            <select class="field" id="chapterFilter"></select>
            <button class="pill active" id="modeAll"></button>
            <button class="pill" id="modeUnmastered"></button>
          </div>
          <div class="flash-layout">
            <article class="flashcard" id="flashcard">
              <div class="flashcard-inner">
                <div class="flash-front">
                  <div class="flash-top">
                    <div class="flash-no" id="flashNo"></div>
                    <button class="mastery-btn" id="masteryBtn" type="button">✓</button>
                  </div>
                  <div>
                    <span class="eyebrow" id="flashChapter"></span>
                    <h3 id="flashQuestion"></h3>
                  </div>
                  <p class="flash-hint" id="flash-hint"></p>
                </div>
                <div class="flash-back">
                  <strong id="answer-label"></strong>
                  <p id="flashAnswer"></p>
                </div>
              </div>
            </article>

            <aside class="flash-side">
              <div class="sidebar-card">
                <h3 id="progress-title"></h3>
                <p id="progressText"></p>
                <div class="progress-track">
                  <div class="progress-fill" id="progressFill"></div>
                </div>
              </div>
              <div class="sidebar-card">
                <h3 id="source-title"></h3>
                <p id="sourceText"></p>
              </div>
              <div class="sidebar-card">
                <h3 id="actions-title"></h3>
                <p id="actions-body"></p>
                <div class="flash-actions">
                  <button class="btn btn-ghost" id="prevBtn" type="button"></button>
                  <button class="btn btn-primary" id="nextBtn" type="button"></button>
                  <button class="btn btn-ghost" id="shuffleBtn" type="button"></button>
                  <button class="btn btn-ghost" id="resetBtn" type="button"></button>
                </div>
              </div>
            </aside>
          </div>
        </div>
      </section>

      <section id="quiz">
        <div class="section-head">
          <h2 id="quiz-title"></h2>
          <p id="quiz-body"></p>
        </div>
        <div class="section-card">
          <div class="quiz-layout">
            <article class="quiz-card">
              <div class="quiz-meta">
                <strong id="quizStep"></strong>
                <span class="flash-no" id="quizChapter"></span>
              </div>
              <h3 id="quizQuestion"></h3>
              <div class="quiz-options" id="quizOptions"></div>
              <div class="flash-actions">
                <button class="btn btn-ghost" id="quizPrevBtn" type="button"></button>
                <button class="btn btn-primary" id="quizNextBtn" type="button"></button>
              </div>
            </article>
            <aside class="result-card">
              <div class="result-score">
                <strong id="scoreValue"></strong>
                <span id="score-suffix"></span>
              </div>
              <p id="scoreText"></p>
              <div class="mistake-list" id="mistakeList"></div>
              <div class="flash-actions">
                <button class="btn btn-ghost" id="resetQuizBtn" type="button"></button>
              </div>
            </aside>
          </div>
        </div>
      </section>
    </main>

    <footer class="footer" id="footer-text"></footer>
  </div>

  <script>
    "use strict";
    const ui = {ui_json};
    const cards = {cards_json};
    const chapters = {chapters_json};
    const chapterCounts = {chapter_counts_json};
    const overviewCards = {overview_json};
    const quizItems = {quiz_json};

    const STORAGE_KEYS = {{
      mastery: "mayuan_mastery_v3",
      quiz: "mayuan_quiz_v3"
    }};

    const state = {{
      chapter: "all",
      mode: "all",
      currentId: cards[0].id,
      showAnswer: false,
      shuffleOrder: cards.map(card => card.id),
      mastered: loadJson(STORAGE_KEYS.mastery, []),
      quizIndex: 0,
      quizAnswers: loadJson(STORAGE_KEYS.quiz, Array(quizItems.length).fill(null))
    }};

    const el = {{
      metricCards: document.getElementById("metricCards"),
      metricMastery: document.getElementById("metricMastery"),
      metricQuiz: document.getElementById("metricQuiz"),
      chapterSummary: document.getElementById("chapterSummary"),
      overviewGrid: document.getElementById("overviewGrid"),
      chapterFilter: document.getElementById("chapterFilter"),
      modeAll: document.getElementById("modeAll"),
      modeUnmastered: document.getElementById("modeUnmastered"),
      flashcard: document.getElementById("flashcard"),
      flashNo: document.getElementById("flashNo"),
      flashChapter: document.getElementById("flashChapter"),
      flashQuestion: document.getElementById("flashQuestion"),
      flashAnswer: document.getElementById("flashAnswer"),
      masteryBtn: document.getElementById("masteryBtn"),
      progressText: document.getElementById("progressText"),
      progressFill: document.getElementById("progressFill"),
      sourceText: document.getElementById("sourceText"),
      prevBtn: document.getElementById("prevBtn"),
      nextBtn: document.getElementById("nextBtn"),
      shuffleBtn: document.getElementById("shuffleBtn"),
      resetBtn: document.getElementById("resetBtn"),
      quizStep: document.getElementById("quizStep"),
      quizChapter: document.getElementById("quizChapter"),
      quizQuestion: document.getElementById("quizQuestion"),
      quizOptions: document.getElementById("quizOptions"),
      quizPrevBtn: document.getElementById("quizPrevBtn"),
      quizNextBtn: document.getElementById("quizNextBtn"),
      scoreValue: document.getElementById("scoreValue"),
      scoreText: document.getElementById("scoreText"),
      mistakeList: document.getElementById("mistakeList"),
      resetQuizBtn: document.getElementById("resetQuizBtn")
    }};

    function text(id, value) {{
      const node = document.getElementById(id);
      if (node) node.textContent = value;
    }}

    function loadJson(key, fallback) {{
      try {{
        const raw = localStorage.getItem(key);
        return raw ? JSON.parse(raw) : fallback;
      }} catch (error) {{
        return fallback;
      }}
    }}

    function saveJson(key, value) {{
      localStorage.setItem(key, JSON.stringify(value));
    }}

    function applyUi() {{
      document.title = ui.title;
      text("seal-text", "\\u9a6c\\u539f");
      text("brand-main", ui.brand_main);
      text("brand-sub", ui.brand_sub);
      text("nav-overview", ui.nav_overview);
      text("nav-flashcards", ui.nav_flashcards);
      text("nav-quiz", ui.nav_quiz);
      text("hero-eyebrow", ui.hero_eyebrow);
      text("hero-title", ui.hero_title);
      text("hero-lead", ui.hero_lead);
      text("hero-cta-cards", ui.hero_cta_cards);
      text("hero-cta-quiz", ui.hero_cta_quiz);
      text("metric-cards-label", ui.metric_cards_label);
      text("metric-mastery-label", ui.metric_mastery_label);
      text("metric-quiz-label", ui.metric_quiz_label);
      text("route-title", ui.route_title);
      text("route-1", ui.route_1);
      text("route-1-tip", ui.route_1_tip);
      text("route-2", ui.route_2);
      text("route-2-tip", ui.route_2_tip);
      text("route-3", ui.route_3);
      text("route-3-tip", ui.route_3_tip);
      text("route-4", ui.route_4);
      text("route-4-tip", ui.route_4_tip);
      text("chapter-count-title", ui.chapter_count_title);
      text("choice-hint-title", ui.choice_hint_title);
      text("choice-hint-body", ui.choice_hint_body);
      text("overview-title", ui.overview_title);
      text("overview-body", ui.overview_body);
      text("flashcards-title", ui.flashcards_title);
      text("flashcards-body", ui.flashcards_body);
      text("modeAll", ui.mode_all);
      text("modeUnmastered", ui.mode_unmastered);
      text("flash-hint", ui.flash_hint);
      text("answer-label", ui.answer_label);
      text("progress-title", ui.progress_title);
      text("source-title", ui.source_title);
      text("actions-title", ui.actions_title);
      text("actions-body", ui.actions_body);
      text("prevBtn", ui.prev);
      text("nextBtn", ui.next);
      text("shuffleBtn", ui.shuffle);
      text("resetBtn", ui.reset_mastery);
      text("quiz-title", ui.quiz_title);
      text("quiz-body", ui.quiz_body);
      text("quizPrevBtn", ui.prev);
      text("quizNextBtn", ui.next);
      text("score-suffix", ui.score_suffix);
      text("scoreText", ui.score_default);
      text("resetQuizBtn", ui.reset_quiz);
      text("footer-text", ui.footer);
    }}

    function getFilteredCards() {{
      let filtered = cards.slice();
      if (state.chapter !== "all") filtered = filtered.filter(card => card.chapter === state.chapter);
      if (state.mode === "unmastered") filtered = filtered.filter(card => !state.mastered.includes(card.id));
      filtered.sort((a, b) => state.shuffleOrder.indexOf(a.id) - state.shuffleOrder.indexOf(b.id));
      return filtered;
    }}

    function getCurrentCard(filtered) {{
      if (!filtered.length) return null;
      const found = filtered.find(card => card.id === state.currentId);
      if (found) return found;
      state.currentId = filtered[0].id;
      return filtered[0];
    }}

    function formatTemplate(template, data) {{
      return template.replace(/\\{{(.*?)\\}}/g, (_, key) => String(data[key.trim()] ?? ""));
    }}

    function renderSummary() {{
      el.chapterSummary.innerHTML = chapters.map(chapter => {{
        return `<li><span>${{chapter}}</span><span>${{chapter_counts[chapter]}} 张卡</span></li>`;
      }}).join("");
      el.metricCards.textContent = String(cards.length);
    }}

    function renderOverview() {{
      el.overviewGrid.innerHTML = overviewCards.map((item, index) => {{
        return `
          <article class="overview-item">
            <span class="overview-tag">${{String(index + 1).padStart(2, "0")}}</span>
            <div>
              <strong>${{item.title}}</strong>
              <p>${{item.desc}}</p>
            </div>
            <p>当前已接入 ${{item.count}} 张知识卡。</p>
          </article>
        `;
      }}).join("");
    }}

    function renderFilter() {{
      const items = ["all", ...chapters];
      el.chapterFilter.innerHTML = items.map(chapter => {{
        const label = chapter === "all" ? ui.filter_all : chapter;
        return `<option value="${{chapter}}">${{label}}</option>`;
      }}).join("");
      el.chapterFilter.value = state.chapter;
    }}

    function renderCards() {{
      const filtered = getFilteredCards();
      const current = getCurrentCard(filtered);
      const mastery = cards.length ? Math.round(state.mastered.length / cards.length * 100) : 0;
      el.metricMastery.textContent = mastery + "%";
      el.progressText.textContent = formatTemplate(ui.mastery_template, {{
        mastered: state.mastered.length,
        total: cards.length
      }});
      el.progressFill.style.width = mastery + "%";
      el.modeAll.classList.toggle("active", state.mode === "all");
      el.modeUnmastered.classList.toggle("active", state.mode === "unmastered");

      if (!current) {{
        el.flashNo.textContent = ui.empty_title;
        el.flashChapter.textContent = ui.empty_title;
        el.flashQuestion.textContent = ui.empty_question;
        el.flashAnswer.textContent = ui.empty_answer;
        el.sourceText.textContent = ui.empty_source;
        el.flashcard.classList.remove("show");
        el.masteryBtn.classList.remove("active");
        return;
      }}

      const currentIndex = filtered.findIndex(card => card.id === current.id) + 1;
      el.flashNo.textContent = formatTemplate(ui.flash_step_template, {{
        current: currentIndex,
        total: filtered.length
      }});
      el.flashChapter.textContent = current.chapter;
      el.flashQuestion.textContent = current.question;
      el.flashAnswer.textContent = current.answer;
      el.sourceText.textContent = ui.source_prefix + current.source_pdf;
      el.masteryBtn.classList.toggle("active", state.mastered.includes(current.id));
      el.flashcard.classList.toggle("show", state.showAnswer);
    }}

    function moveCard(step) {{
      const filtered = getFilteredCards();
      if (!filtered.length) return;
      const index = filtered.findIndex(card => card.id === state.currentId);
      const next = (index + step + filtered.length) % filtered.length;
      state.currentId = filtered[next].id;
      state.showAnswer = false;
      renderCards();
    }}

    function toggleMastery() {{
      const filtered = getFilteredCards();
      const current = getCurrentCard(filtered);
      if (!current) return;
      if (state.mastered.includes(current.id)) {{
        state.mastered = state.mastered.filter(id => id !== current.id);
      }} else {{
        state.mastered = state.mastered.concat(current.id);
      }}
      saveJson(STORAGE_KEYS.mastery, state.mastered);
      renderCards();
    }}

    function renderQuiz() {{
      const item = quizItems[state.quizIndex];
      el.quizStep.textContent = formatTemplate(ui.quiz_step_template, {{
        current: state.quizIndex + 1,
        total: quizItems.length
      }});
      el.quizChapter.textContent = item.chapter;
      el.quizQuestion.textContent = item.question;
      el.quizOptions.innerHTML = item.options.map((option, index) => {{
        const selected = state.quizAnswers[state.quizIndex] === index ? "selected" : "";
        return `<button type="button" class="${{selected}}" data-index="${{index}}">${{String.fromCharCode(65 + index)}}. ${{option}}</button>`;
      }}).join("");
      Array.from(el.quizOptions.querySelectorAll("button")).forEach(button => {{
        button.addEventListener("click", () => {{
          state.quizAnswers[state.quizIndex] = Number(button.dataset.index);
          saveJson(STORAGE_KEYS.quiz, state.quizAnswers);
          renderQuiz();
          renderQuizResult();
        }});
      }});
      el.metricQuiz.textContent = state.quizAnswers.filter(value => value !== null).length + "/" + quizItems.length;
    }}

    function renderQuizResult() {{
      let correct = 0;
      const mistakes = [];
      quizItems.forEach((item, index) => {{
        if (state.quizAnswers[index] === item.answer) {{
          correct += 1;
        }} else if (state.quizAnswers[index] !== null) {{
          mistakes.push(item);
        }}
      }});
      const score = Math.round(correct / quizItems.length * 100);
      el.scoreValue.textContent = String(score);
      el.scoreText.textContent = score >= 80
        ? "\\u8fd9\\u4e00\\u8f6e\\u5df2\\u7ecf\\u5f88\\u80fd\\u6253\\u4e86\\uff0c\\u4e0b\\u4e00\\u6b65\\u91cd\\u70b9\\u56de\\u770b\\u9519\\u9898\\u6240\\u5728\\u6a21\\u5757\\u3002"
        : "\\u5206\\u6570\\u5148\\u522b\\u7126\\u8651\\uff0c\\u9519\\u9898\\u96c6\\u4e2d\\u53cd\\u800c\\u8bf4\\u660e\\u540e\\u9762\\u8865\\u8d77\\u6765\\u4f1a\\u66f4\\u5feb\\u3002";

      if (!mistakes.length) {{
        el.mistakeList.innerHTML = `
          <div class="mistake-item">
            <strong>${{ui.mistake_none_title}}</strong>
            <span>${{ui.mistake_none_body}}</span>
          </div>
        `;
        return;
      }}

      el.mistakeList.innerHTML = mistakes.map(item => {{
        return `
          <article class="mistake-item">
            <strong>${{item.question}}</strong>
            <span>${{ui.correct_answer}}${{item.options[item.answer]}}</span><br />
            <span>${{item.explain}}</span>
          </article>
        `;
      }}).join("");
    }}

    function bindEvents() {{
      el.chapterFilter.addEventListener("change", event => {{
        state.chapter = event.target.value;
        state.showAnswer = false;
        renderCards();
      }});
      el.modeAll.addEventListener("click", () => {{
        state.mode = "all";
        state.showAnswer = false;
        renderCards();
      }});
      el.modeUnmastered.addEventListener("click", () => {{
        state.mode = "unmastered";
        state.showAnswer = false;
        renderCards();
      }});
      el.flashcard.addEventListener("click", () => {{
        state.showAnswer = !state.showAnswer;
        renderCards();
      }});
      el.masteryBtn.addEventListener("click", event => {{
        event.stopPropagation();
        toggleMastery();
      }});
      el.prevBtn.addEventListener("click", () => moveCard(-1));
      el.nextBtn.addEventListener("click", () => moveCard(1));
      el.shuffleBtn.addEventListener("click", () => {{
        state.shuffleOrder = cards.map(card => card.id).sort(() => Math.random() - 0.5);
        state.showAnswer = false;
        renderCards();
      }});
      el.resetBtn.addEventListener("click", () => {{
        state.mastered = [];
        saveJson(STORAGE_KEYS.mastery, state.mastered);
        renderCards();
      }});
      el.quizPrevBtn.addEventListener("click", () => {{
        state.quizIndex = Math.max(0, state.quizIndex - 1);
        renderQuiz();
      }});
      el.quizNextBtn.addEventListener("click", () => {{
        state.quizIndex = Math.min(quizItems.length - 1, state.quizIndex + 1);
        renderQuiz();
      }});
      el.resetQuizBtn.addEventListener("click", () => {{
        state.quizIndex = 0;
        state.quizAnswers = Array(quizItems.length).fill(null);
        saveJson(STORAGE_KEYS.quiz, state.quizAnswers);
        renderQuiz();
        renderQuizResult();
      }});
      document.addEventListener("keydown", event => {{
        if (event.code === "Space") {{
          event.preventDefault();
          state.showAnswer = !state.showAnswer;
          renderCards();
        }} else if (event.code === "ArrowRight") {{
          moveCard(1);
        }} else if (event.code === "ArrowLeft") {{
          moveCard(-1);
        }}
      }});
    }}

    function init() {{
      applyUi();
      renderSummary();
      renderOverview();
      renderFilter();
      renderCards();
      renderQuiz();
      renderQuizResult();
      bindEvents();
    }}

    init();
  </script>
</body>
</html>
"""

html = template.format(
    ui_json=json.dumps(ui, ensure_ascii=True),
    cards_json=json.dumps(cards, ensure_ascii=True),
    overview_json=json.dumps(overview, ensure_ascii=True),
    quiz_json=json.dumps(quiz, ensure_ascii=True),
)

OUTPUT_PATH.write_text(html, encoding="utf-8")
print(f"wrote {OUTPUT_PATH.name} with {len(cards)} cards")
