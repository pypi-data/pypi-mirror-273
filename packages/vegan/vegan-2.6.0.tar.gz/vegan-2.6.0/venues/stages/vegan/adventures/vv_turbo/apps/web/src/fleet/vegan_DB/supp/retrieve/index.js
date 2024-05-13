

/*
	priorities:
		use grid/lap
*/


/*
	import { retrieve_supp } from '@/fleet/vegan_DB/supp/retrieve'
	const { proceeds, tropical } = await retrieve_supp ({ emblem })
*/

import { lap } from '@/fleet/syllabus/lap'

import { goals_store } from '@/warehouses/goals'

export async function retrieve_supp ({
	emblem
}) {	
	var goal = {}
	if (goals_store.warehouse ().goal_picked) {
		goal = goals_store.warehouse ().goal
	}
	
	return await lap ({
		path: "guests",
		envelope: {
			"label": "retrieve supp",
			"freight": {
				"filters": {
					"emblem": emblem
				},
				goal
			}
		}
	});
}