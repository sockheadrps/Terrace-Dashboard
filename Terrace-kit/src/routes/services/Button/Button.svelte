<script lang="ts">
	import { websocketSend } from "$lib/stores";
    export let iconName: undefined | string
    import Icon from "@iconify/svelte";
    export let buttonCommand: undefined | string
    export let name: undefined | string

    $: {
        console.log(buttonCommand, iconName)
    }

    function handleClick(){
        console.log('click')
        websocketSend("SERVICE-DATA", {'TARGET-CLIENT': "Controller", "COMMAND": buttonCommand})
    }

</script>

<button class="h-32 m-2 bg-original-card-bg-dark text-original-muted p-2
    rounded-md transition-colors hover:text-original-muted-hover 
    hover:bg-original-service-dark text-center" on:click|preventDefault={() => handleClick()}>
        <div class="text-7xl text-center m-1">
            <Icon icon={iconName} />
        </div>
        <div class="text-center">
            {name}
        </div>
</button>