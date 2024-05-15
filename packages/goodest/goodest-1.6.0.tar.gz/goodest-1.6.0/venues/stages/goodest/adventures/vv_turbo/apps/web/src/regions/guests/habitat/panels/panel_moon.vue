





<script>

import mural from '@/scenery/name/mural.vue'

export default {
	components: { mural },
	props: [],
	
	data () {
		return {
			// 
			homestead: `url("\/bits/1\/fajaws--ai-generated-8071034_1920.png")`,
			
			moon: `url("\/bits/1\/pexels-min-an-713664.jpg")`,
			scifi_metropolis: `url("\/bits/1\/ThankYouFantasyPictures\/ai-generated-7801845_1920.jpg")`,
			scifi_metropolis_2: `url("\/bits/1\/ThankYouFantasyPictures\/ai-generated-8275890_1920.jpg")`,
			
			text: `Research suggests that every essential nutrient can be found in plants, fungi, or algae.`
		}
	}
}

</script>


<template>
	<lounge #default="{ palette, style, terrain }">
		<s_panel
			:style="Object.assign ({}, {
				// height: '100%',
				minHeight: '120vh',
				fontSize: terrain.width <= terrain.mobile_nav_width ? '.7em' : '1em'
			}, style)"
			:board_physics="{
				// height: '100%',
				minHeight: '120vh',
			}"
		>		
			<main
				:style="{
					display: 'flex',
					
					position: 'relative',
					top: 0,
					left: 0,

					boxSizing: 'border-box',
					minHeight: '120vh',
					height: '100%',
					width: '100%',
					padding: '.5in 0',
					
					textAlign: 'center',
					
					color: 				palette [2],
					transition: [
						'color ' 	  + palette.change_duration,
						'border '     + palette.change_duration,
					].join (', '),
				}"
			>	
				<div
					:style="{
						position: 'absolute',
						top: '0',
						left: '50%',
						transform: 'translateX(-50%)',
						
						height: '100%',
						width: '100%',
						maxWidth: '1600px',
						
						backgroundRepeat: 'no-repeat',
						backgroundSize: 'cover',
						backgroundColor: 'white',						
					}"
				></div>
			
				<div
					:style="{
						position: 'absolute',
						top: '0',
						left: '50%',
						transform: 'translateX(-50%)',
						
						height: '100%',
						width: '100%',
						maxWidth: '1600px',
						
						backgroundImage: homestead,
						backgroundPosition: '23% 75%',
						backgroundRepeat: 'no-repeat',
						backgroundSize: 'cover',
						
						opacity: 1
					}"
				></div>
				
				<section
					:style="{
						textAlign: 'left',
						
						position: 'absolute',
						left: '40px',
						top: '10px',
						
						marginTop: '12px',
						
						
						
						maxWidth: 'calc(100% - 70px)'
					}"
				>
					<div>
						<p
							:style="{
								display: 'inline-block',
								
								background: palette [1],
								border: '2px solid ' + palette [6],
								borderRadius: '4px',
								padding: '8px',
								
								fontSize: '1.1em',
								
								marginBottom: '10px'
							}"
						>This site might be utilizing non-vegan electricity generated from dinos that have passed on.</p>
					</div>
					<p
						:style="{
							display: 'inline-block',
							
							background: palette [1],
							border: '2px solid ' + palette [6],
							borderRadius: '4px',
							padding: '8px',
							
							fontSize: '1.1em'
						}"
					>Research on solar, wind, hydro, etc. is in progress.</p>
				</section>
				
				<article
					:style="{
						display: 'flex',
						flexDirection: 'column',
						justifyContent: 'center',
						
						position: 'relative',
						// top: '50%',
						left: '50%',
						// transform: 'translateX(-50%) translateY(-50%)',
						transform: 'translateX(-50%)',
						
						maxWidth: '800px',
						width: '95%',
						//paddingTop: '3in'
					}"
				>
					<section
						:style="{
							background: palette [1],
							border: '2px solid ' + palette [6],
							borderRadius: '4px',
							padding: '8px'
						}"
					>
						<h2
							:style="{
								fontSize: '5em'
							}"
						>Homesteads</h2>
					</section>
					<section
						:style="{
							marginTop: '12px',
							
							background: palette [1],
							border: '2px solid ' + palette [6],
							borderRadius: '4px',
							padding: '8px'
						}"
					>
						<p
							:style="{
								fontSize: '3em'
							}"
						>{{ text }}</p>
					</section>
					
					
				</article>
			</main>
		</s_panel>
	</lounge>
</template>

