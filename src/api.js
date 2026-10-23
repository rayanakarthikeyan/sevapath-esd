import { createClient } from '@insforge/sdk';
import { sanitizePlan } from './knowledge.js';
const baseUrl = import.meta.env.VITE_INSFORGE_URL;
const anonKey = import.meta.env.VITE_INSFORGE_ANON_KEY;
const client = baseUrl && anonKey ? createClient({baseUrl, anonKey}) : null;
export const configured = Boolean(client);
export function getToken() {
  let token = localStorage.getItem('sevapath-key');
  if (!/^[a-f0-9]{64}$/.test(token || '')) {
    token = [...crypto.getRandomValues(new Uint8Array(32))].map(x => x.toString(16).padStart(2,'0')).join('');
    localStorage.setItem('sevapath-key', token);
  }
  return token;
}
async function rpc(action, data = {}) {
  if (!client) throw new Error('Cloud is not configured. Your preparation stays on this device.');
  const { data: result, error } = await client.database.rpc('sevapath_draft', { p_action:action, p_token:getToken(), p_data:data });
  if (error) throw new Error('Cloud request failed. Your device copy is safe. Try again when connected.');
  return result;
}
export const saveDraft = plan => rpc('save', sanitizePlan(plan));
export const loadDraft = () => rpc('load');
export const deleteDraft = () => rpc('delete');
export const sendFeedback = helpful => rpc('feedback', {helpful});
export async function checkCloud() {
  if (!client) return false;
  try { const {data,error} = await client.database.from('service_sources').select('id').limit(1); return !error && data?.length === 1; }
  catch { return false; }
}
