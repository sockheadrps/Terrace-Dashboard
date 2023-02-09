/** @type {import('tailwindcss').Config} */
module.exports = {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			backgroundImage: {
				space: "url('./src/assets/backgrnd.jpeg)",
			},
			textColor: {
				original : {
					base: 'var(--color-text-base)',
					muted: 'var(--color-text-muted)',
				},
			},
			backgroundColor: {
				original: {
					fill: 'var(--color-input-bg-light)',
					'input-hover': 'var(--color-input-bg-hover)'
				}
			},
			borderColor: {
				original: {
					muted: 'var(--color-text-muted)'
				}
			}
		}
	},
	plugins: []
};
