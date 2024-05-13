





'''
	python3 status.proc.py shows/ingredient_scan_recipe/formulate/_status/status_rational_amounts/status_1.py
'''

#----
#
import vegan.besties.food_USDA.deliveries.one.assertions.foundational as assertions_foundational
import vegan.besties.food_USDA.examples as USDA_examples	
import vegan.besties.food_USDA.nature_v2 as food_USDA_nature_v2
#
import vegan.besties.supp_NIH.nature_v2 as supp_NIH_nature_v2
import vegan.besties.supp_NIH.examples as NIH_examples
#
import vegan.mixes.insure.equality as equality
#
from vegan.shows_v2.recipe._ops.formulate import formulate_recipe
from vegan.shows_v2.treasure.nature.land.grove._ops.seek_name_or_accepts import seek_name_or_accepts	
#
#
from copy import deepcopy
from fractions import Fraction
import json
#
#----

def find_grams (measures):
	return Fraction (
		measures ["mass + mass equivalents"] ["per recipe"] ["grams"] ["fraction string"]
	)

def check_1 ():
	def retrieve_supp (supp_path):
		return supp_NIH_nature_v2.create (
			NIH_examples.retrieve (supp_path) 
		)
	
	def retrieve_food (food_path):
		return food_USDA_nature_v2.create (
			USDA_examples.retrieve (food_path)
		)
	
	print (json.dumps (retrieve_food ("branded/beet_juice_2412474.JSON"), indent = 4))
	
	recipe = formulate_recipe ({
		"natures_with_amounts": [
			[ retrieve_supp ("coated tablets/multivitamin_276336.JSON"), 1.2 ],
			[ retrieve_supp ("other/chia_seeds_214893.JSON"), 1.4 ]
		]
	})
	
	def add (path, data):
		import pathlib
		from os.path import dirname, join, normpath
		this_directory = pathlib.Path (__file__).parent.resolve ()
		example_path = normpath (join (this_directory, path))
		FP = open (example_path, "w")
		FP.write (data)
		FP.close ()
		
	add ("status_1.JSON", json.dumps (recipe, indent = 4))
	
	assert (
		len (recipe ["essential nutrients"] ["natures"]) == 2
	), len (recipe ["essential nutrients"] ["natures"])
	


	
checks = {
	"check 1": check_1
}