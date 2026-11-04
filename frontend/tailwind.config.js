/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // 主色调 - Amber / Warm Orange 琥珀流光金橙色系 (AgentByte Brand)
        primary: {
          50: '#fffbeb',
          100: '#fef3c7',
          200: '#fde68a',
          300: '#fcd34d',
          400: '#fbbf24',
          500: '#f59e0b',
          600: '#ea580c',
          700: '#c2410c',
          800: '#9a3412',
          900: '#7c2d12',
          950: '#431407'
        },
        // 辅助色 - 暖曜石中性灰
        accent: {
          50: '#fafaf9',
          100: '#f5f5f4',
          200: '#e7e5e4',
          300: '#d6d3d1',
          400: '#a8a29e',
          500: '#78716c',
          600: '#57534e',
          700: '#332f2c',
          800: '#211e1b',
          900: '#141210',
          950: '#0b0a09'
        },
        // 深色模式背景 - Apple 曜石暖黑系
        dark: {
          50: '#fafaf9',
          100: '#f5f5f4',
          200: '#e7e5e4',
          300: '#d6d3d1',
          400: '#a8a29e',
          500: '#78716c',
          600: '#57534e',
          700: '#332f2c',
          800: '#211e1b',
          900: '#141210',
          950: '#0b0a09'
        }
      },
      fontFamily: {
        sans: [
          '-apple-system',
          'BlinkMacSystemFont',
          '"SF Pro Display"',
          '"SF Pro Text"',
          'Inter',
          'system-ui',
          'Segoe UI',
          'Roboto',
          'Helvetica Neue',
          'PingFang SC',
          'Hiragino Sans GB',
          'Microsoft YaHei',
          'sans-serif'
        ],
        mono: [
          '"SF Mono"',
          '"JetBrains Mono"',
          'ui-monospace',
          'SFMono-Regular',
          'Menlo',
          'Monaco',
          'Consolas',
          'monospace'
        ]
      },
      boxShadow: {
        glass:
          '0 12px 40px -8px rgba(15, 10, 5, 0.10), 0 4px 16px -4px rgba(15, 10, 5, 0.05), inset 0 1px 0 0 rgba(255, 255, 255, 0.65)',
        'glass-sm':
          '0 4px 20px -2px rgba(15, 10, 5, 0.06), inset 0 1px 0 0 rgba(255, 255, 255, 0.5)',
        glow: '0 0 24px rgba(245, 158, 11, 0.30)',
        'glow-lg': '0 0 48px rgba(245, 158, 11, 0.42)',
        card: '0 4px 24px -4px rgba(15, 10, 5, 0.05), 0 1px 3px 0 rgba(15, 10, 5, 0.03), inset 0 1px 0 0 rgba(255, 255, 255, 0.6)',
        'card-hover':
          '0 16px 48px -8px rgba(245, 158, 11, 0.14), 0 6px 20px -4px rgba(15, 10, 5, 0.08)',
        'inner-glow': 'inset 0 1px 0 rgba(255, 255, 255, 0.18)'
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-primary': 'linear-gradient(135deg, #f59e0b 0%, #ea580c 100%)',
        'gradient-dark': 'linear-gradient(135deg, #211e1b 0%, #141210 100%)',
        'gradient-glass':
          'linear-gradient(135deg, rgba(255,255,255,0.16) 0%, rgba(255,255,255,0.05) 100%)',
        'mesh-gradient':
          'radial-gradient(at 25% 15%, rgba(245, 158, 11, 0.14) 0px, transparent 52%), radial-gradient(at 85% 5%, rgba(234, 88, 12, 0.10) 0px, transparent 48%), radial-gradient(at 10% 75%, rgba(251, 191, 36, 0.09) 0px, transparent 50%), radial-gradient(at 80% 85%, rgba(249, 115, 22, 0.08) 0px, transparent 50%)'
      },
      animation: {
        'fade-in': 'fadeIn 0.3s cubic-bezier(0.16, 1, 0.3, 1)',
        'slide-up': 'slideUp 0.35s cubic-bezier(0.16, 1, 0.3, 1)',
        'slide-down': 'slideDown 0.35s cubic-bezier(0.16, 1, 0.3, 1)',
        'slide-in-right': 'slideInRight 0.35s cubic-bezier(0.16, 1, 0.3, 1)',
        'scale-in': 'scaleIn 0.25s cubic-bezier(0.16, 1, 0.3, 1)',
        'pulse-slow': 'pulse 3.5s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        shimmer: 'shimmer 2s linear infinite',
        glow: 'glow 2.5s ease-in-out infinite alternate'
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' }
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(12px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' }
        },
        slideDown: {
          '0%': { opacity: '0', transform: 'translateY(-12px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' }
        },
        slideInRight: {
          '0%': { opacity: '0', transform: 'translateX(20px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' }
        },
        scaleIn: {
          '0%': { opacity: '0', transform: 'scale(0.95)' },
          '100%': { opacity: '1', transform: 'scale(1)' }
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' }
        },
        glow: {
          '0%': { boxShadow: '0 0 20px rgba(245, 158, 11, 0.25)' },
          '100%': { boxShadow: '0 0 34px rgba(234, 88, 12, 0.42)' }
        }
      },
      backdropBlur: {
        xs: '2px',
        '2xl': '40px',
        '3xl': '64px'
      },
      borderRadius: {
        '4xl': '2rem',
        '5xl': '2.5rem'
      }
    }
  },
  plugins: []
}
