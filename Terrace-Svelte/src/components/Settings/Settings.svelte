<script>
    import SettingsNav from "./SettingsNav.svelte";
    import WeatherSettings from "./WeatherSettings.svelte"
    export let activeSetting = "";
    export let settingsItems = ["Weather"];

    // Tracks active settings tab for switching between settings scope
    const setView = (e) => {
        activeSetting = e.srcElement.innerText;
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
