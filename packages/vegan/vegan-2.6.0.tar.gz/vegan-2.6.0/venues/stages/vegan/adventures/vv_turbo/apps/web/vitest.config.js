



import { fileURLToPath } 				from 'node:url'
import { mergeConfig, defineConfig } 	from 'vite'

import { configDefaults } 				from 'vitest/config'
import viteConfig 						from './vite.config'

export default mergeConfig(
	viteConfig,
	defineConfig ({
		test: {
			environment: 'jsdom',
			
			include: [
				'**/*.{test,spec,ST,status}.?(c|m)[jt]s?(x)'
			],
			
			exclude: [
				...configDefaults.exclude, 
				'e2e/*'
			],
			root: fileURLToPath (
				new URL ('./', import.meta.url)
			),
			transformMode: {
				web: [/\.[jt]sx$/]
			}
		}
	})
)
