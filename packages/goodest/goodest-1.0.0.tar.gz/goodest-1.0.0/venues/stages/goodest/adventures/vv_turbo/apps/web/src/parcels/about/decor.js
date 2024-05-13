

import s_input from '@/scenery/input/decor.vue'
import s_button from '@/scenery/button/decor.vue'
import s_line from '@/scenery/line/decor.vue'
import s_outer_link from '@/scenery/link/outer/decor.vue'
		
	
export const decor = {
	components: { s_outer_link, s_input, s_button, s_line },
	data () {
		return {
			correspondance: ''
		}
	},
	methods: {
		send () {
			
		}
	},
	mounted () {
		let script = document.createElement('script')
		script.setAttribute('src', 'https://js.stripe.com/v3/buy-button.js')
		this.$refs['crate-script'].appendChild(script)
	}
}