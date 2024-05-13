









	


from vegan.besties.supp_NIH.nature_v2._ops.retrieve import retrieve_parsed_NIH_supp
from vegan.adventures.alerting import activate_alert
from vegan.adventures.sanique.utilities.check_key import check_key

import sanic.response as sanic_response



def besties__supp_NIH__nature_v2__DSLD_ID (packet):
	app = packet ["app"]
	openapi = packet ["openapi"]
	NIH_supp_ellipse = packet ["NIH_supp_ellipse"]
	staff_addresses = packet ["staff_addresses"]
	
	@staff_addresses.route ("/besties/supp_NIH/nature_v2/<DLSD_ID>")
	@openapi.summary ("Supp")
	@openapi.description ("Supp parsing route, examples: 69439")
	@openapi.parameter ("opener", str, "header")
	async def NIH_supp (request, DLSD_ID):
		data = request.json
	
		lock_status = check_key (request)
		if (lock_status != "unlocked"):
			return lock_status		
	
		try:
			out_packet = retrieve_parsed_NIH_supp ({
				"DSLD_ID": DLSD_ID,
				"NIH API Pass": NIH_supp_ellipse
			})
			
			if ("anomaly" in out_packet):
				if (out_packet ["anomaly"] == "The NIH API could not find that DLSD_ID."):
					return sanic_response.json (out_packet, status = 604)
			
				return sanic_response.json (out_packet, status = 600)
			
			return sanic_response.json (out_packet)
			
		except Exception as E:
			print (str (E))
			
		return sanic_response.json ({
			"anomaly": "An unaccounted for anomaly occurred."
		}, status = 600)