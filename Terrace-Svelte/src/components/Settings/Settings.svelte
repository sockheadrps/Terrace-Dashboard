<script>
    import SettingsNav from "./SettingsNav.svelte";
    import WeatherSettings from "./WeatherSettings.svelte"
    import BookmarkSettings from "./Bookmarks/BookmarkSettings.svelte";
    export let activeSetting = "Weather";
    export let settingsItems = ["Weather", "Bookmarks"];

</script>


<div class="settings__area">
    <div id="settings__nav" >
        <SettingsNav bind:activeSetting {settingsItems} />
        {#if (activeSetting == "Weather")}
            <WeatherSettings />
        {/if}
        {#if (activeSetting == "Bookmarks")}
            <BookmarkSettings />
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
