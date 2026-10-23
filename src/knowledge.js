export const sources = [
  { id: 'income-form', title: 'Income certificate application form', publisher: 'Government of Telangana', url: 'https://www.telangana.gov.in/wp-content/uploads/2023/03/IncomeGeneralApplicationForm.pdf', detail: 'Document alternatives and the citizen-login exception.' },
  { id: 'meeseva-faq', title: 'MeeSeva mobile governance FAQ', publisher: 'Government of Telangana', url: 'https://mgov.telangana.gov.in/faqnew.html', detail: 'Preparation, editing, upload limits and service guidance. Published guidance may describe an older interface.' },
  { id: 'state-services', title: 'Public utility forms', publisher: 'Telangana State Portal', url: 'https://www.telangana.gov.in/services/public-utility-forms/', detail: 'Official index of citizen application forms.' }
];
export const reviewedOn = '23 October 2026';
export const serviceNames = { income: 'Income certificate', birth: 'Birth certificate', residence: 'Residence certificate', pension: 'Pension services' };
const training = {
  income: ['income certificate salary earnings proof affidavit income proof family income annual income', 'scholarship fee reimbursement college admission financial aid student income certificate', 'aadayam certificate income ledu salary slip ledu scholarship kosam', 'ఆదాయ ధృవీకరణ పత్రం ఆదాయం జీతం స్కాలర్‌షిప్ ఫీజు కాలేజీ ఉపకార వేతనం', 'I need proof of my family earnings for college', 'no payslip self employed income document'],
  birth: ['birth certificate child baby newborn birth registration date of birth', 'పుట్టిన తేదీ జనన ధృవీకరణ బిడ్డ జనన నమోదు', 'puttina birth certificate baby registration'],
  residence: ['residence certificate address proof resident residential domicile living proof', 'నివాస ధృవీకరణ చిరునామా నివాసం', 'nivasam certificate address proof'],
  pension: ['old age pension senior citizen widow disability pension aasara retirement elderly', 'ఆసరా పింఛను వృద్ధాప్య వితంతు వికలాంగుల పెన్షన్', 'aasara pension pinchan old age']
};
const stopwords = new Set('a an the i my me need want for of to is am can have get how do you with and please help apply'.split(' '));
export function tokenize(text) {
  return text.normalize('NFKC').toLowerCase().replace(/\b(aadayam|aadayam|aadayamu)\b/g,'income').match(/[\p{L}\p{M}\p{N}]+/gu)?.filter(t => !stopwords.has(t)) || [];
}
// Local TF-IDF nearest-prototype classifier. No LLM, API key or remote inference.
const docs = Object.entries(training).map(([id, examples]) => ({ id, terms: tokenize(examples.join(' ')) }));
const vocabulary = new Set(docs.flatMap(d => d.terms));
const idf = Object.fromEntries([...vocabulary].map(t => [t, Math.log((1 + docs.length) / (1 + docs.filter(d => d.terms.includes(t)).length)) + 1]));
function vector(terms) {
  const v = {}; for (const term of terms) if (idf[term]) v[term] = (v[term] || 0) + idf[term];
  const norm = Math.sqrt(Object.values(v).reduce((s, n) => s + n * n, 0));
  return Object.fromEntries(Object.entries(v).map(([k, n]) => [k, n / (norm || 1)]));
}
const models = docs.map(d => ({ id: d.id, vector: vector(d.terms) }));
export function classify(text) {
  if (typeof text !== 'string' || text.length > 500) throw new Error('Use 1–500 characters.');
  const terms = tokenize(text); const query = vector(terms);
  const ranked = models.map(m => ({ id: m.id, score: Object.entries(query).reduce((s, [k, v]) => s + v * (m.vector[k] || 0), 0) })).sort((a,b) => b.score - a.score);
  const best = ranked[0];
  const ambiguous = best.score < 0.12 || best.score - ranked[1].score < 0.055;
  return { service: ambiguous ? null : best.id, score: Number(best.score.toFixed(3)), ambiguous,
    alternatives: ranked.filter(r => r.score > 0.1).map(r => r.id),
    needsPurposeConfirmation: /scholar|reimburs|college|admission|ఫీజు|స్కాలర్|కాలేజీ|upakara/i.test(text),
    evidence: best.id === 'income' && !ambiguous ? ['income-form','meeseva-faq'] : ['state-services'],
    engine: 'local-tfidf-v1', scoreMeaning: 'Similarity score, not a calibrated probability or an eligibility decision.' };
}
export function requirements(plan, lang = 'en') {
  const te = lang === 'te';
  const rows = [
    { key:'identity_ready', title: te ? 'గుర్తింపు పత్రం' : 'One identity document', text: te ? 'రేషన్ కార్డు, ఆధార్ కార్డు లేదా ఓటరు గుర్తింపు కార్డు — వీటిలో ఒకటి.' : 'A ration card, Aadhaar card or voter ID (EPIC). One alternative from the published form.', source:'income-form' },
    { key:'income_ready', title: te ? 'ఆదాయానికి ఆధారం' : 'Evidence of income', text: te ? 'ఐటీ రిటర్న్, పే స్లిప్, ఆదాయ ఆధారం లేదా అఫిడవిట్. మీ పరిస్థితికి తగిన ఆధారాన్ని కేంద్రంతో నిర్ధారించుకోండి.' : 'An IT return, payslip, income evidence or affidavit. No payslip? The form lists alternatives; confirm the suitable proof with MeeSeva.', source:'income-form' },
    { key:'photo_ready', title: te ? 'పాస్‌పోర్ట్ సైజు ఫోటో' : 'Passport-size photograph', text: te ? 'స్పష్టమైన, ఇటీవలి ఫోటో సిద్ధంగా ఉంచండి.' : 'Keep a clear passport-size photograph ready.', source:'income-form' }
  ];
  if (plan.channel === 'centre') rows.push({ key:'form_ready', title: te ? 'నింపిన దరఖాస్తు' : 'Completed application form', text: te ? 'MeeSeva కేంద్రం మార్గం కోసం దరఖాస్తు సిద్ధం చేయండి. సిటిజన్ లాగిన్‌కు ఫారం తప్పనిసరి కాదని ప్రచురిత పత్రం చెబుతుంది.' : 'Prepare the application for a centre visit. The published form exempts citizen login from this requirement.', source:'income-form' });
  return rows;
}
export function readiness(plan) {
  const rows = requirements(plan); const completed = rows.filter(r => plan[r.key] === true).length;
  return { completed, total: rows.length, percent: Math.round(completed / rows.length * 100), ready: completed === rows.length };
}
export function validateFile({type,size}, photo = false) {
  if (!['application/pdf','image/jpeg'].includes(type) || (photo && type !== 'image/jpeg')) return { ok:false, message:photo ? 'Choose a JPEG photograph.' : 'Choose a PDF or JPEG file.' };
  const limit = photo ? 20 * 1024 : 3 * 1024 * 1024;
  if (!Number.isFinite(size) || size <= 0 || size > limit) return { ok:false, message:photo ? 'Photo exceeds the published 20 KB reference limit, or is empty.' : 'Document exceeds the published 3 MB reference limit, or is empty.' };
  return { ok:true, message:'Format and size fit the published reference limits. Content and authenticity are not checked.' };
}
export function blankPlan() { return { language:'en', channel:'citizen', employment:'other', identity_ready:false, income_ready:false, photo_ready:false, form_ready:false }; }
export function sanitizePlan(input) {
  const d = blankPlan();
  if (!input || typeof input !== 'object') return d;
  for (const k of ['identity_ready','income_ready','photo_ready','form_ready']) d[k] = input[k] === true;
  if (['en','te'].includes(input.language)) d.language = input.language;
  if (['citizen','centre'].includes(input.channel)) d.channel = input.channel;
  if (['salaried','self','other'].includes(input.employment)) d.employment = input.employment;
  return d;
}
