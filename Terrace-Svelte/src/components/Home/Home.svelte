<script>
    import Search from "./Search.svelte";
    import Weather from "./Weather.svelte";
    import Bookmarks from "./Bookmarks.svelte";
    import Services from "./Services.svelte";

</script>

<div id="main__content">
    <div class="top__spacer"></div>
    <div class="search__area">
        <Search />
    </div>
    <div class="weather__area">
        <Weather />
    </div>
    <div class="bookmark__area">
        <Bookmarks />
    </div>
    <div class="service__area">
        <Services />
    </div>
    <div class="bottom__spacer"></div>

</div>

<style>
#main__content{
    grid-column-start: 2;
    display: grid;
    grid-template-rows: 5% 10% 25% 25% 33%;
    align-items: top;
}

.top__spacer{
    height: 100%;
}

.bottom__spacer{
    height: 100%;
}

.service__area {
    display: flex;
    flex-direction: column-reverse;
}
</style>
