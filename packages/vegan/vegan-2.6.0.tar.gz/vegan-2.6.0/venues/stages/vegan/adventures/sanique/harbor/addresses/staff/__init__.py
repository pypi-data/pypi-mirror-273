

#----
#
from vegan._essence import retrieve_essence, build_essence
from vegan.adventures.sanique.utilities.check_key import check_key
#
from vegan.shows_v2.recipe._ops.retrieve import retrieve_recipe
from vegan.shows_v2.recipe_with_goals._ops.formulate import formulate_recipe_with_goals	
#
#
import sanic
from sanic import Sanic
from sanic_ext import openapi
import sanic.response as sanic_response
#
#----

def addresses_staff (packet):
	staff_addresses = packet ["staff_addresses"]
	
	@staff_addresses.route ("/essence")
	@openapi.parameter ("opener", str, "header")
	async def address_essence (request):
		essence = retrieve_essence ()

		lock_status = check_key (request)
		if (lock_status != "unlocked"):
			return lock_status

		return sanic.json (essence)
		
		
	@staff_addresses.get ('/goals/<region>')
	@openapi.summary ("goals")
	@openapi.description ("goals")
	async def goals_by_region (request, region):
		try:
			ingredient_doc = retrieve_one_goal ({
				"region": region
			})
			
			return sanic_response.json (ingredient_doc)
			
		except Exception as E:
			show_variable (str (E))
			
		return sanic_response.json ({
			"anomaly": "An unaccounted for anomaly occurred."
		}, status = 600)
		
	
	'''
		 https://sanic.dev/en/plugins/sanic-ext/openapi/decorators.html#ui
	'''
	@staff_addresses.patch ('/shows_v2/recipe')
	@openapi.summary ("recipe")
	@openapi.description ("""
	
		{ 
			"IDs_with_amounts": [
				{
					"DSLD_ID": "276336",
					"packets": 10
				},
				{
					"DSLD_ID": "214893",
					"packets": 20
				},
				{
					"FDC_ID": "2412474",
					"packets": 20
				}
			] 
		}
		
	""")
	@openapi.body({
		"application/json": {
			"properties": {
				"IDs_with_amounts": { "type": "list" }
			}
		}
	})
	#@doc.produces ({'message': str})
	#@doc.response (200, {"message": "Hello, {name}!"})
	async def recipe (request):
		data = request.json
	
		show_variable ({
			"data": data
		}, mode = "pprint")
	
		try:
			recipe_packet = retrieve_recipe ({
				"IDs_with_amounts": data ["IDs_with_amounts"]
			})
			if (len (recipe_packet ["not_added"]) >= 1):
				not_found_len = len (recipe_packet ["not_added"]);
				assert (type (not_found_len) == int)
			
				not_found_len = str (not_found_len)
			
				return sanic_response.json ({
					"anomaly": f"{ not_found_len } could not be found."
				}, status = 600)
			
			assert (len (recipe_packet ["not_added"]) == 0)
			
			recipe_with_goals_packet = formulate_recipe_with_goals ({
				"recipe": recipe_packet ["recipe"],
				"goal_region": "2"
			})
			
			recipe = recipe_with_goals_packet ["recipe"]	
			
			return sanic_response.json (recipe_with_goals_packet ["recipe"])
			
		except Exception as E:
			print (str (E))
			
		return sanic_response.json ({
			"anomaly": "An unaccounted for anomaly occurred."
		}, status = 600)