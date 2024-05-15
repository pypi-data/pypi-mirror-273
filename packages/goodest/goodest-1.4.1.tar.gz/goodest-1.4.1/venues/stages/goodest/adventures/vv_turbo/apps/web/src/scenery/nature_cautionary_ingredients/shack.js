
import { round_quantity } from '@/grid/round_quantity'
import { furnish_string } from '@/grid/furnish/string'
import { fraction_to_float } from '@/grid/Fraction/to_float'
import { has_field } from '@/grid/object/has_field'

import nature_ingredients_table from '@/scenery/nature_ingredients_table/fountains.vue'

import cloneDeep from 'lodash/cloneDeep'
import _get from 'lodash/get'

export const shack = {
	props: [ "land" ],
	
	components: {
		nature_ingredients_table
	},
	
	data () {
		return {
			component_opacity: 0,
			condensed: false
		}
	},
	watch: {
		land () {
			// this.show_pie ()
		}
	},
	methods: {
		_get,
		
		/*
		show_pie_without_macros () {
			const land = cloneDeep (this.land);
			
			land.grove = land.grove.filter (ingredient => {
				const filter = [ 
					"protein",
					"carbohydrates",
					"fats"
				].includes (
					ingredient ['info'] ['names'] [0]
				)
				
				// console.log ({ filter })
				
				if (filter) {
					return false;
				}
				
				return true;
			})
			
			
			
			this.$refs.pie_without_macros.show ({
				land
			})
		},
		*/
		
		
		show_pie () {
			return;
			
			/*
			console.log ('show_pie', has_field (this.land, "grove"))
			
			if (has_field (this.land, "grove")) {				
				this.$refs.pie_every.show ({
					land: cloneDeep (this.land)
				})
				
				// this.show_pie_without_macros ()
			}
			*/
		},
		energy_parsed () {
			try {
				return fraction_to_float (
					this.land ["measures"] ['energy'] ['per recipe'] ['food calories'] ['fraction string']
				)
			}
			catch (ex) {}
			
			return ''
		},
		mass_plus_mass_eq_parsed () {
			try {
				return fraction_to_float (
					this.land ["measures"] ['mass + mass equivalents'] ['per recipe'] ['grams'] ['fraction string']
				)
			}
			catch (ex) {}
			
			return ''
		},
		calc_condensed () {
			const layout = this.$refs.layout;
			const { width } = layout.getBoundingClientRect ()
			if (width <= 800) {
				this.condensed = true
			}
			else {
				this.condensed = false;
			}
			
			// console.log ('this.condensed:', this.condensed)
		}
	},
	async mounted () {
		const layout = this.$refs.layout;
		this.RO = new ResizeObserver ((entries, observer) => {
			// console.log ('ResizeObserver:', entries)
			
			this.calc_condensed ()
			
			/*
			for (const entry of entries) {
				const {left, top, width, height} = entry.contentRect;

				console.log('Element:', entry.target);
				console.log(`Element's size: ${ width }px x ${ height }px`);
				console.log(`Element's paddings: ${ top }px ; ${ left }px`);
			}
			*/
		});


		this.calc_condensed ()

		// this.show_pie ()
		
		this.component_opacity = 1;

		this.RO.observe (layout);
	},
	
	beforeUnmount () {
		const layout = this.$refs.layout;
		this.RO.unobserve (layout)
	}
}