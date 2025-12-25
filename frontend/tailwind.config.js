/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                space: {
                    950: '#050510', // Deep void
                    900: '#0b0d17',
                    800: '#161b22',
                    700: '#21262d',
                },
                cosmos: {
                    300: '#c084fc', // Purple glow
                    500: '#a855f7',
                    900: '#581c87',
                },
                starlight: {
                    100: '#e0f2fe',
                    400: '#38bdf8', // Blue glow
                    600: '#0284c7',
                }
            },
            animation: {
                'spin-slow': 'spin 20s linear infinite',
                'pulse-glow': 'pulse-glow 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                'float': 'float 6s ease-in-out infinite',
            },
            keyframes: {
                'pulse-glow': {
                    '0%, 100%': { opacity: '1', boxShadow: '0 0 20px #a855f7' },
                    '50%': { opacity: '.8', boxShadow: '0 0 50px #38bdf8' },
                },
                'float': {
                    '0%, 100%': { transform: 'translateY(0)' },
                    '50%': { transform: 'translateY(-20px)' },
                }
            }
        },
    },
    plugins: [],
}
