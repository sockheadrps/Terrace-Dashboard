<script>
	import { onMount } from "svelte";
    import SettingsNav from "./SettingsNav.svelte";
	import { fade } from 'svelte/transition';
	import { quintInOut } from "svelte/easing";
    let ready = false

    onMount(() => {
        ready=true
    })
</script>

{#if ready}
    <div class="settings__area h-full rounded-md m-2 text-original-muted"
    transition:fade={{easing: quintInOut}}
    >
        <div class="settings__nav pt-5" >
            <SettingsNav />
            <div  class="h-full flex flex-col justify-center " in:fade|local={{delay: 500}}>
                <slot />
            </div>
        </div>
    </div>
{/if}

<style>

.settings__area {
    background: linear-gradient(
        to left top,
         rgba(24, 24, 24, 0.822),
         rgba(15, 15, 15, 0.863)
         );
}
</style>
