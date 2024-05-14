

<script>

import { decor } from './decor'
export default decor;

</script>

<template>
	<lounge #default="{ palette, terrain }">
		<article v-if="show_goal">
			<div
				:style="{
					display: 'flex',
					justifyContent: 'space-between',
					alignItems: 'center'
				}"
			>
				<h1
					:style="{
						fontWeight: 'bold'
					}"
				>{{ find_label () }}</h1>
				<s_button
					v-if="show_pick"
				
					:clicked="pick_goal"
					boundaries="8px 32px"
				>pick</s_button>
			</div>
			
			<s_line :style="{ margin: '10px 0' }" />
			
			<div>
				<h2 :style="{ textAlign: 'center' }">caution</h2>
				<div 
					v-for="caution in furnish_array (goal, [ 'nature', 'cautions'], [])"
					:style="{}"
				>
					<p>{{ caution }}</p>
				</div>
			</div>
			
			<s_line :style="{ margin: '10px 0' }" />
			
			<div>
				<h2 :style="{ textAlign: 'center' }">audience</h2>
				
				<div 
					v-for="limiter in furnish_array (goal, [ 'nature', 'limiters'], [])"
					:style="{
						display: 'flex',
						alignItems: 'center',
						
						boxSizing: 'border-box',
						padding: '4px 0',
						//justifyContent: 'space-between'
					}"
				>	
					<div
						:style="{
							width: '100px'
						}"
					>
						<div
							:style="{
								display: 'inline-block',
								position: 'relative',
								
								padding: '4px 8px',
								border: '1px solid ' + palette [6],
								borderRadius: '4px'
							}"
						>
							<s_curtain />
							<p
								:style="{
									position: 'relative',
									margin: 0,
								}"
							>{{ furnish_string (limiter, 'label', '') }}</p>
						</div>
					</div>
					
					<div
						:style="{
							paddingLeft: '10px'
						}"
					>
						<p 
							v-for="(include, index) in furnish_array (limiter, [ 'includes' ], [])"
							:style="{
								paddingRight: '4px'
							}"
						>
							<span v-if="typeof include === 'string'">
								<span>{{ include }}</span>
							</span>
							
							<span v-else-if="Array.isArray (include)"
								:style="{
									display: 'inline-flex'
								}"
							>
								<span>{{ include [0] }}</span>
								<span :style="{ padding: '0 4px' }">to</span>
								<span>{{ include [1] }}</span>
							</span>
							
							<span v-else>
								<span>{{ include }}</span>
							</span>
							
							<span
								v-if="index != furnish_array (limiter, [ 'includes' ], []).length - 1"
							>,</span>
						</p>
					</div>
				</div>
			</div>
			
			<s_line :style="{ margin: '10px 0' }" />
			
			<div>
				<h2 :style="{ textAlign: 'center' }">goals</h2>
				<div 
					v-for="ingredient in furnish_array (goal, [ 'nature', 'ingredients'], [])"
					:style="{
						display: 'flex',
						justifyContent: 'space-between',
						maxWidth: '800px',
						borderBottom: '1px solid ' + palette[2]
					}"
				>
					<div>
						<span 
							v-for="(label, index) in furnish_array (ingredient, [ 'labels'], [])"
							:style="{}"
						>
							<span>{{ label }}</span>
							<span 
								v-if="index + 1 != furnish_array (ingredient, [ 'labels'], []).length"
								:style="{
									marginRight: '4px'
								}"
							>,</span>
						</span>
					</div>
					
					<div
						:style="{
							display: 'flex'
						}"
					>
						<component :is="find_goal_amount ({ ingredient })" />
					</div>
				</div>
			</div>
			
			
		</article>
	</lounge>
</template>