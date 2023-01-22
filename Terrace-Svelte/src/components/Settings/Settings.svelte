<script>
    import SettingsNav from "./SettingsNav.svelte";
    import WeatherSettings from "./WeatherSettings.svelte"
    export let activeSetting = ""
    export let settingsItems = ["Weather"]
    
    const setView = (e) => {
		activeSetting = e.srcElement.innerText
	    }


</script>


<div class="settings__area">
    <div id="settings__nav" >
        <SettingsNav {settingsItems} on:click={setView} />
        {#if (activeSetting == "Weather")}
        <WeatherSettings />
        {/if}
    </div>

</div>


<style>

.settings__area {
    display: grid;
    grid-template-columns: 1fr;
    background: linear-gradient(to right bottom, rgba(10, 6, 24, 0.75), rgba(10, 6, 24, 0.69));
    border-radius: 2rem;
    margin: 2rem;
    color: #808080;
}


</style>