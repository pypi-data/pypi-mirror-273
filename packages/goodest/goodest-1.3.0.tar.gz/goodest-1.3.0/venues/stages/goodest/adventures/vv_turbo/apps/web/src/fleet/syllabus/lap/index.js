
/*
	import { lap } from '@/fleet/syllabus/lap'
	const { 
		status,
		parsed,
		proceeds
	} = await lap ({
		envelope: {
			label: ""
		}
	});
	if (status !== 200) { 
		
	}
*/



import { assert_equal } from '@/grid/assert/equal'
import { has_field } from '@/grid/object/has_field'


function calc_address () {
	const node_address = localStorage.getItem ("node address")
	if (typeof node_address === "string" && node_address.length >= 1) {
		return node_address
	}

	return "/"
}


var address = calc_address ()


export const lap = async function ({
	method = "PATCH",
	envelope = {},
	path = ""
} = {}) {
	assert_equal (has_field (envelope, "label"), true)
	assert_equal (has_field (envelope, "freight"), true)

	var address_1 = address + path;

	const proceeds = await fetch (address_1, {
		method,
		body: JSON.stringify (envelope)
	});
	
	try {
		const proceeds_JSON = await proceeds.json ();	
		return {			
			status: proceeds.status,
			
			parsed: "yes",			
			proceeds: proceeds_JSON
		}
	}
	catch (exception) {
		console.error (exception)		
	}
	
	
	return {
		status: proceeds.status,
		parsed: "no" 
	}
}