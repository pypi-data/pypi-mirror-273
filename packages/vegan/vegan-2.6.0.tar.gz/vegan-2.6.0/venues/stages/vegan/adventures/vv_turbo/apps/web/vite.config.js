


import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig ({
	// base: '/assets',
	plugins: [
		vue ()
	],
	resolve: {
		alias: {
			'@': fileURLToPath (new URL ('./src', import.meta.url)),
			'@%': fileURLToPath (new URL ('./../../shares', import.meta.url))
		}
	}
})
