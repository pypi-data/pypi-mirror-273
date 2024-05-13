

#----
#
from goodest._essence import retrieve_essence
#
from .vue import vue_regions
#
#
import law_dictionary
#
#
import sanic
from sanic import Sanic
from sanic_ext import openapi
import sanic.response as sanic_response
from sanic_limiter import Limiter, get_remote_address
#from sanic.response import html
#
#
import json
from os.path import exists, dirname, normpath, join
from urllib.parse import unquote
#
#----

from goodest.adventures.sanique.quests.retrieve_food import retrieve_food_quest
from goodest.adventures.sanique.quests.retrieve_supp import retrieve_supp_quest
from goodest.adventures.sanique.quests.search_goods import search_goods_quest
quests = {
	"retrieve food": retrieve_food_quest,
	"retrieve supp": retrieve_supp_quest,
	
	"search goods": search_goods_quest,
	
}

def addresses_guest (addresses_packet):
	essence = retrieve_essence ()
	
	app = addresses_packet ["app"]

	guest_addresses = sanic.Blueprint ("guest", url_prefix = "/")

	@guest_addresses.websocket ('/ws')
	async def address_ws_handler(request, ws):
		while True:
			data = await ws.recv ()  # Receive data from the client
			await ws.send (f"Echo: {data}")  # Send the received data back to the client
		
		
	@guest_addresses.route ("/guests", methods = [ "patch" ])
	async def address_guests (request):
		essence = retrieve_essence ()
		
		try:
			dictionary = request.json
			print ("dictionary:", dictionary)
			
		except Exception:
			return sanic.json ({
				"label": "unfinished",
				"freight": {
					"description": "The body could not be parsed."
				}
			})
		
		report_1 = law_dictionary.check (
			return_obstacle_if_not_legit = True,
			allow_extra_fields = False,
			laws = {
				"label": {
					"required": True,
					"type": str
				},
				"freight": {
					"required": True,
					"type": dict
				}
			},
			dictionary = dictionary 
		)
		if (report_1 ["advance"] != True):
			return sanic.json ({
				"label": "unfinished",
				"freight": {
					"description": "The packet check was not passed.",
					"report": report_1
				}
			}, status = 600)
		
		label = dictionary ["label"]		
		if (label not in quests):
			return sanic.json ({
				"label": "unfinished",
				"freight": {
					"description": 'A quest with that "label" was not found.',
					"report": report_1
				}
			}, status = 600)
		
		proceeds = quests [label] ({
			"freight": dictionary ["freight"]
		})
		return sanic.json (proceeds, status = 200)
			
			
	vue_regions ({
		"app": app,
		"guest_addresses": guest_addresses
	})
	
	app.blueprint (guest_addresses)