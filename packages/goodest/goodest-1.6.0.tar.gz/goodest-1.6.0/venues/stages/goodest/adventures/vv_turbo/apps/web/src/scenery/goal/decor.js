
import { furnish_string } from 'procedures/furnish/string'
import { furnish_array } from 'procedures/furnish/array'

import { open_goal } from '@/parcels/goal/open.js'
import s_curtain from '@/scenery/curtain/decor.vue'

import { defineComponent, h } from 'vue';
import goal_amount from './components/goal_amount.vue'

export const decor = {
	components: { s_curtain },
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
		
		pick_goal () {
			this.pick ({ goal: this.goal })
		},
		
		find_includes () {
			try {
				return this.goal.nature.label;
			}
			catch (exception) {
				
			}
			
			return {}
		},
		
		find_goal_amount ({ ingredient }) {
			const exceptions = []
			
			try {
				const grams = ingredient.goal [
					"mass + mass equivalents"
				] ["per Earth day"] ["grams"] ["decimal string"]
				
				return h (goal_amount, { 
					grams
				})
			}
			catch (exception) {
				exceptions.push (exception)
			}
			
			try {
				return h (goal_amount, { 
					food_calories: ingredient.goal [
						"energy"
					] ["per Earth day"] ["food calories"] ["decimal string"]
				})
			}
			catch (exception) {
				exceptions.push (exception)
			}
			
			console.error ({
				ingredient,
				exceptions
			})
			
			return h (goal_amount, { food_calories: ingredient })
		},
		
		find_goal () {
			
			try {
				return this.goal.nature.label;
			}
			catch (exception) {
				
			}
			
			return {}
		},
		
		find_label () { 
			try {
				return this.goal.nature.label;
			}
			catch (exception) {
				
			}
			
			return ''
		}
	}
}