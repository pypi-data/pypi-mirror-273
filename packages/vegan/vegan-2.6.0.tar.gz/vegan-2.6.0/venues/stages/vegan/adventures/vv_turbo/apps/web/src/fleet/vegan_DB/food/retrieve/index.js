
/*
	priorities:
		use grid/lap
*/


/*
	import { retrieve_food } from '@/fleet/vegan_DB/food/retrieve'
	const { 
		status,
		parsed,
		proceeds
	} = await retrieve_food ({ emblem })
*/

import { lap } from '@/fleet/syllabus/lap'
import { goals_store } from '@/warehouses/goals'

export async function retrieve_food ({
	emblem
}) {	
	var goal = {}
	if (goals_store.warehouse ().goal_picked) {
		goal = goals_store.warehouse ().goal
	}
	
	return await lap ({
		path: "guests",
		envelope: {
			"label": "retrieve food",
			"freight": {
				"filters": {
					"emblem": emblem
				},
				"goal": goal
			}
		}
	});
}



//