import json, random

with open('pet_schedule_v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Gather all words with their tier info
# We stored the order: ket words, ket_new, pet interleaved, pet_new, extra
# Let's categorize by difficulty based on word length and commonality

all_words = []
for d in data['schedule']:
    all_words.extend(d['words'])

# Add missing basic KET words
missing_basics = [
    {'word': 'a', 'pos': 'det', 'meaning': '一个'},
    {'word': 'two', 'pos': 'num', 'meaning': '二'},
    {'word': 'three', 'pos': 'num', 'meaning': '三'},
    {'word': 'four', 'pos': 'num', 'meaning': '四'},
    {'word': 'five', 'pos': 'num', 'meaning': '五'},
    {'word': 'six', 'pos': 'num', 'meaning': '六'},
    {'word': 'seven', 'pos': 'num', 'meaning': '七'},
    {'word': 'eight', 'pos': 'num', 'meaning': '八'},
    {'word': 'nine', 'pos': 'num', 'meaning': '九'},
    {'word': 'ten', 'pos': 'num', 'meaning': '十'},
]
existing = {w['word'].lower() for w in all_words}
for w in missing_basics:
    if w['word'] not in existing:
        all_words.insert(0, w)  # Add to front (easy words)

print(f'总词数(含新增基础词): {len(all_words)}')

# Categorize words by difficulty
# Easy: length <= 5 or in KET official (based on word length as heuristic)
# The real KET/PET distinction was lost during serialization
# Let's use word length as a rough proxy and also detect common KET words
common_ket = {'the','a','an','is','am','are','have','has','do','does','go','get',
    'can','will','may','must','should','would','could','like','love','want',
    'need','know','think','see','look','hear','say','tell','ask','answer',
    'give','take','make','put','come','go','run','walk','eat','drink','sleep',
    'read','write','speak','listen','play','work','study','help','call',
    'open','close','sit','stand','turn','show','try','keep','find','lose',
    'one','two','three','four','five','six','seven','eight','nine','ten',
    'first','second','third','last','next','every','some','any','many','much',
    'few','little','big','small','large','long','short','tall','high','low',
    'new','old','good','bad','hot','cold','warm','cool','fast','slow',
    'happy','sad','angry','tired','hungry','thirsty','sick','well','fine',
    'red','blue','green','black','white','yellow','pink','purple','brown','grey',
    'apple','banana','orange','grape','water','milk','bread','rice','egg',
    'meat','fish','fruit','vegetable','cake','candy','sugar','salt',
    'mother','father','brother','sister','friend','family','house','home',
    'school','teacher','student','child','baby','man','woman','boy','girl',
    'name','number','word','letter','book','pen','pencil','paper','bag',
    'table','chair','door','window','room','bed','desk','chair','floor','wall',
    'car','bus','train','plane','ship','bike','taxi','foot',
    'day','week','month','year','today','tomorrow','yesterday',
    'morning','afternoon','evening','night','time','clock','hour','minute',
    'cat','dog','bird','fish','horse','cow','pig','sheep','duck','chicken',
    'head','hand','foot','eye','ear','nose','mouth','arm','leg','hair'}

def estimate_difficulty(word):
    w = word.lower()
    if len(w) <= 4 and w.isalpha():
        return 1  # Very easy
    if w in common_ket:
        return 1  # Common KET word
    if len(w) <= 6:
        return 2  # Medium
    return 3  # Hard

# Sort words by difficulty
easy_words = [w for w in all_words if estimate_difficulty(w['word']) == 1]
medium_words = [w for w in all_words if estimate_difficulty(w['word']) == 2]
hard_words = [w for w in all_words if estimate_difficulty(w['word']) == 3]

print(f'简单词: {len(easy_words)}')
print(f'中等词: {len(medium_words)}')
print(f'困难词: {len(hard_words)}')

random.shuffle(easy_words)
random.shuffle(medium_words)
random.shuffle(hard_words)

# Build ordered list: first 40 days = easy only, then mix medium, then all
easy_only_days = 40
words_per_day = 30
easy_needed = easy_only_days * words_per_day

ordered = []

# Phase 1: Easy only (~40 days)
if len(easy_words) >= easy_needed:
    phase1 = easy_words[:easy_needed]
    remaining_easy = easy_words[easy_needed:]
else:
    phase1 = list(easy_words)
    remaining_easy = []

ordered.extend(phase1)

# Phase 2: Remaining easy + some medium (interleaved)
remaining = remaining_easy + medium_words
random.shuffle(remaining)
ordered.extend(remaining)

# Phase 3: Hard words
ordered.extend(hard_words)

print(f'排序后总词: {len(ordered)}')

# Build new schedule
schedule = []
for i in range(0, len(ordered), words_per_day):
    chunk = ordered[i:i+words_per_day]
    day_num = len(schedule) + 1
    schedule.append({'day': day_num, 'words': chunk, 'phrases': []})

# Redistribute phrases
with open('pet_schedule_final.json', 'r', encoding='utf-8') as f:
    old = json.load(f)

seen = set()
all_phrases = []
for d in old['schedule']:
    for p in d['phrases']:
        key = p['phrase'].strip().lower()
        if key not in seen:
            seen.add(key)
            all_phrases.append({
                'phrase': p['phrase'],
                'meaning': p.get('meaning', ''),
                'source': p.get('source', 'book'),
                'associated_word': p.get('associated_word', ''),
            })

random.shuffle(all_phrases)
num_days = len(schedule)
ppd = max(1, len(all_phrases) // num_days)
extra = len(all_phrases) - ppd * num_days
idx = 0
for i, day in enumerate(schedule):
    count = ppd + (1 if i < extra else 0)
    day['phrases'] = all_phrases[idx:idx+count]
    idx += count

output = {'schedule': schedule}
with open('pet_schedule_v2.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f'\n✅ 已完成')
print(f'   天数: {len(schedule)}')
print(f'   总词: {sum(len(d["words"]) for d in schedule)}')
print(f'   总短语: {sum(len(d["phrases"]) for d in schedule)}')
print(f'   前5天样本:')
for d in schedule[:3]:
    print(f'     Day {d["day"]}: {[w["word"] for w in d["words"][:8]]}')
