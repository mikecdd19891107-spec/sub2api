import { describe, expect, it } from 'vitest'
import { formatCurrency } from '../format'

describe('金额显示符号', () => {
  it('只替换美元显示符号，不改变数值', () => {
    const result = formatCurrency(12.34, 'USD')
    expect(result).toContain('¥')
    expect(result).toContain('12.34')
    expect(result).not.toContain('$')
  })

  it('仅替换其他币种的显示符号，保留数值', () => {
    expect(formatCurrency(12.34, 'EUR')).toContain('¥')
    expect(formatCurrency(12.34, 'EUR')).toContain('12.34')
  })
})
