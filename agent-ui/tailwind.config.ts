import type { Config } from 'tailwindcss'
import tailwindcssAnimate from 'tailwindcss-animate'

export default {
  darkMode: ['class'],
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}'
  ],
  theme: {
    extend: {
      colors: {
        primary: '#212529', // Dark gray for text (good contrast)
        primaryAccent: '#808080', // Neutral gray for accents
        brand: 'rgba(0, 130, 9, 0.8)', // Bright orange for branding
        background: {
          DEFAULT: '#FFFFFF', // White background for the main panel
          secondary: '#CED4DA', // Very light gray for secondary panels
          tertiary: '#E9ECEF', // Light gray for tertiary panels
          quaternary: '#DEE2E6', // Slightly darker gray for additional contrast
          quinary: '#CED4DA' // Medium gray for testing deeper contrast
        },
        secondary: '#ADB5BD', // Medium gray for borders or subtle elements
        border: '#6C757D', // Neutral gray for visible borders
        accent: '#868E96', // Muted gray for accents
        muted: '#A1A1AA', // Muted gray for less prominent text
        destructive: '#E03131', // Softer red for destructive actions
        positive: '#37B24D' // Softer green for success messages
      },
      fontFamily: {
        geist: 'var(--font-geist-sans)',
        dmmono: 'var(--font-dm-mono)'
      },
      borderRadius: {
        xl: '10px'
      }
    }
  },
  plugins: [tailwindcssAnimate]
} satisfies Config
