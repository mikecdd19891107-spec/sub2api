/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // 品牌色 - 单一橙色色相，只用于点缀（选中态、链接、图表强调）
        // 600 起可作白底文字色（对比度 ≥ 4.5:1）
        primary: {
          50: '#FFF7ED',
          100: '#FFEDD5',
          200: '#FED7AA',
          300: '#FDBA74',
          400: '#FB923C',
          500: '#E8590C',
          600: '#C2410C',
          700: '#9A3412',
          800: '#7C2D12',
          900: '#5C2410',
          950: '#431407'
        },
        // 中性色 - gray / accent / dark 统一为同一套中性灰
        gray: {
          50: '#FAFAF9',
          100: '#F4F4F2',
          200: '#EAEAE7',
          300: '#D6D6D2',
          400: '#A1A1A8',
          500: '#6E6E73',
          600: '#4A4A50',
          700: '#2E2E33',
          800: '#1C1C1F',
          900: '#141416',
          950: '#0B0B0C'
        },
        accent: {
          50: '#FAFAF9',
          100: '#F4F4F2',
          200: '#EAEAE7',
          300: '#D6D6D2',
          400: '#A1A1A8',
          500: '#6E6E73',
          600: '#4A4A50',
          700: '#2E2E33',
          800: '#1C1C1F',
          900: '#141416',
          950: '#0B0B0C'
        },
        dark: {
          50: '#FAFAF9',
          100: '#F4F4F2',
          200: '#EAEAE7',
          300: '#D6D6D2',
          400: '#A1A1A8',
          500: '#6E6E73',
          600: '#4A4A50',
          700: '#2E2E33',
          800: '#1C1C1F',
          900: '#141416',
          950: '#0B0B0C'
        },
        // 主操作色（近黑），深色模式下反转为近白
        ink: {
          DEFAULT: '#0B0B0C',
          hover: '#2E2E33',
          inverse: '#FAFAF9'
        }
      },
      fontFamily: {
        sans: [
          'Inter',
          '-apple-system',
          'BlinkMacSystemFont',
          'system-ui',
          '"Segoe UI"',
          '"PingFang SC"',
          '"Hiragino Sans GB"',
          '"Microsoft YaHei"',
          '"Noto Sans SC"',
          'sans-serif'
        ],
        mono: [
          '"JetBrains Mono"',
          '"SF Mono"',
          'ui-monospace',
          'SFMono-Regular',
          'Menlo',
          'Consolas',
          'monospace'
        ]
      },
      boxShadow: {
        // 扁平化：保留旧名称以兼容现有组件，但效果统一为轻阴影
        glass: '0 1px 2px rgba(11, 11, 12, 0.04), 0 4px 12px -4px rgba(11, 11, 12, 0.06)',
        'glass-sm': '0 1px 2px rgba(11, 11, 12, 0.04)',
        glow: 'none',
        'glow-lg': 'none',
        card: '0 1px 2px rgba(11, 11, 12, 0.03)',
        'card-hover': '0 4px 16px -4px rgba(11, 11, 12, 0.10)',
        'inner-glow': 'none'
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-primary': 'linear-gradient(0deg, #0B0B0C 0%, #0B0B0C 100%)',
        'gradient-dark': 'linear-gradient(0deg, #141416 0%, #141416 100%)',
        'gradient-glass': 'none',
        'mesh-gradient': 'none'
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
          '0%': { boxShadow: '0 0 20px rgba(232, 89, 12, 0.20)' },
          '100%': { boxShadow: '0 0 34px rgba(232, 89, 12, 0.30)' }
        }
      },
      backdropBlur: {
        xs: '2px',
        '2xl': '40px',
        '3xl': '64px'
      },
      borderRadius: {
        // 收紧圆角：现有 rounded-xl/2xl/3xl 用法整体变小
        xl: '0.625rem',
        '2xl': '0.75rem',
        '3xl': '0.875rem',
        '4xl': '1rem',
        '5xl': '1.25rem'
      }
    }
  },
  plugins: []
}
