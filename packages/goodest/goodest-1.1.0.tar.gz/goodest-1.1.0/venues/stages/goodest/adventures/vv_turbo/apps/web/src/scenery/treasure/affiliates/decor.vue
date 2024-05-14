

<script>

import { furnish_string } from 'procedures/furnish/string'
import s_outer_link from '@/scenery/link/outer/decor.vue'
import s_button from '@/scenery/button/decor.vue'
	
		
export default {
	components: { s_outer_link, s_button },
	props: {
		affiliates: Array
	},
	methods: {
		furnish_string
	}
}


</script>

<template>
	<lounge #default="{ palette }">
		<h2
			:style="{
				textAlign: 'center',
			}"
		>affiliate sources</h2>
		
		<div v-for="affiliate in affiliates">
			<s_button
				ref="button"
				:pressable="true"
				boundaries="3px 12px 3px"
				:clicked="() => {}"
				:styles="{
					inside: {
						
					}
				}"
			>
				<s_outer_link 
					:new_tab="true"
					:address="furnish_string (affiliate, 'link', '')" 
					:style="{
						color: palette [1]
					}"
					:text="furnish_string (affiliate, 'name', '')"
				/>
			</s_button>
		</div>
		
		<div v-if="affiliates.length === 0"
			:style="{
				textAlign: 'center',
				height: '100%',
				paddingTop: '5px',
				boxSizing: 'border-box'
			}"
		>
			not found
		</div>
	</lounge>
</template>