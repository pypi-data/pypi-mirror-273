





/*
	import { scan_goals } from '@/fleet/nutrition_meadow/goals/scan_emblem'
	const { 
		status,
		parsed,
		proceeds
	} = await scan_goals ({ 
		freight: {}
	})
	if (status !== 200) { 
		
	}
	
*/

import { lap } from '@/fleet/syllabus/lap'	
	
export const scan_goals = async ({
	freight
}) => {
	return await lap ({
		envelope: {
			"label": "nutrition meadow, goals: scan emblem",
			"freight": freight
		}
	});
}