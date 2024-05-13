

<script>

import { furnish_string } from 'procedures/furnish/string'
import { furnish_array } from 'procedures/furnish/array'

export default {
	props: {
		goal: Object,
		show_goal: {
			type: Boolean,
			default: false
		},
		
		pick: {
			default () {}
		},
		show_pick: {
			type: Boolean,
			default: false
		}
	},
	methods: {			
		furnish_string,
		furnish_array,
		
		find_label () { 
			return furnish_string (this.goal, [ 'nature', 'label' ], '') 
		}
	}
}

</script>

<template>
	<article v-if="show_goal">
		<!-- <div
			:style="{
				display: 'flex',
				justifyContent: 'space-between',
				alignItems: 'center'
			}"
		>
			<h1>{{ find_label () }}</h1>
			<s_button
				v-if="show_pick"
			
				:clicked="pick (goal)"
				boundaries="8px 32px"
			>pick</s_button>
		</div>
		
		<div>
			<h2>caution</h2>
			<div 
				v-for="caution in furnish_array (goal, [ 'nature', 'cautions'], [])"
				:style="{}"
			>
				<p>{{ caution }}</p>
			</div>
		</div>
		
		<div>
			<h2>goals</h2>
			<div 
				v-for="ingredient in furnish_array (goal, [ 'nature', 'ingredients'], [])"
				:style="{}"
			>
				<div 
					v-for="label in furnish_array (ingredient, [ 'labels'], [])"
					:style="{}"
				>
					<h3>{{ label }}</h3>
				</div>
				
				<div
					:style="{
						display: 'flex'
					}"
				>
					<p>{{ ingredient.goal [0] }}</p>
					<p>{{ ingredient.goal [1] }}</p>
				</div>
			</div>
		</div>
		
		<div>
			<h2>audience</h2>
			<div 
				v-for="limiter in furnish_array (goal, [ 'nature', 'limiters'], [])"
				:style="{}"
			>	
				<h2>{{ furnish_string (limiter, 'label', '') }}</h2>
				
				
				<div 
					v-for="include in furnish_array (limiter, [ 'includes' ], [])"
					:style="{}"
				>
					<p>{{ include }}</p>
				</div>
			</div>
		</div> -->
	</article>
</template>