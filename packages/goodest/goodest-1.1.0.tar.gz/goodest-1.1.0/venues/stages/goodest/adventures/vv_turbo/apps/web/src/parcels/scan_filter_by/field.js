


	
import { inject } from 'vue'
import s_select from '@/scenery/select/decor.vue'

	

export const field = {
	components: {
		s_select
	},
	data () {
		return {
			affiliate_link_option: "either",
			affiliate_link_options: [
				"yes",
				"yes & no",
				"no"
			]
		}
	},
	methods: {
		affiliate_link_option_changed (option) {
			console.log (option.value)
			
			this.affiliate_link_option = option.value;
		}
	},
	
	created () {	
		const coodinate = inject ('the_coordinate')
		console.log ("field coordiante:", coodinate)
	
		const system = inject ('system');
		console.log ({ system })
	},
	beforeUnmount () {}	
}