
<script>

import mural from '@/scenery/name/mural.vue'

export default {
	components: { mural },
	props: [],
	
	data () {
		return {
			// 
			farmscape: `url("\/bits\/dlsdkcgl--ai-generated-8413076_1920.png")`,
			
			beans: `url("\/bits\/arielnunezg\/string-bean-3861864_1920.jpg")`,
			text: `Vegan foods provide healthy sources of enthusiasm, agility, and strength.`,
			text2: `B12 supplements and Omega 3, 6, 9 supplements are usually recommended for vegan diets.`,
			text3: `A vegan multivitamin is usually recommended as well.`
		}
	}
}

</script>


<template>
	<lounge #default="{ palette, style, terrain }">
		<s_panel
			:style="Object.assign ({}, {
				minHeight: '100vh',
				fontSize: terrain.width <= terrain.mobile_nav_width ? '.7em' : '1em'
			}, style)"
			:board_physics="{
				minHeight: '100vh',
			}"
		>		
			<main
				:style="{
					display: 'flex',
					
					position: 'relative',
					top: 0,
					left: 0,

					boxSizing: 'border-box',
					minHeight: '100vh',
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
						
						backgroundImage: farmscape,
						backgroundPosition: '23% 75%',
						backgroundRepeat: 'no-repeat',
						backgroundSize: 'cover',
						
						opacity: .57
					}"
				></div>
				
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
						width: '95%'
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
						>Health</h2>
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
								fontSize: '1.5em'
							}"
						>{{ text2 }}</p>
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
								fontSize: '1.5em'
							}"
						>{{ text3 }}</p>
					</section>
				</article>
			</main>
		</s_panel>
	</lounge>
</template>

