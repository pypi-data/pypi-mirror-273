

'''
	itinerary:
		[ ] pass the current python path to this procedure
'''


'''
	https://sanic.dev/en/guide/running/manager.html#dynamic-applications
'''

'''
	worker manager:
		https://sanic.dev/en/guide/running/manager.html
'''

'''
	Asynchronous Server Gateway Interface, ASGI:
		https://sanic.dev/en/guide/running/running.html#asgi
		
		uvicorn harbor:create
'''

'''
	Robyn, rust
		https://robyn.tech/
'''

'''
	--factory
'''

#----
#
''''
	addresses
"'''
#
from .sockets_guest import sockets_guest
#
from .addresses.staff import addresses_staff
from .addresses.staff.besties__food_USDA__nature_v2__FDC_ID import besties__food_USDA__nature_v2__FDC_ID
from .addresses.staff.besties__supp_NIH__nature_v2__DSLD_ID import besties__supp_NIH__nature_v2__DSLD_ID
from .addresses.staff_goodest_inventory.foods import addresses_foods
from .addresses.staff_goodest_inventory.supps import addresses_supps
from .addresses.staff_goodest_inventory.recipes import addresses_staff_goodest_inventory_recipes
#
from .addresses.guest import addresses_guest
from .addresses.guest_bits import addresses_guest_bits
from .addresses.guest_goodest_inventory.recipes import addresses_guest_recipes
from .addresses.guest_goodest_inventory.foods import addresses_guest_foods
from .addresses.guest_goodest_inventory.supps import addresses_guest_supps
#
from goodest.adventures.sanique.utilities.generate_inventory_paths import generate_inventory_paths
#
from goodest._essence import retrieve_essence, build_essence
from goodest.adventures.alerting import activate_alert
from goodest.adventures.alerting.parse_exception import parse_exception
#
from goodest.adventures.monetary.DB.goodest_tract.goals.retrieve_one import retrieve_one_goal

from goodest.besties.supp_NIH.nature_v2._ops.retrieve import retrieve_parsed_NIH_supp
from goodest.shows_v2.recipe._ops.retrieve import retrieve_recipe
from goodest.shows_v2.recipe_with_goals._ops.formulate import formulate_recipe_with_goals	
#
#
from biotech.topics.show.variable import show_variable
#
#
import sanic
from sanic import Sanic
from sanic_ext import openapi
#from sanic_openapi import swagger_blueprint, openapi_metadata
#from sanic_openapi import swagger_blueprint, doc
import sanic.response as sanic_response
#
#
import json
import os
import traceback
#
#----

'''
	https://sanic.dev/en/guide/running/running.html#using-a-factory
'''
def create ():
	USDA_food_ellipse = os.environ.get ('USDA_food')
	NIH_supp_ellipse = os.environ.get ('NIH_supp')
	inspector_port = os.environ.get ('inspector_port')
	env_vars = os.environ.copy ()
	
	essence = retrieve_essence ()
	
	
	'''
		#
		#	https://sanic.dev/en/guide/running/configuration.html#inspector
		#
		INSPECTOR_PORT
	'''
	
	app = Sanic (__name__)
	
	app.extend (config = {
		"oas_url_prefix": "/docs",
		"swagger_ui_configuration": {
			"docExpansion": "list" # "none"
		}
	})
	
	#app.blueprint(swagger_blueprint)
	app.config.INSPECTOR = True
	app.config.INSPECTOR_HOST = "0.0.0.0"
	app.config.INSPECTOR_PORT = int (inspector_port)
	
	#
	#	opener
	#
	#
	#app.ext.openapi.add_security_scheme ("api_key", "apiKey")
	app.ext.openapi.add_security_scheme ("api_key", "http")
	

	
	
	#----
	#
	#	Guests 
	#
	#----
	addresses_guest_bits ({
		"app": app,
	})
	addresses_guest ({
		"app": app
	})
	
	#
	#	recipes
	#
	#
	addresses_guest_recipes ({
		"app": app
	})
	addresses_guest_foods ({
		"app": app
	})
	addresses_guest_supps ({
		"app": app
	})

	#----
	#
	#	Staff 
	#
	#----
	staff_addresses = sanic.Blueprint ("staff", url_prefix = "/staff")
	#
	#	staff foods
	#
	#
	foods_addresses = sanic.Blueprint (
		"staff_foods", 
		url_prefix = "/staff/foods"
	)
	addresses_foods ({
		"app": app,
		"blueprint": foods_addresses
	})
	app.blueprint (foods_addresses)
	
	
	#
	#	staff supps
	#
	#
	supps_addresses = sanic.Blueprint (
		"staff_supps", 
		url_prefix = "/staff/supps"
	)
	addresses_foods ({
		"app": app,
		"blueprint": supps_addresses
	})
	app.blueprint (supps_addresses)
	

	
	
	
	#
	#	recipes
	#
	#
	app.blueprint (addresses_staff_goodest_inventory_recipes ({
		"app": app
	}))
	
	
	#
	#
	#
	#
	addresses_staff ({
		"app": app,
		"staff_addresses": staff_addresses
	})
	
	
	
	'''
		 https://sanic.dev/en/plugins/sanic-ext/openapi/decorators.html#ui
	'''
	besties__food_USDA__nature_v2__FDC_ID ({
		"app": app,
		"openapi": openapi,
		"USDA_food_ellipse": USDA_food_ellipse,
		"staff_addresses": staff_addresses
	})
	
	besties__supp_NIH__nature_v2__DSLD_ID ({
		"app": app,
		"openapi": openapi,
		"NIH_supp_ellipse": NIH_supp_ellipse,
		"staff_addresses": staff_addresses
	})
	
	
	
	app.blueprint (staff_addresses)
	

		
	return app

