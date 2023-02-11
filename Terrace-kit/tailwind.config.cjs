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
					iconhover: 'var(color-table-icon-hover)'
				},
			},
			backgroundColor: {
				original: {
					fill: 'var(--color-input-bg-light)',
					'input-hover': 'var(--color-input-bg-hover)',
					'table-header': 'var(--color-table-header)',
					'table-header-focus': 'var(--color-table-header-focus)',
					'table-row-even': 'var(--color-table-row-even)'
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
