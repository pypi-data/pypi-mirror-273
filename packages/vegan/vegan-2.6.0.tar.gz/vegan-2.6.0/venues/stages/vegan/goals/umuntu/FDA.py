
'''
	import vegan.goals.umuntu.FDA as FDA_goals_for_umuntu
	goal = FDA_goals_for_umuntu.retrieve ()
'''

'''
	multikey index:
		https://www.mongodb.com/docs/manual/core/indexes/index-types/index-multikey/
'''
def retrieve ():
	return {
	  "label": "FDA goals for the average adult humans",
	  "cautions": [
		#"These guidelines have not been checked by any high status nutritionists.",
		"The goals for each individual adult may vary substantially based on body, lifestyle, and aspirations.",
		"Consulting with your nutritionist or physician is recommended."
	  ],
	  "ingredients": [
		{
		  "labels": [
			"Biotin"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "3/100000",
				  "decimal string": "3.0000e-5"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Calcium"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "13/10",
				  "decimal string": "1.3000e+0"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"calories"
		  ],
		  "goal": {
			"energy": {
			  "per Earth day": {
				"food calories": {
				  "fraction string": "2000",
				  "decimal string": "2.0000e+3"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Choline"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "11/20",
				  "decimal string": "5.5000e-1"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Cholesterol"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "3/10",
				  "decimal string": "3.0000e-1"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Chromium"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "7/200000",
				  "decimal string": "3.5000e-5"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Copper"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "9/10000",
				  "decimal string": "9.0000e-4"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Dietary Fiber"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "28",
				  "decimal string": "2.8000e+1"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Fats"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "78",
				  "decimal string": "7.8000e+1"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Folate",
			"Folic Acid"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "1/2500",
				  "decimal string": "4.0000e-4"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Iodine"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "3/20000",
				  "decimal string": "1.5000e-4"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Iron"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "9/500",
				  "decimal string": "1.8000e-2"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Magnesium"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "21/50",
				  "decimal string": "4.2000e-1"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Manganese"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "23/10000",
				  "decimal string": "2.3000e-3"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Molybdenum"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "9/200000",
				  "decimal string": "4.5000e-5"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Niacin"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "2/125",
				  "decimal string": "1.6000e-2"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Pantothenic Acid"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "1/200",
				  "decimal string": "5.0000e-3"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Phosphorus"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "5/4",
				  "decimal string": "1.2500e+0"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Potassium"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "47/10",
				  "decimal string": "4.7000e+0"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Protein"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "50",
				  "decimal string": "5.0000e+1"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Riboflavin"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "13/10000",
				  "decimal string": "1.3000e-3"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Saturated Fat"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "20",
				  "decimal string": "2.0000e+1"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Selenium"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "11/200000",
				  "decimal string": "5.5000e-5"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Sodium"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "23/10",
				  "decimal string": "2.3000e+0"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Thiamin"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "3/2500",
				  "decimal string": "1.2000e-3"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"carbohydrates"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "275",
				  "decimal string": "2.7500e+2"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Vitamin A"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "9/10000",
				  "decimal string": "9.0000e-4"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Vitamin B6"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "17/10000",
				  "decimal string": "1.7000e-3"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Vitamin B12"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "3/1250000",
				  "decimal string": "2.4000e-6"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Vitamin C"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "9/100",
				  "decimal string": "9.0000e-2"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Vitamin D"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "1/50000",
				  "decimal string": "2.0000e-5"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Vitamin E"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "3/200",
				  "decimal string": "1.5000e-2"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Vitamin K"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "3/25000",
				  "decimal string": "1.2000e-4"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Zinc"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "11/1000",
				  "decimal string": "1.1000e-2"
				}
			  }
			}
		  }
		}
	  ],
	  "limiters": [
		{
		  "label": "species",
		  "includes": [
			"human"
		  ]
		},
		{
		  "kind": "slider--integer",
		  "label": "age",
		  "includes": [
			[
			  "20",
			  "eternity"
			]
		  ]
		},
		{
		  "label": "exclusions",
		  "includes": [
			"pregnant",
			"breast feeding"
		  ]
		}
	  ],
	  "sources": [
		"https://www.fda.gov/food/new-nutrition-facts-label/daily-value-new-nutrition-and-supplement-facts-labels",
		"https://www.fda.gov/food/nutrition-facts-label/calories-nutrition-facts-label",
		"https://www.fda.gov/media/99069/download",
		"https://www.fda.gov/media/99059/download"
	  ]
	}

