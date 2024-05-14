


def floating_process (procedure, CWD, env):
	show_variable ("procedure:", procedure)
	process = subprocess.Popen (
		procedure, 
		cwd = CWD,
		env = env
	)
	
	pid = process.pid
	
	show_variable ("sanic pid:", pid)
	
def turn_on_sanique (packet = {}):
	essence = retrieve_essence ()



	process = floating_process (
		procedure = [
			"nft"
		],
		CWD = harbor_path,
		env = env_vars
	)
	
	
	loop = 0
	while True:
		show_variable ("checking sanique status")
	
		the_status = check_sanique_status ()
		if (the_status == "on"):
			break;
		
		time.sleep (1)

		loop += 1
		if (loop == 20):
			raise Exception ("Sanique doesn't seem to be turning on.")

	return;