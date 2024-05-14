




<script>

import { field } from './field.js'
export default field

</script>


<template>
	<lounge #default="{ palette, terrain }">
		<div
			:style="{
				padding: '10%'
			}"
		>
			<h1
				:style="{
					color: palette [2],
					transition: [
						'color ' + palette.change_duration,
					].join (', '),
					
					margin: '10px auto',
					textAlign: 'center'
				}"
			></h1>
			
			<s_select 
				name="has affiliate link"
				:preselected_option="affiliate_link_option"
				:options="affiliate_link_options"
				:change="affiliate_link_option_changed"
			/>	
		</div>
	</lounge>
</template>
