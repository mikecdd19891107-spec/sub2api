import { sanitizeUrl } from '@/utils/url'

export const DEFAULT_BRAND_NAME = 'AgentByte'

/**
 * Resolves the display brand name, replacing empty or uncustomized stock "AgentByte"
 * values with "AgentByte" while preserving any custom site name.
 */
export function resolveBrandName(name?: string | null): string {
  const trimmed = typeof name === 'string' ? name.trim() : ''
  if (!trimmed || trimmed.toLowerCase() === 'agentbyte') {
    return DEFAULT_BRAND_NAME
  }
  return trimmed
}

export function updateFavicon(logoUrl: string): void {
  const sanitizedLogoUrl = sanitizeUrl(logoUrl, {
    allowRelative: true,
    allowDataUrl: true,
  })
  if (!sanitizedLogoUrl) {
    return
  }

  let link = document.querySelector<HTMLLinkElement>('link[rel="icon"]')
  if (!link) {
    link = document.createElement('link')
    link.rel = 'icon'
    document.head.appendChild(link)
  }

  link.type = sanitizedLogoUrl.endsWith('.svg') ? 'image/svg+xml' : 'image/x-icon'
  link.href = sanitizedLogoUrl
}
