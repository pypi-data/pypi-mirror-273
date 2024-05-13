
'''
	python3 insurance.py shows/ingredient_scan_recipe/formulate/_status/status_food/status_1.py
'''



#----
#
import vegan.besties.food_USDA.deliveries.one.assertions.foundational as assertions_foundational
import vegan.besties.food_USDA.examples as USDA_examples	
import vegan.besties.food_USDA.nature_v2 as food_USDA_nature_v2
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
	walnuts_1882785 = food_USDA_nature_v2.create (
		USDA_examples.retrieve ("branded/walnuts_1882785.JSON")
	)
	vegan_pizza_2672996 = food_USDA_nature_v2.create (
		USDA_examples.retrieve ("branded/vegan_pizza_2672996.JSON")
	)

	walnuts_1882785_1 = deepcopy (walnuts_1882785)
	vegan_pizza_2672996_1 = deepcopy (vegan_pizza_2672996)

	#print (json.dumps (walnuts_1882785 ["measures"], indent = 4))

	walnut_mass_and_mass_eq_grams = Fraction ("47746738154613173415299/112589990684262400000")
	walnut_energy_food_calories = Fraction ("154133/50")
	walnut_multiplier = 10

	vegan_pizza_2672996_mass_and_mass_eq_grams = Fraction ("1484714659522158138277/45035996273704960000")
	vegan_pizza_2672996_energy_food_calories = Fraction ("2627/20")
	vegan_pizza_2672996_multiplier = 100
	
	'''
		walnuts: 5021813355368299589/7036874417766400 713.6425999999999
		vegan pizza: 89531560592125469/2251799813685248 39.760000000000005
	'''	
	assert (
		walnuts_1882785  ["essential nutrients"] ["measures"] ==
		{
			"mass + mass equivalents": {
				"per recipe": {
					"grams": {
						'scinote string': '4.2408e+2',
						"fraction string": str (walnut_mass_and_mass_eq_grams)
					}
				}
			},
			"energy": {
				"per recipe": {
					"food calories": {
						'scinote string': '3.0827e+3',
						"fraction string": str (walnut_energy_food_calories)
					}
				}
			}
		}
	), walnuts_1882785 ["essential nutrients"] ["measures"]
	assert (
		vegan_pizza_2672996 ["essential nutrients"] ["measures"] ==
		{
			"mass + mass equivalents": {
				"per recipe": {
					"grams": {
						'scinote string': '3.2967e+1',
						"fraction string": str (vegan_pizza_2672996_mass_and_mass_eq_grams)
					}
				}
			},
			"energy": {
				"per recipe": {
					"food calories": {
						'scinote string': '1.3135e+2',
						"fraction string": str (vegan_pizza_2672996_energy_food_calories)
					}
				}
			}
		}
	), vegan_pizza_2672996 ["essential nutrients"] ["measures"]

	recipe = formulate_recipe ({
		"natures_with_amounts": [
			[ walnuts_1882785, walnut_multiplier ],
			[ vegan_pizza_2672996, vegan_pizza_2672996_multiplier ]
		]
	})
	assert (
		recipe ["essential nutrients"] ["measures"] ==
		{
			"mass + mass equivalents": {
				"per recipe": {
					"grams": {
						"fraction string": str (
							(walnut_mass_and_mass_eq_grams * walnut_multiplier) +
							(vegan_pizza_2672996_mass_and_mass_eq_grams * vegan_pizza_2672996_multiplier)							
						),
						'scinote string': '7.5375e+3'
					}
				}
			},
			"energy": {
				"per recipe": {
					"food calories": {
						"fraction string": str (
							(walnut_energy_food_calories * walnut_multiplier) +
							(vegan_pizza_2672996_energy_food_calories * vegan_pizza_2672996_multiplier)							
						),
						'scinote string': '4.3962e+4'
					}
				}
			}
		}
	), recipe ["essential nutrients"] ["measures"]
	
	
	def assert_ingredient (ingredient):
		walnuts_1882785_ingredient_1 = seek_name_or_accepts (
			grove = walnuts_1882785_1 ["essential nutrients"] ["grove"],
			name_or_accepts = ingredient
		)
		vegan_pizza_2672996_ingredient_1 = seek_name_or_accepts (
			grove = vegan_pizza_2672996_1 ["essential nutrients"] ["grove"],
			name_or_accepts = ingredient
		)
		
		print ("original:")
		print (
			"	walnuts:", 
			(find_grams (walnuts_1882785_ingredient_1 ["measures"])),
			float (find_grams (walnuts_1882785_ingredient_1 ["measures"])),
		)
		print (
			"	vegan pizza:", 
			(find_grams (vegan_pizza_2672996_ingredient_1 ["measures"])),
			float (find_grams (vegan_pizza_2672996_ingredient_1 ["measures"]))
		)
		
		print ()
	
		walnuts_1882785_ingredient = seek_name_or_accepts (
			grove = walnuts_1882785 ["essential nutrients"] ["grove"],
			name_or_accepts = ingredient
		)
		vegan_pizza_2672996_ingredient = seek_name_or_accepts(
			grove = vegan_pizza_2672996 ["essential nutrients"] ["grove"],
			name_or_accepts = ingredient
		)
		recipe_ingredient = seek_name_or_accepts (
			grove = recipe ["essential nutrients"] ["grove"],
			name_or_accepts = ingredient
		)
		
		'''
			starts at:
				walnuts: 5021813355368299589/7036874417766400 713.6425999999999
				vegan pizza: 89531560592125469/2251799813685248 39.760000000000005
		'''	
		'''
			ends with:
				recipe: 7752113592587244929/11258999068426240 688.526
				walnuts: 456528486851663599/70368744177664 6487.66
				vegan pizza: 447657802960627345/562949953421312 795.2
				combined: 4099885697773936137/562949953421312 7282.86
		'''
		print ("recipe amounts:")
		print (
			"	recipe:", 
			find_grams (recipe_ingredient ["measures"]), 
			float (find_grams (recipe_ingredient ["measures"]))
		)
		print (
			"	walnuts:", 
			(find_grams (walnuts_1882785_ingredient ["measures"])),
			float (find_grams (walnuts_1882785_ingredient ["measures"])),
			
		)
		print (
			"	vegan pizza:", 
			(find_grams (vegan_pizza_2672996_ingredient ["measures"])),
			float (find_grams (vegan_pizza_2672996_ingredient ["measures"]))
		)
		print (
			"	combined:", 
			(
				(find_grams (walnuts_1882785_ingredient ["measures"])) +
				(find_grams (vegan_pizza_2672996_ingredient ["measures"]))
			),
			float (
				(find_grams (walnuts_1882785_ingredient ["measures"])) +
				(find_grams (vegan_pizza_2672996_ingredient ["measures"]))
			)
		)
		
		assert (
			find_grams (recipe_ingredient ["measures"]) == (
				(find_grams (walnuts_1882785_ingredient_1 ["measures"]) * walnut_multiplier) +
				(find_grams (vegan_pizza_2672996_ingredient_1 ["measures"]) * vegan_pizza_2672996_multiplier)
			)
		)
	
	
	assert_ingredient ("protein")
	assert_ingredient ("carbohydrates")
	assert_ingredient ("Cholesterol")
	assert_ingredient ("Sodium, Na")
	
checks = {
	"check 1": check_1
}