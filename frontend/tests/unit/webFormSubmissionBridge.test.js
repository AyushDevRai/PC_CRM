import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'
import { runInNewContext } from 'node:vm'

const html = readFileSync(join(dirname(fileURLToPath(import.meta.url)), '../../../crm/www/crm_form.html'), 'utf8')
const source = html.split('// [submission-bridge:start]')[1].split('// [submission-bridge:end]')[0]
function bridge(overrides = {}) {
  const calls = []
  const context = {
    EMBED: true, DRAFT: false, DOCTYPE: 'CRM Lead', WEB_FORM: 'sales', URL,
    document: { referrer: 'http://localhost:3000/hockey' },
    window: { parent: { postMessage: (...args) => calls.push(args) } }, ...overrides,
  }
  const notify = runInNewContext(`${source}; notifyEmbeddingPage`, context)
  notify({ email: 'pilot@example.com', mobile_no: '+919876543210', first_name: 'Private', custom_organization_type: 'School' })
  return calls
}
describe('CRM form submission bridge', () => {
  it('sends only identity to the exact embedding origin', () => {
    const calls = bridge()
    expect(calls).toHaveLength(1)
    expect(calls[0][1]).toBe('http://localhost:3000')
    expect(calls[0][0]).toEqual({ type: 'crm:form-submitted', documentType: 'CRM Lead', formName: 'sales', identity: { email: 'pilot@example.com', phone: '+919876543210' } })
  })
  it('does not send draft previews, deals, standalone forms or referrer-less messages', () => {
    expect(bridge({ DRAFT: true })).toHaveLength(0)
    expect(bridge({ DOCTYPE: 'CRM Deal' })).toHaveLength(0)
    expect(bridge({ EMBED: false })).toHaveLength(0)
    expect(bridge({ document: { referrer: '' } })).toHaveLength(0)
  })
  it('the notification is gated by successful submission and precedes form reset', () => {
    const success = html.indexOf('notifyEmbeddingPage(values);')
    expect(success).toBeGreaterThan(html.indexOf('if (!res.ok)'))
    expect(success).toBeLessThan(html.indexOf('form.reset();', success))
  })
})
