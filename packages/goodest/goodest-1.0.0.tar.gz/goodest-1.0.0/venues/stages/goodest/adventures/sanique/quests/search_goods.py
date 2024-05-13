
'''
	{
		"freight": {
			"filters": {
				"include": {
					"food": true,
					"supp": true
				},
				"limit": 25,
				"string": ""
			}
		}
	}
'''

#----
#
from goodest.adventures.monetary.quests.search_goods import search_goods
#
#
import law_dictionary
#
#----


def check_filters (filters):
	report_filters = law_dictionary.check (
		return_obstacle_if_not_legit = True,
		allow_extra_fields = False,
		laws = {
			"include": {
				"required": True,
				"type": dict
			},
			"limit": {
				"required": True,
				"type": int
			},
			"string": {
				"required": True,
				"type": str
			}
		},
		dictionary = filters 
	)
	
	return report_filters
	
def check_include (filters):
	report_filters = law_dictionary.check (
		return_obstacle_if_not_legit = True,
		allow_extra_fields = False,
		laws = {
			"food": {
				"required": True,
				"type": bool
			},
			"supp": {
				"required": True,
				"type": bool
			}
		},
		dictionary = filters 
	)
	
	return report_filters

def search_goods_quest (packet):

	freight = packet ["freight"]
	
	report_freight = law_dictionary.check (
		return_obstacle_if_not_legit = True,
		allow_extra_fields = True,
		laws = {
			"filters": {
				"required": True,
				"type": dict
			}
		},
		dictionary = freight 
	)
	if (report_freight ["advance"] != True):
		return {
			"label": "unfinished",
			"freight": {
				"description": "",
				"report": report_freight
			}
		}
		
	filters = freight ["filters"]
		
	report_filters = check_filters (filters)
	if (report_filters ["advance"] != True):
		return {
			"label": "unfinished",
			"freight": {
				"obstacle": report_filters,
				"description": "The 'filters' check was not passed.",
			}
		}
	



	report_include = check_include (filters ["include"])
	if (report_filters ["advance"] != True):
		return {
			"label": "unfinished",
			"freight": {
				"description": "The 'include' check was not passed.",
				"obstacle": report_include
			}
		}

	try:
		if ("emblem" in filters):
			filters ["emblem"] = int (filters ["emblem"])
	except Exception:	
		return {
			"label": "unfinished",
			"freight": {
				"description": "The emblem couldn't be converted to an integer.",
				"obstacle number": 4
			}
		}
	

	
	search_proceeds = search_goods ({
		"filters": {
			"string": "",
			"include": {
				"food": True,
				"supp": True
			},
			"limit": 10
		}
	})

	
	return {
		"label": "finished",
		"freight": search_proceeds
	}