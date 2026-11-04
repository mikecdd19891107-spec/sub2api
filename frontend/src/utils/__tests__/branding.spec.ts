import { beforeEach, describe, expect, it } from 'vitest'
import { DEFAULT_BRAND_NAME, resolveBrandName, updateFavicon } from '@/utils/branding'

describe('resolveBrandName', () => {
  it('returns AgentByte for empty or stock Sub2API names', () => {
    expect(DEFAULT_BRAND_NAME).toBe('AgentByte')
    expect(resolveBrandName('')).toBe('AgentByte')
    expect(resolveBrandName('   ')).toBe('AgentByte')
    expect(resolveBrandName(undefined)).toBe('AgentByte')
    expect(resolveBrandName('Sub2API')).toBe('AgentByte')
    expect(resolveBrandName('sub2api')).toBe('AgentByte')
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
