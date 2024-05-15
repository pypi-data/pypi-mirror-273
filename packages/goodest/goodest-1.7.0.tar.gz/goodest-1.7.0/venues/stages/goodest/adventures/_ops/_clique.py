

#----
#
from goodest.adventures._ops.on import turn_on
from goodest.adventures._ops.off import turn_off
from goodest.adventures._ops.refresh import refresh
from goodest.adventures._ops.status import check_status
#
#
from ..monetary._ops._clique import monetary_clique
from ..squishy._controls._clique import squishy_clique
from ..demux_hap._controls._clique import demux_hap_clique
#
#
import click
#
#----

def adventures_clique ():
	@click.group ("adventures")
	def group ():
		pass


	
	
	#
	#	goodest on
	#
	@group.command ("on")
	def on ():		
		turn_on ()

	
	@group.command ("off")
	def off ():
		turn_off ()

	@group.command ("refresh")
	def refresh_op ():
		refresh ()

	@group.command ("status")
	def status ():
		check_status ()

	group.add_command (monetary_clique ())
	group.add_command (squishy_clique ())
	group.add_command (demux_hap_clique ())


	return group




#



