









	

#----
#
from vegan.besties.food_USDA.nature_v2._ops.retrieve import retrieve_parsed_USDA_food
from vegan.adventures.alerting import activate_alert
#
from vegan.adventures.sanique.utilities.check_key import check_key
#
#
import sanic.response as sanic_response
#
#----

def besties__food_USDA__nature_v2__FDC_ID (packet):
	app = packet ["app"]
	openapi = packet ["openapi"]
	USDA_food_ellipse = packet ["USDA_food_ellipse"]
	staff_addresses = packet ["staff_addresses"]

	'''
		 https://sanic.dev/en/plugins/sanic-ext/openapi/decorators.html#ui
	'''
	@staff_addresses.route ('/besties/food_USDA/nature_v2/<FDC_ID>')
	@openapi.summary ("Food")
	@openapi.description ("Food parsing route, examples: 2369390")
	@openapi.parameter ("opener", str, "header")
	#@doc.produces ({'message': str})
	#@doc.response (200, {"message": "Hello, {name}!"})
	async def USDA_food_FDC_ID (request, FDC_ID):
		activate_alert ("info", "/besties/food_USDA/nature_v2/<FDC_ID>")

		lock_status = check_key (request)
		if (lock_status != "unlocked"):
			return lock_status		
	
		try:
			out_packet = retrieve_parsed_USDA_food ({
				"FDC_ID": FDC_ID,
				"USDA API Pass": USDA_food_ellipse
			})
			
			if ("anomaly" in out_packet):
				if (out_packet ["anomaly"] == "The USDA API could not find that FDC_ID."):
					return sanic_response.json (out_packet, status = 604)
			
				return sanic_response.json (out_packet, status = 600)
			
			return sanic_response.json (out_packet)
			
		except Exception as E:
			print (str (E))
			
		return sanic_response.json ({
			"anomaly": "An unaccounted for anomaly occurred."
		}, status = 600)