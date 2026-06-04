"""
暑假共学背单词系统 – 生成 83 天完整学习计划
================================================

输入: 6 份词表 CSV（样章 + 5 批次）
输出: plan-完整计划.csv + plan-完整计划.md

设计:
- 5+1+1 节奏: 5 天新词 + 1 天复习 + 1 天休息
- 每天 25 词（统一强度）
- 1460 词 ÷ 25 = 58.4 → 11 完整周期 (1375 词, 77 天) + 1 短周期 (85 词, 6 天) = 83 天
- Day 1 = 周一, 复习日 = 周六, 休息日 = 周日
- 修复批次 4 中 2 处"城市与礼仪"误标 → 归回"城市与建筑"
"""

import csv
import os
from collections import defaultdict

# === 配置 ===
WORKSPACE = os.path.dirname(os.path.abspath(__file__))
WORDS_PER_DAY = 25
VOCAB_FILES = [
    '样章/vocab-样章-100词.csv',
    'vocab-批次1-动作形容词情感.csv',
    'vocab-批次2-旅行衣物动物-clean.csv',
    'vocab-批次3-职业身体数字食物扩展.csv',
    'vocab-批次4-社交城市天气语言.csv',
    'vocab-批次5-科技体育娱乐抽象自然地理.csv',
]
WEEKDAYS = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']


# === Step 1: 读取所有单词，修复主题误标 ===
all_words = []  # [(theme, word, meaning, phrase), ...]
for fname in VOCAB_FILES:
    path = os.path.join(WORKSPACE, fname)
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # 跳过表头
        for row in reader:
            if len(row) < 4:
                continue
            theme, word, meaning, phrase = row[0], row[1], row[2], row[3]
            # 修复批次 4 的主题误标: 城市与礼仪 (2 词) → 城市与建筑
            if theme == '城市与礼仪':
                theme = '城市与建筑'
            all_words.append((theme, word, meaning, phrase))

print(f'读取完成: 共 {len(all_words)} 词')

# 统计各主题词数
theme_count = defaultdict(int)
for theme, _, _, _ in all_words:
    theme_count[theme] += 1

# 主题顺序（按文件中出现顺序）
seen_themes = []
for theme, _, _, _ in all_words:
    if theme not in seen_themes:
        seen_themes.append(theme)
print(f'主题数: {len(seen_themes)}')
for t in seen_themes:
    print(f'  {t}: {theme_count[t]} 词')

# === Step 2: 计算每个单词在主题内的序号 ===
# word_theme_index[i] = 第 i 个单词在它所属主题中的序号 (1-based)
theme_running = defaultdict(int)
word_theme_index = []
for theme, _, _, _ in all_words:
    theme_running[theme] += 1
    word_theme_index.append(theme_running[theme])

# === Step 3: 切分为天 ===
schedule = []  # [{day, cycle, type, words, is_partial}]
word_idx = 0
day_num = 1
cycle_num = 1

while word_idx < len(all_words):
    # 5 个新词日
    for _ in range(5):
        if word_idx >= len(all_words):
            break
        day_words = all_words[word_idx:word_idx + WORDS_PER_DAY]
        if not day_words:
            break
        schedule.append({
            'day': day_num,
            'cycle': cycle_num,
            'type': '新词',
            'words': day_words,
            'is_partial': len(day_words) < WORDS_PER_DAY,
        })
        word_idx += len(day_words)
        day_num += 1
    if word_idx >= len(all_words):
        # 最后一个周期，补复习日和休息日
        schedule.append({'day': day_num, 'cycle': cycle_num, 'type': '复习', 'words': []})
        day_num += 1
        schedule.append({'day': day_num, 'cycle': cycle_num, 'type': '休息', 'words': []})
        day_num += 1
        break
    # 复习日
    schedule.append({'day': day_num, 'cycle': cycle_num, 'type': '复习', 'words': []})
    day_num += 1
    # 休息日
    schedule.append({'day': day_num, 'cycle': cycle_num, 'type': '休息', 'words': []})
    day_num += 1
    cycle_num += 1

print(f'\n切分完成: 共 {len(schedule)} 天, {cycle_num} 周期')

# 验证
new_days = [d for d in schedule if d['type'] == '新词']
review_days = [d for d in schedule if d['type'] == '复习']
rest_days = [d for d in schedule if d['type'] == '休息']
print(f'  新词日: {len(new_days)} 天, 共 {sum(len(d["words"]) for d in new_days)} 词')
print(f'  复习日: {len(review_days)} 天')
print(f'  休息日: {len(rest_days)} 天')

# === Step 4: 计算累计新词数（用于完成度行） ===
cum = 0
day_cum = {}  # day_num -> 累计新词数 (进入该日之前)
for d in schedule:
    day_cum[d['day']] = cum
    if d['type'] == '新词':
        cum += len(d['words'])


# === Step 5: 工具函数 ===
def describe_day_theme(words):
    """生成日期的主题说明，如: '家庭与人物（1-20）+ 学校与学习（1-5）'"""
    # 用全局 word_idx 范围来定位
    # 我们已经知道 words 是 all_words 的连续切片
    start_global = None
    end_global = None
    for i, w in enumerate(all_words):
        if w == tuple(words[0]):
            # 找首次出现
            if start_global is None:
                # 验证后面也连续
                if all_words[i:i+len(words)] == list(words):
                    start_global = i
                    end_global = i + len(words) - 1
                    break
    if start_global is None:
        # 兜底（不应该走到）
        return '主题未识别'

    # 按主题分组，统计每个主题在当天的 (min_local_idx, max_local_idx)
    theme_ranges = {}
    for i in range(start_global, end_global + 1):
        theme = all_words[i][0]
        local_idx = word_theme_index[i]
        if theme not in theme_ranges:
            theme_ranges[theme] = [local_idx, local_idx]
        else:
            theme_ranges[theme][0] = min(theme_ranges[theme][0], local_idx)
            theme_ranges[theme][1] = max(theme_ranges[theme][1], local_idx)

    return ' + '.join(f'{t}（{mn}-{mx}）' for t, (mn, mx) in theme_ranges.items())


def get_cycle_themes(cycle_num):
    """获取一个周期内涉及的主题及词数（按出现顺序）"""
    cycle_days = [d for d in schedule if d['cycle'] == cycle_num and d['type'] == '新词']
    if not cycle_days:
        return []
    themes_seen = []
    theme_words = defaultdict(int)
    for d in cycle_days:
        for theme, _, _, _ in d['words']:
            theme_words[theme] += 1
            if theme not in themes_seen:
                themes_seen.append(theme)
    return [(t, theme_words[t]) for t in themes_seen]


# === Step 6: 写入 CSV ===
csv_path = os.path.join(WORKSPACE, 'plan-完整计划.csv')
with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['日期', '类型', '主题', '新词序号', '单词', '中文', '词组'])

    for d in schedule:
        day_label = f"Day {d['day']}"
        if d['type'] == '新词':
            # 计算当天的全局起始 idx
            start_global = None
            for i, w in enumerate(all_words):
                if w == tuple(d['words'][0]):
                    if all_words[i:i+len(d['words'])] == list(d['words']):
                        start_global = i
                        break
            for i, (theme, word, meaning, phrase) in enumerate(d['words']):
                local_idx = word_theme_index[start_global + i]
                writer.writerow([day_label, '新词', theme, local_idx, word, meaning, phrase])
        elif d['type'] == '复习':
            themes = get_cycle_themes(d['cycle'])
            total_words = sum(c for _, c in themes)
            # 主题循环复习行
            for theme, count in themes:
                writer.writerow([day_label, '复习', f'{theme}复习', '—', '—', f'复习 {count} 词', '看英文说中文'])
            # 模糊回炉
            writer.writerow([day_label, '复习', '模糊词回炉', '—', '用户标"模糊"词', '逐个过', '只过不熟的'])
            # 易混辨析（2 个占位行）
            writer.writerow([day_label, '复习', '易混词辨析', '—', '本周期易混词 1', '辨析', '形近/义近对比'])
            writer.writerow([day_label, '复习', '易混词辨析', '—', '本周期易混词 2', '辨析', '形近/义近对比'])
            # 听写测试
            writer.writerow([day_label, '复习', '听写测试', '—', f'本周期 {total_words} 词', '听写', '家长报中文孩子写英文'])
        elif d['type'] == '休息':
            writer.writerow([day_label, '休息', '—', '—', '—', '休息', '—'])

print(f'\nCSV 已写入: {csv_path}')


# === Step 7: 写入 MD ===
md_path = os.path.join(WORKSPACE, 'plan-完整计划.md')

# 主题概要
theme_summary_lines = []
cum_x = 0
for i, theme in enumerate(seen_themes, 1):
    cum_x += theme_count[theme]
    theme_summary_lines.append(f'| {i:>2} | {theme} | {theme_count[theme]} | {cum_x} |')

md_lines = []
md_lines.append('# 暑假共学背单词系统 – 完整 83 天学习计划\n')
md_lines.append('> **核心节奏**：5+1+1（5 天新词 + 1 天复习 + 1 天休息，每周循环）  ')
md_lines.append('> **总词数**：1460 词（按 6 份词表 CSV 实际行数统计）  ')
md_lines.append('> **总天数**：83 天 = 12 周期（11 完整周期 × 7 天 + 1 短周期 × 6 天）  ')
md_lines.append('> **主题数**：24 个（按 PET 主题分类）  ')
md_lines.append('> **每日强度**：25 词（统一强度；如 1 周内连续 3 天未达 80% 准确率，可降为 20 词/天）\n')

md_lines.append('## 📋 主题与词数总览\n')
md_lines.append('| 序号 | 主题 | 词数 | 累计 |')
md_lines.append('|------|------|------|------|')
md_lines.extend(theme_summary_lines)
md_lines.append(f'| **合计** | — | **{len(all_words)}** | — |')
md_lines.append('')

md_lines.append('## 📅 周期与里程碑\n')
md_lines.append('| 周期 | 天数范围 | 覆盖词数范围 | 周期末累计 | 节奏 |')
md_lines.append('|------|----------|--------------|------------|------|')

# 计算每个周期的覆盖范围
cycle_ranges = []
cum_p = 0
for d in schedule:
    pass
# 重新整理
cycle_info = []
cum_p = 0
for cn in range(1, cycle_num + 1):
    cycle_new_days = [d for d in schedule if d['cycle'] == cn and d['type'] == '新词']
    if not cycle_new_days:
        continue
    start_day = cycle_new_days[0]['day']
    end_day = cycle_new_days[-1]['day']
    # 找覆盖的全局词序号范围
    first_word_idx = None
    last_word_idx = None
    for d in cycle_new_days:
        for i, w in enumerate(all_words):
            if w == tuple(d['words'][0]):
                if all_words[i:i+len(d['words'])] == list(d['words']):
                    if first_word_idx is None or i < first_word_idx:
                        first_word_idx = i
                    last_i = i + len(d['words']) - 1
                    if last_word_idx is None or last_i > last_word_idx:
                        last_word_idx = last_i
                    break
    start_global = first_word_idx + 1  # 1-based
    end_global = last_word_idx + 1
    cum_p = end_global
    is_short = len(cycle_new_days) < 5
    rhythm = '短周期' if is_short else '完整周期'
    cycle_info.append((cn, start_day, end_day, start_global, end_global, cum_p, rhythm))

for cn, sd, ed, sg, eg, ce, rhythm in cycle_info:
    md_lines.append(f'| {cn} | Day {sd} – Day {ed} | 词 {sg} – {eg} | {ce}/1460 | {rhythm} |')
md_lines.append('')

md_lines.append('## ⚠️ 生成说明与已知问题\n')
md_lines.append('1. **批次 4 主题误标修复**：原 CSV 中"城市与礼仪"主题有 2 词（block 街区、road 公路）实际属于"城市与建筑"，已在本计划中归回"城市与建筑"。')
md_lines.append('2. **重复词保留**：批次 1-3 中存在少量重复词（passion ×2, confident ×2, dozen ×2, percent ×2, sandwich ×2），保留为不同语境下的词条，未剔除。')
md_lines.append('3. **周期 12 为短周期**：4 个新词日（第 4 日仅 10 词），加 1 复习 + 1 休息 = 6 天。')
md_lines.append('4. **节奏细节**：Day 1 = 周一，每周期内 复习日 = 周六，休息日 = 周日。')
md_lines.append('5. **配套前端**：本计划为内容层，前端单页 HTML 见 Step 3（待启动）。\n')

md_lines.append('---\n')

# === 逐日输出 ===
TOTAL_WORDS = len(all_words)
for cycle in range(1, cycle_num + 1):
    # 周期标题
    cycle_days = [d for d in schedule if d['cycle'] == cycle]
    if not cycle_days:
        continue
    start_day = cycle_days[0]['day']
    end_day = cycle_days[-1]['day']
    new_days = [d for d in cycle_days if d['type'] == '新词']
    cycle_word_count = sum(len(d['words']) for d in new_days)
    themes_in_cycle = get_cycle_themes(cycle)

    md_lines.append(f'\n## 🗓 周期 {cycle}（Day {start_day} – Day {end_day}）｜新词 {cycle_word_count} 词｜{len(themes_in_cycle)} 主题\n')

    theme_desc = '、'.join(f'{t}（{c} 词）' for t, c in themes_in_cycle)
    md_lines.append(f'**本周期主题**：{theme_desc}\n')

    cum_before_cycle = day_cum[start_day]
    cum_after_cycle = cum_before_cycle + cycle_word_count

    # 里程碑提示
    for milestone in [500, 1000, 1500]:
        if cum_before_cycle < milestone <= cum_after_cycle:
            md_lines.append(f'> 🎉 **本周期跨越 {milestone} 词里程碑！** 完成 {milestone} 词 = 已覆盖 {'高考' if milestone >= 1500 else "高考"}核心词表的 {milestone/15:.1f}%\n')

    for d in cycle_days:
        day_num_d = d['day']
        weekday = WEEKDAYS[(day_num_d - 1) % 7]
        cum_before = day_cum[day_num_d]
        cum_after = cum_before + (len(d['words']) if d['type'] == '新词' else 0)

        if d['type'] == '新词':
            # 新词日
            theme_desc_day = describe_day_theme(d['words'])
            n_words = len(d['words'])
            partial_note = '（短日）' if d['is_partial'] else ''
            md_lines.append(f'\n### 📅 Day {day_num_d}（{weekday}）｜新词 {n_words} 词{partial_note}｜累计 {cum_after}/{TOTAL_WORDS}\n')
            md_lines.append(f'**主题**：{theme_desc_day}\n')
            md_lines.append('| # | 单词 | 中文 | 词组 | 状态 |')
            md_lines.append('|---|------|------|------|------|')

            start_global = None
            for i, w in enumerate(all_words):
                if w == tuple(d['words'][0]):
                    if all_words[i:i+len(d['words'])] == list(d['words']):
                        start_global = i
                        break
            for i, (theme, word, meaning, phrase) in enumerate(d['words']):
                global_num = start_global + i + 1  # 1-based
                phrase_disp = phrase if phrase else '—'
                md_lines.append(f'| {global_num} | {word} | {meaning} | {phrase_disp} | ⬜ |')

            md_lines.append('')
            md_lines.append(f'**今日完成度**：0/{n_words} | **总进度**：0/{TOTAL_WORDS}（0%）\n')
            md_lines.append('---\n')

        elif d['type'] == '复习':
            md_lines.append(f'\n### 📅 Day {day_num_d}（{weekday}）｜🌀 复习日｜不学新词\n')
            md_lines.append(f'> **本周期 {cycle_word_count} 词已学完。Day {day_num_d} 不学新词，专门用来"巩固"前 5 天的内容。**\n')

            md_lines.append('#### ⏰ 上午 30 分钟｜整体过一遍\n')
            md_lines.append('**A. 主题循环复习（20 min）**\n')
            md_lines.append('| 主题 | 词数 | 用法 | 时间 |')
            md_lines.append('|------|------|------|------|')
            # 主题按 4 分钟一个，最多列 5 个；超过则按比例
            n_themes = len(themes_in_cycle)
            per_theme_min = 20 // n_themes if n_themes <= 5 else max(2, 20 // n_themes)
            for theme, count in themes_in_cycle:
                md_lines.append(f'| {theme} | {count} | 看英文说中文，不熟的打 ⭐ | {per_theme_min} min |')

            md_lines.append('\n**B. 模糊词回炉（5 min）**')
            md_lines.append('把本周所有 ⭐（标记模糊）的词集中再过一遍，只过不熟的。\n')

            md_lines.append('**C. 易混词辨析（5 min）**')
            md_lines.append(f'- 本周期易混词 1（形近/义近对比）')
            md_lines.append(f'- 本周期易混词 2（形近/义近对比）')
            md_lines.append(f'- （具体辨析内容家长根据孩子薄弱点现场补充）\n')

            md_lines.append('#### ⏰ 下午 15 分钟｜听写测试\n')
            md_lines.append('家长报中文 → 孩子写英文 → 对照批改\n')
            md_lines.append(f'- **目标准确率**：≥ 90%（{int(cycle_word_count * 0.9)}/{cycle_word_count}）')
            md_lines.append(f'- **未达标**：错词进入"周末加练"列表\n')

            md_lines.append('\n#### 🌙 晚上 5 分钟｜复盘 + 打卡\n')
            md_lines.append(f'- 记录本周学完词数（本周期：{cycle_word_count} 词，累计：{cum_after}/{TOTAL_WORDS}）')
            md_lines.append(f'- 标记明天休息（Day {day_num_d + 1} 周日）')
            if cycle < cycle_num:
                next_cycle_themes = get_cycle_themes(cycle + 1)
                preview_themes = '、'.join(f'{t}' for t, _ in next_cycle_themes[:3])
                md_lines.append(f'- 标记后天（Day {day_num_d + 2} 周一）预习下一周期主题：{preview_themes} 等（提前看一遍）')
            else:
                md_lines.append('- 🎉 这是最后一个周期！Day 83 之后系统达成 1460 词，可以光荣退休 ✨\n')

            md_lines.append('\n---\n')

        elif d['type'] == '休息':
            md_lines.append(f'\n### 📅 Day {day_num_d}（{weekday}）｜💤 休息日｜不背词\n')
            md_lines.append('> 完整休息，不安排任何学习任务。')
            md_lines.append('> 可以：')
            md_lines.append('> - 听英文儿歌 / 看英文动画（磨耳朵）')
            md_lines.append('> - 翻一翻之前学过的单词本（无意识重复）')
            md_lines.append('> - 户外运动 / 自由玩耍\n')
            md_lines.append('---\n')

# === 末尾总结 ===
md_lines.append('\n## 📊 83 天总览\n')
md_lines.append('| 指标 | 数值 |')
md_lines.append('|------|------|')
md_lines.append(f'| 总周期 | 12 周期（11 完整 + 1 短） |')
md_lines.append(f'| 总天数 | 83 天 |')
md_lines.append(f'| 新词日 | {len(new_days)} 天 |')
md_lines.append(f'| 复习日 | {len(review_days)} 天 |')
md_lines.append(f'| 休息日 | {len(rest_days)} 天 |')
md_lines.append(f'| 总词数 | {TOTAL_WORDS} 词 |')
md_lines.append(f'| 日均强度 | {TOTAL_WORDS / len(new_days):.1f} 词/新词日 |')
md_lines.append(f'| 主题数 | {len(seen_themes)} 个 |')
md_lines.append('')

md_lines.append('## 🎯 计划完成 = 系统退休\n')
md_lines.append('按本计划执行完 83 天，1460 词全部过完一轮。')
md_lines.append('这意味着：')
md_lines.append('- 三年级的孩子已建立自主背单词的方法论 + 1500+ 基础词库')
md_lines.append('- 高一的孩子已重塑信心 + 高考核心词覆盖到位')
md_lines.append('- 工具的使命完成：可以光荣退休，转向"以读促背"的自主学习阶段\n')

md_lines.append('## 📁 配套文件\n')
md_lines.append('- `plan-完整计划.csv`：83 天逐日逐词清单，可导入 Excel / 单词 App')
md_lines.append('- `plan-完整计划.md`：本文件，按日 / 按周期组织的可执行版本')
md_lines.append('- `样章/plan-样章-5天.{csv,md}`：5 天样章（已确认，作为风格参考）')
md_lines.append('- `vocab-*.csv / .md`：6 份主题词表（内容来源）\n')

with open(md_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(md_lines))

print(f'MD 已写入: {md_path}')
print(f'  总行数: {len(md_lines)}')
