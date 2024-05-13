


'''
	import vegan.adventures.monetary.quests.search_goods.techniques.obtain_proceeds as obtain_proceeds
	obtain_proceeds.smoothly (
		DB = 
		filters = {
			"string": "lentils",
			"include": {
				"food": True,
				"supp": False
			},
			"limit": 10,
			
			
			#
			#	has either "before" or "after"
			#
			
			"before": {
				"emblem": 32,
				"kind": "food",
				"name": "POMEGRANATE JUICE, POMEGRANATE"
			},
			
			"after": {
				"emblem": 32,
				"kind": "food",
				"name": "POMEGRANATE JUICE, POMEGRANATE"
			},
			
			"format": 1
		}
	)
'''

'''
	agenda:
		aggregation steps:
			[ ] unionize "food" and "supp" -> "food_emblem" and "supp_emblem"

			[ ] has "nature.identity.name" and "emblem"
			[ ] add "lower_case_name" = "$nature.identity.name".lower ()
			[ ] [filter (if scan string)] by scan string
			[ ] sort by "lower_case_name", then "emblem" in alphabetical order
			
			[ ] add "before" and "after" stats
			[ ] (conditionally) sort by "lower_case_name", then "emblem" in reverse alphabetical order
			
			[ ] [filter (if vector)] by name vector
			[ ] [filter (if vector)] by name and emblem vector									
			
			[ ] limit the documents returned

			[ ] if reversed, forward sort by "lower_case_name", then "emblem"

			[ ] format
'''

import vegan.adventures.monetary.quests.search_goods.techniques.obtain_proceeds.spruce.filters as spruce_filters
import vegan.adventures.monetary.quests.search_goods.techniques.obtain_proceeds.affirm.direction as affirm_direction

#
#	aggregation steps
#
#
import vegan.adventures.monetary.quests.search_goods.techniques.obtain_proceeds.aggregation_steps.unionize as unionize
import vegan.adventures.monetary.quests.search_goods.techniques.obtain_proceeds.aggregation_steps.check_fields as check_fields
import vegan.adventures.monetary.quests.search_goods.techniques.obtain_proceeds.aggregation_steps.lower_case_name as lower_case_name
import vegan.adventures.monetary.quests.search_goods.techniques.obtain_proceeds.aggregation_steps.sort_name_emblem as sort_name_emblem
import vegan.adventures.monetary.quests.search_goods.techniques.obtain_proceeds.aggregation_steps.filters.scan_string as filter_by_scan_string
import vegan.adventures.monetary.quests.search_goods.techniques.obtain_proceeds.aggregation_steps.before_and_after as before_and_after
import vegan.adventures.monetary.quests.search_goods.techniques.obtain_proceeds.aggregation_steps.filters.vector_name as filter_by_vector_name
import vegan.adventures.monetary.quests.search_goods.techniques.obtain_proceeds.aggregation_steps.filters.vector_name_and_emblem as filter_by_vector_name_and_emblem
import vegan.adventures.monetary.quests.search_goods.techniques.obtain_proceeds.aggregation_steps.filters.limit as limit_documents

import vegan.adventures.monetary.quests.search_goods.techniques.obtain_proceeds.aggregation_steps.formats.format_1 as format_1


import rich

from vegan.adventures.monetary.DB.vegan_inventory.connect import connect_to_vegan_inventory
	

def obtain_proceeds (
	filters = None
):
	spruce_filters.solid (
		filters = filters, 
		limit_limit = 100
	)
	
	if ("format" not in filters):
		format = 1
	
	direction = affirm_direction.solid (filters = filters)
	is_before = direction ["is_before"]
	is_after = direction ["is_after"]
	if (is_before and is_after):
		raise Exception (f'Vectors "after" and "before" currently cannot both be included.')

	scan_string = filters ["string"]
	limit = filters ["limit"]
	include_food = filters ["include"] ["food"]
	include_supp = filters ["include"] ["supp"]
	
	
	'''
		join starts from one collection and 
		then adds the other.
	'''
	if (
		(include_food and include_supp) or
		(include_food and not include_supp) 
	):		
		collection = "food"
	elif (include_supp and not include_food):
		collection = "supp"
	else:
		return []
		
		
	'''
		direction
	'''
	if (is_before):
		vector_direction = "before"
		reverse = True
	else:
		vector_direction = "after"
		reverse = False
	
	
	ask = []
	unity = unionize.occur (
		include_food = include_food,
		include_supp = include_supp
	)
	for u in unity:
		ask.append (u)
	

	ask.append (check_fields.occur ())
	ask.append (lower_case_name.occur ())


	scan_string_filter = filter_by_scan_string.occur (
		scan_string = scan_string
	);
	if (type (scan_string_filter) == dict):
		ask.append (scan_string_filter)


	ask.append (sort_name_emblem.occur (reverse = False))
	ask.append (before_and_after.occur (reverse = False))

	if (reverse == True):
		ask.append (sort_name_emblem.occur (reverse = reverse))
	
	
	'''
		start from a certain point.
	'''
	if (is_before or is_after):
		if (is_before):
			vector = filters ["before"]
		else:
			vector = filters ["after"]

		vector_kind = vector ["kind"]
		vector_name = vector ["name"].lower ()
		vector_emblem = vector ["emblem"]
		
		if (vector_kind == "food"):
			vector_unique_emblem = "food_emblem"
		else:
			vector_unique_emblem = "supp_emblem"
			
		ask.append (
			filter_by_vector_name_and_emblem.occur (
				kind = vector ["kind"],
				name = vector_name,
				emblem = vector ["emblem"],
				
				direction = vector_direction
			)
		)
	
		ask.append (
			filter_by_vector_name.occur (
				name = vector_name,
				direction = vector_direction
			)
		)
	
	
	
	
	'''
		?? if before, needs to be reverse = True before this line.
	'''
	ask.append (limit_documents.occur (limit))
	if (reverse == True):
		ask.append (sort_name_emblem.occur (reverse = False))

	
	'''
		This step erases fields from the documents
		and prepares the document to only have
		designated fields.
	'''
	ask.append (format_1.occur ())
	

	rich.print_json (data = {
		"aggregate": ask
	})


	'''
		This is where the query is actually run.
	'''
	[ driver, vegan_inventory_DB ] = connect_to_vegan_inventory ()
	documents = vegan_inventory_DB [ collection ].aggregate (ask)
	driver.close ()
	
	return {
		"documents": documents
	};
	
	
	
	
	
	
	
	#