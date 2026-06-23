import React, { useState, useMemo } from 'react';
import { Card } from '../components/Card';
import { petSchedule, PETWord } from '../services/utils/petVocabLoader';

type FilterType = 'all' | 'mastered' | 'fuzzy';

export function Vocabulary() {
  const [query, setQuery] = useState('');
  const [filter, setFilter] = useState<FilterType>('all');
  const [saved, setSaved] = useState<Record<string, string>>(() => {
    try { return JSON.parse(localStorage.getItem('di_states') || '{}'); }
    catch { return {}; }
  });

  const allWords = useMemo(() => {
    const result: { word: PETWord; day: number }[] = [];
    for (const d of petSchedule.schedule) {
      for (const w of d.words) {
        result.push({ word: w, day: d.day });
      }
    }
    return result;
  }, []);

  const filtered = useMemo(() => {
    let items = allWords;
    const q = query.toLowerCase().trim();
    if (q) {
      items = items.filter(i => i.word.word.toLowerCase().includes(q) || i.word.meaning.includes(q));
    }
    switch (filter) {
      case 'mastered': return items.filter(i => saved[i.word.word] === 'mastered');
      case 'fuzzy': return items.filter(i => saved[i.word.word] === 'fuzzy');
      default: return items;
    }
  }, [allWords, query, filter, saved]);

  return (
    <div className="space-y-4">
      <h1 className="text-lg font-bold text-gray-800">PET 词库</h1>

      <input
        value={query}
        onChange={e => setQuery(e.target.value)}
        placeholder="搜索单词..."
        className="w-full px-4 py-2.5 bg-white border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
      />

      <div className="flex gap-2">
        {[
          { id: 'all' as FilterType, label: `全部 (${allWords.length})` },
          { id: 'mastered' as FilterType, label: '已掌握' },
          { id: 'fuzzy' as FilterType, label: '△ 模糊' },
        ].map(f => (
          <button
            key={f.id}
            onClick={() => setFilter(f.id)}
            className={`px-3 py-1.5 rounded-full text-xs ${
              filter === f.id ? 'bg-primary-500 text-white' : 'bg-gray-100 text-gray-600'
            }`}
          >
            {f.label}
          </button>
        ))}
      </div>

      <div className="space-y-2">
        {filtered.slice(0, 100).map(i => {
          const s = saved[i.word.word];
          return (
            <Card key={i.word.word} className="py-3">
              <div className="flex items-center justify-between">
                <div>
                  <span className="font-medium text-gray-800">{i.word.word}</span>
                  <span className="text-xs text-gray-400 ml-2">_{i.word.pos}_</span>
                  <span className="text-sm text-gray-500 ml-2">{i.word.meaning}</span>
                  <span className="text-xs text-gray-400 ml-2">Day {i.day}</span>
                </div>
                <span className={`text-sm px-2 py-0.5 rounded-full ${
                  s === 'mastered' ? 'bg-green-100 text-green-700' :
                  s === 'fuzzy' ? 'bg-yellow-100 text-yellow-700' :
                  'bg-gray-100 text-gray-400'
                }`}>
                  {s === 'mastered' ? '✓' : s === 'fuzzy' ? '△' : '○'}
                </span>
              </div>
            </Card>
          );
        })}
        {filtered.length === 0 && (
          <p className="text-center text-gray-400 py-8">没有匹配结果</p>
        )}
      </div>
    </div>
  );
}
