// petVocabLoader.ts — PET 词库加载器（内联 pet_schedule_final.json）
import petSchedule from '../../../pet_schedule_final.json';

export interface PETWord {
  word: string;
  pos: string;
  meaning: string;
}

export interface PETPhrase {
  phrase: string;
  meaning: string;
  source: 'book' | 'cambridge_official';
  associated_word?: string;
}

export interface PETDay {
  day: number;
  grammar_stage: number;
  words: PETWord[];
  phrases: PETPhrase[];
}

export interface PETSchedule {
  total_days: number;
  words_per_day: number;
  total_words: number;
  total_phrases: number;
  schedule: PETDay[];
}

const scheduleData = petSchedule as unknown as PETSchedule;

export function getTotalDays(): number {
  return scheduleData.total_days;
}

export function getDayData(day: number): PETDay | undefined {
  return scheduleData.schedule.find(d => d.day === day);
}

export function getDayWords(day: number): PETWord[] {
  const d = getDayData(day);
  return d?.words || [];
}

export function getDayPhrases(day: number): PETPhrase[] {
  const d = getDayData(day);
  return d?.phrases || [];
}

export function getAllWordsFlat(): PETWord[] {
  const result: PETWord[] = [];
  for (const d of scheduleData.schedule) {
    result.push(...d.words);
  }
  return result;
}

export function searchWords(query: string): { word: PETWord; day: number }[] {
  const q = query.toLowerCase().trim();
  if (!q) return [];
  const results: { word: PETWord; day: number }[] = [];
  for (const d of scheduleData.schedule) {
    for (const w of d.words) {
      if (w.word.toLowerCase().includes(q) || w.meaning.includes(q)) {
        results.push({ word: w, day: d.day });
        if (results.length >= 50) break;
      }
    }
    if (results.length >= 50) break;
  }
  return results;
}

export function searchPhrases(query: string): { phrase: PETPhrase; day: number }[] {
  const q = query.toLowerCase().trim();
  if (!q) return [];
  const results: { phrase: PETPhrase; day: number }[] = [];
  for (const d of scheduleData.schedule) {
    for (const p of d.phrases) {
      if (p.phrase.toLowerCase().includes(q) || p.meaning.includes(q)) {
        results.push({ phrase: p, day: d.day });
        if (results.length >= 30) break;
      }
    }
    if (results.length >= 30) break;
  }
  return results;
}

export { scheduleData as petSchedule };
