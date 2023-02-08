<script>
	import { onMount } from "svelte";
    import SettingsNav from "./SettingsNav.svelte";

    onMount(() => console.log("fuck"))
</script>


<div class="settings__area">
    <div id="settings__nav" >
        <SettingsNav />
        <slot />
    </div>
</div>


<style>

.settings__area {
    display: grid;
    grid-template-columns: 1fr;
    background: linear-gradient(
        to left top,
         rgba(24, 24, 24, 0.822),
         rgba(15, 15, 15, 0.863)
         );
    border-radius: 2rem;
    margin: 2rem;
    color: #808080;
}


</style>
