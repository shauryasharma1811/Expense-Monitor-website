/**
 * @type {import('tailwindcss').Config}
 */
module.exports = {
  content: ['./src/**/*.{ts,tsx,js,jsx,html}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50:  '#f3f4ff',
          100: '#e6e7ff',
          200: '#c4c7ff',
          300: '#a0a4ff',
          400: '#7d83ff',
          500: '#5b61ff',
          600: '#474cdb',
          700: '#3233a6',
          800: '#1b1b73',
          900: '#0a0a39',
        },
        semantic: {
          success: {
            50: '#fdfdfb',
            100: '#fafaf8',
            200: '#f6f6f3',
            300: '#f0efea',
            400: '#e8e4d9',
            500: '#e0dac8',
            600: '#d5ceba',
            700: '#c7c0a7',
            800: '#bab39b',
            900: '#a8a097',
          },
          danger: {
            50: '#fdf6f6',
            100: '#fde8e8',
            200: '#fccaca',
            300: '#f9a6a6',
            400: '#f47575',
            500: '#f14b4b',
            600: '#dd3d3d',
            700: '#c83030',
            800: '#b22424',
            900: '#800000',
          },
        },
      },
    },
  },
  plugins: [],
}
