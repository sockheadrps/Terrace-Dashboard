/** @type {import('tailwindcss').Config} */
module.exports = {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		screens: {
			'tablet': {'min': '640px', 'max': '860px'}
	},

		
		extend: {
			backgroundImage: {
				original: {
					astro: "var(--bg-astro)"
			}
			},
			textColor: {
				original : {
					base: 'var(--color-text-base)',
					muted: 'var(--color-text-muted)',
					iconhover: 'var(color-table-icon-hover)',
					'muted-hover': 'var(--color-text-muted-hover)',
					success: 'var(--color-text-success)'
				},
			},
			backgroundColor: {
				original: {
					fill: 'var(--color-input-bg-light)',
					'input-hover': 'var(--color-input-bg-hover)',
					'table-header': 'var(--color-table-header)',
					'table-header-focus': 'var(--color-table-header-focus)',
					'table-row-even': 'var(--color-table-row-even)',
					'card-bg-dark': 'var(--color-bg-dark)',
					'nav-background': 'var(--color-bg-lighter-dark)',
					'service-dark': 'var(--color-service-bg-dark)',
					'icon-finder-background': 'var(--color-icon-finder-bg)',
					'settings-nav-bg': 'var(--color-bg-nav-background)',
					'settings-nav-bg-hover': 'var(--color-bg-nav-background-hover)',
					'success-background': 'var(--color-bg-success)'

				}
			},
			borderColor: {
				original: {
					muted: 'var(--color-text-muted)',
					dark: 'var(--color-border-dark)'
				}
			}
		}
	},
	plugins: []
};
