

#----
#
#	
import click
import time
#
#
from goodest.adventures.squishy._controls.on import turn_on_squishy
from goodest.adventures.squishy._controls.build import build_squishy
	
#
#----

def squishy_clique ():

	@click.group ("squishy")
	def group ():
		pass

	@group.command ("build")
	def on ():
		build_squishy ()
		return;

	@group.command ("on")
	def on ():
		turn_on_squishy ()
		return;
		
		

	@group.command ("off")
	def off ():
		return;
		
		
	@group.command ("status")
	def on ():
		return;


	return group




#



