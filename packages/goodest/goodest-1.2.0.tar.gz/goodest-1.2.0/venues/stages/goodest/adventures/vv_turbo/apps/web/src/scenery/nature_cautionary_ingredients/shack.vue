





<script>

/*
	import cautionary_ingredients from '@/scenery/nature_cautionary_ingredients/shack.vue'
	<cautionary_ingredients 
		:land=""
	/>

*/

import { shack } from './shack'
export default shack;

</script>


<template>
	<lounge #default="{ palette, terrain }">	
		<s_panel
			:style="{
				opacity: component_opacity
			}"
		>
			<header
				:style="{
					margin: '0 auto',
					maxWidth: '800px',
					paddingBottom: '50px'
				}"
			>
				<h2
					:style="{
						textAlign: 'center',
						marginBottom: '20px'
					}"
				>cautionary ingredients</h2>
				
				<p>
					Ingredients in this list might have adverse health effects.
				</p>
				<p>
					Empty rows indicate that no data was found.
				</p>
			</header>	
			
			
			<div
				:style="{
					margin: '0 auto',
					maxWidth: '900px',
					width: '100%',
					
					textAlign: 'center'
				}"
			>
				<s_line :style="{ margin: '10px 0' }" />
			
				<h3>sums</h3>
			
				<div
					:style="{
						display: 'flex',
						justifyContent: 'space-between'
					}"
				>
					<div
						:style="{
							width: '50%'
						}"
					>
						<h3 :style="{ margin: 0, fontSize: '.8em' }">food calories</h3>
						<p :style="{ margin: 0 }">{{ this.energy_parsed () }}</p>
					</div>
					
					<div
						:style="{
							width: '50%'
						}"
					>
						<h3 :style="{ margin: 0, fontSize: '.8em' }">mass + mass equivalents</h3>
						<p :style="{ margin: 0 }">{{ this.mass_plus_mass_eq_parsed () }}</p>
					</div>
				</div>
				
				<s_line :style="{ margin: '10px 0' }" />
			</div>
			
			
			<div
				ref="layout"
				:style="{
					display: 'flex',
					flexDirection: condensed ? 'column-reverse' : 'row',
					justifyContent: 'center',
					
					margin: '0 auto',
					maxWidth: '900px'
				}"
			>
				<div
					:style="{
						display: 'flex',
						flexGrow: 2,
						
						boxSizing: 'border-box',
						width: condensed ? '100%' : 'auto',
						minWidth: '500px',
						minHeight: '100px',
						
						justifyContent: condensed ? 'center' : 'left',
						padding: '.125in'
					}"
				>
					<nature_ingredients_table
						:grove="_get (land, 'grove', '')"
						table_kind="CI"
					/>
				</div>
			</div>
		</s_panel>
	</lounge>
</template>