




/*
	{ home, habitat }

*/

import s_panel from '@/scenery/panel/decor.vue'
import mascot from '@/scenery/mascot/craft.vue'

import panel_sink_caution from './panels/panel_sink_caution.vue'
import panel_sink from './panels/panel_sink.vue'

import panel_1 from './panels/panel_1.vue'
import panel_health from './panels/panel_health.vue'
import panel_physics from './panels/panel_physics.vue'
import panel_tech from './panels/panel_tech.vue'
import panel_goodness from './panels/panel_goodness.vue'
import panel_moon from './panels/panel_moon.vue'

import panel_organic_crop_farming from '@/regions/guests/habitat/panels/panel_organic_crop_farming.vue'

export const decor = {
	components: { 
		s_panel, 
		mascot, 

		panel_sink,			
		panel_sink_caution,
		panel_1, 
		panel_health,
		panel_physics,
		panel_tech,
		panel_goodness,
		panel_moon,
		
		panel_organic_crop_farming
	},
	
	data () {
		return {
			wheat: `url("\/bits\/pexels-pierre-sudre-55766.jpg")`,
			moon: `url("\/bits\/pexels-min-an-713664.jpg")`,
			water: `url("\/bits\/pexels-berend-de-kort-1452701.jpg")`,
			cloud: `url("\/bits\/pexels-emma-trewin-813770.jpg")`,
			
			wind: `url("\/bits\/pexels-narcisa-aciko-1292464.jpg")`,
			solar: `url("\/bits\/mrganso\/photovoltaic-system-2742302_1920.jpg")`,
			
			// 
			
			

			food: `url("\/bits\/jensenartofficial\/food-8346107_1920.jpg")`,

			mergers: `url("\/bits\/background-1462755_1920.jpg")`,
			
			cart: `url("\/bits\/thanksgiving-3804849_1920.jpg")`,
			
			

			universe: `url("\/bits\/universe.png")`,

			pitachios: `url("\/bits\/NoName_13--pistachios-1540123_1920.jpg")`,

			// slogan: "The best tasting food is here.",
			// slogan: "the nearest vegan food and vegan supplements",
			// slogan2: "helping vegans make sure they are getting all the nutrients they need."
			
			
			panel_1: {
				title: "Earliest",
				slogan: "Grow all the essential nutrients in developing regions from plants, fungi, and algae."
			},
			
			//
			panel_3: {
				title: "Climate",
				slogan: "Reduce the energy and land necessary to advance and sustain life."
			},
			
		}
	}
}