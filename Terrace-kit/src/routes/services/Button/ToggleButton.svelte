<script lang="ts">
	import { websocketSend } from "$lib/stores";
	import { fade } from "svelte/transition";
    export let OniconName: undefined | string
    export let OfficonName: undefined | string
    import Icon from "@iconify/svelte";
    export let buttonOnCommand: boolean 
    export let buttonOffCommand: boolean
    export let name: undefined | string
    export let toggled = false
    export let commandType: undefined | string

    function handleClick(){
        toggled = !toggled
        if (toggled) {
            websocketSend("SERVICE-DATA", {'TARGET-CLIENT': "Twitch", "COMMAND": commandType, "value": buttonOffCommand})
            console.log(buttonOffCommand)
        }

        else {
            console.log(buttonOnCommand)
            websocketSend("SERVICE-DATA", {'TARGET-CLIENT': "Twitch", "COMMAND": commandType, "value": buttonOnCommand})
        }
    }

</script>

<button class="flex flex-col items-center h-32 w-32 m-2 bg-original-card-bg-dark text-original-muted p-2
    rounded-md transition-colors hover:text-original-muted-hover 
    hover:bg-original-service-dark text-center " on:click|preventDefault={() => handleClick()}>
    {#if !toggled}
        <div class="absolute mt-2 text-7xl text-center m-1" in:fade={{ delay: 250, duration: 250 }} out:fade={{ duration: 250 }}>
            <Icon icon={OniconName} />
        </div>
        
    {:else}
        <div class="absolute mt-2 text-7xl text-center m-1" in:fade={{ delay: 250, duration: 250 }} out:fade={{ duration: 250 }}>
            <Icon icon={OfficonName} />
        </div>
    {/if}
        <div class="h-full flex flex-col-reverse">
            <div class="text-xl">
                {name}
            </div>
        </div>
</button>