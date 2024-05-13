

<script>

/*
	This is the mobile nav?
*/

import { decor } from './decor'
export default decor;

</script>

<template>
	<lounge #default="{ palette, terrain, cart }">
		<nav>
			<router_link_scenery name="controls" :clicked="link_clicked" :style="{ textAlign: 'center' }" />
			<router_link_scenery name="habitat" :clicked="link_clicked" :style="{ textAlign: 'center' }"/>
			<router_link_scenery name="goods" :clicked="link_clicked" :style="{ textAlign: 'center' }"/>
		
			<s_button
				ref="button"
				:pressable="true"
				boundaries="3px 12px 3px"
				:clicked="open_about"
				
				animation="1"
				
				:styles="{
					outside: {
						width: '100%',
					},
					inside: {}
				}"
			>
				about
			</s_button>
			
			<router_link_scenery name="goal" :style="{ textAlign: 'center' }"/>
		
			<router_link_scenery 
				name="grocery list"
				:has_slot="true"
				:clicked="link_clicked"
				:style="{ textAlign: 'center' }"
			>
				<span>grocery list</span>
				<span
					:style="{
						marginLeft: '8px',
						padding: '2px 8px',
						borderRadius: '20px',
					}"
				>{{ cart.IDs.length }}</span>
			</router_link_scenery>
		
			
			<s_button
				ref="button"
				:pressable="true"
				boundaries="3px 12px 3px"
				:clicked="open_physics"
				
				animation="1"
				
				:styles="{
					outside: {
						width: '100%',
					}
				}"
			>
				physics
			</s_button>
			
			
			
		
			<!-- <router_link_scenery name="recipes" :clicked="link_clicked" /> -->
		</nav>
	</lounge>
</template>