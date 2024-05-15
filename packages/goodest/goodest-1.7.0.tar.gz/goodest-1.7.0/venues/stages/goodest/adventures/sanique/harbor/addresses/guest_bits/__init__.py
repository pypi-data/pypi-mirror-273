

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

	
	bits_path = vegan_bits_1.sequences ()

	
		
	if (essence ["mode"] == "business"):
		'''
		bits_inventory_paths = generate_inventory_paths (
			essence ["bits"] ["sequences_path"]
		)
		'''
		'''
			bit_path: RebaSpike--persian-6478261_1920.jpg
			bit_path: galaxy-3608029_1920.jpg
			bit_path: Samuelsp--ai-generated-8440480_1920.png
			bit_path: fajaws--ai-generated-8071034_1920.png
			bit_path: noCapXL--ai-generated-8319806_1920.png
			bit_path: dlsdkcgl--ai-generated-8413076_1920.png
			bit_path: animenex--ai-generated-8294122_1920.png
			bit_path: FelixMittermeier/wheat-2391348_1920.jpg
			bit_path: sink-filter/filter-removal-2.jpg
			bit_path: sink-filter/IMG_20240219_130259315.jpg
			bit_path: sink-filter/clamp-off.jpg
			bit_path: sink-filter/from-right.jpg
			bit_path: sink-filter/filter-cleaning.jpg
			bit_path: sink-filter/filter-removal-1.jpg
			bit_path: sink-filter/counter-2.jpg
			bit_path: sink-filter/clamped.jpg
			bit_path: sink-filter/counter.jpg
			bit_path: sink-filter/dish-washer-inlet.jpg
			bit_path: sink-filter/filter-removal-0.jpg
			bit_path: sink-filter/left-2.jpg
			bit_path: sink-filter/left.jpg
			bit_path: favicons/favicon-1.ico
		'''
		bits_inventory_paths = generate_inventory_paths (bits_path)
		for bit_path in bits_inventory_paths:
			print ("bit_path:", bit_path)
	
	
		bits_addresses = sanic.Blueprint ("bits", url_prefix = "/bits/1")

		
		@bits_addresses.route("/<path:path>")
		async def public_route (request, path):	
			try:
				full_path = f"{ path }"
				
				if (full_path in bits_inventory_paths):
					content_type = bits_inventory_paths [ full_path ] ["mime"]
					content = bits_inventory_paths [ full_path ] ["content"]
					
					'''
						possibly: SHA for caching
							maybe better: sequential addresses for caching
					'''						
					return sanic_response.raw (
						content, 
						content_type = content_type,
						headers = {
							"Cache-Control": "private, max-age=31536000",
							"Expires": "0"
						}
					)
				
				return sanic_response.json ({
					"summary": "bits not found"
				}, status = 604)
				
			except Exception as E:
				print ("E:", E)
		
			return sanic_response.text ("An anomaly occurred while processing.", status = 600)	


		app.blueprint (bits_addresses)
	else:
		app.static ("/bits/1", bits_path)
	
	
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