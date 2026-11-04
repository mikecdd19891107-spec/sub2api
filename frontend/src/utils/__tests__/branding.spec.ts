import { beforeEach, describe, expect, it } from 'vitest'
import { DEFAULT_BRAND_NAME, resolveBrandName, updateFavicon } from '@/utils/branding'

describe('resolveBrandName', () => {
  it('returns AgentByte for empty or stock AgentByte names', () => {
    expect(DEFAULT_BRAND_NAME).toBe('AgentByte')
    expect(resolveBrandName('')).toBe('AgentByte')
    expect(resolveBrandName('   ')).toBe('AgentByte')
    expect(resolveBrandName(undefined)).toBe('AgentByte')
    expect(resolveBrandName('AgentByte')).toBe('AgentByte')
    expect(resolveBrandName('agentbyte')).toBe('AgentByte')
  })

  it('preserves custom site names', () => {
    expect(resolveBrandName('Custom Studio')).toBe('Custom Studio')
    expect(resolveBrandName('AgentByte Pro')).toBe('AgentByte Pro')
  })
})

describe('updateFavicon', () => {
  beforeEach(() => {
    document.head.innerHTML = '<link rel="icon" href="/logo.svg">'
  })

  it('replaces the default favicon with the configured logo', () => {
    updateFavicon('https://example.com/custom-logo.png')

    const link = document.querySelector<HTMLLinkElement>('link[rel="icon"]')
    expect(link?.href).toBe('https://example.com/custom-logo.png')
  })

  it('ignores unsafe logo URLs', () => {
    updateFavicon('javascript:alert(1)')

    const link = document.querySelector<HTMLLinkElement>('link[rel="icon"]')
    expect(link?.getAttribute('href')).toBe('/logo.svg')
  })
})
