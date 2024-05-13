

'''
	objectives:
		[ ] 
'''


#----
#
import sanic
from sanic import Sanic
from sanic_ext import openapi
import sanic.response as sanic_response
#
#
from goodest._essence import retrieve_essence, build_essence
from goodest.adventures.sanique.utilities.check_key import check_key
from goodest.adventures.monetary.DB.goodest_inventory.foods.document.insert import insert_food	
#
#----

def addresses_foods (packet):
	blueprint = packet ["blueprint"]

	@blueprint.route ("/insert_1")
	#@openapi.parameter ("opener", str, "header")
	async def address_food_insert (request):
		essence = retrieve_essence ()

		lock_status = check_key (request)
		if (lock_status != "unlocked"):
			return lock_status
		
		insert_food ({
			"FDC_ID": "",
			"affiliates": [],
			"goodness_certifications": []
		})
		
