
/*
	import { open_about } from '@/parcels/about/open.js'
*/

import { append_field } from '@/apps/fields/append'

export async function open_about () {
	await append_field ({
		field_title: "banquet",
		field: import ('@/parcels/about/decor.vue')
	})
}