

'''
	addresses_bits ({
		"app": ""
	})
'''

#----
#
from goodest._essence import retrieve_essence
#
from goodest.adventures.sanique.utilities.generate_inventory_paths import generate_inventory_paths
#
#
import vegan_bits_1
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

def addresses_guest_bits (addresses_packet):
	app = addresses_packet ["app"]
	#
	#	
	essence = retrieve_essence ()
	bits_inventory_paths = generate_inventory_paths (
		essence ["bits"] ["sequences_path"]
	)
	#
	#

	bits_addresses = sanic.Blueprint ("bits", url_prefix = "/bits")
	bits_path = vegan_bits_1.sequences ()


	app.static ("/bits", bits_path)

	app.blueprint (bits_addresses)
	
	
	
	''''
		objectives:
			caching
	
		headers = {
			"Cache-Control": "private, max-age=31536000",
			"Expires": "0"
		}
	'''#
	'''
	@bits_addresses.route("/<path:path>")
	async def public_route (request, path):	
		
		try:
			full_path = f"bits/{ path }"
			print ("full_path:", full_path)
			
			if (full_path in bits_inventory_paths):
				content_type = bits_inventory_paths [ full_path ] ["mime"]
				content = bits_inventory_paths [ full_path ] ["content"]
					
				return sanic_response.raw (content, content_type = content_type)
				
			return sanic_response.text ("not found", status = 604)	
		except Exception as E:
			print ("E:", E)
	
		return sanic_response.text ("An anomaly occurred while processing.", status = 600)	
	'''