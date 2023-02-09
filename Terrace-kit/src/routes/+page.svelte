<script>
    import Search from "$lib/Search.svelte";
    import Weather from "$lib/Weather.svelte";
    import Bookmarks from "$lib/Bookmarks.svelte";
    import Services from "$lib/Services.svelte";

</script>

<div id="main__content" class="grid grid-rows-4 align-top py-5">
    <div class="search__area row-span-1">
        <Search />
    </div>
    <div class="weather__area row-span-1">
        <Weather />
    </div>
    <div class="bookmark__area">
        <Bookmarks />
    </div>
    <div class="service__area">
        <Services />
    </div>

</div>

<style>

.service__area {
    display: flex;
    flex-direction: column-reverse;
}
</style>
