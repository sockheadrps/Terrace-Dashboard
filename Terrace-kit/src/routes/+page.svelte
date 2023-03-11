<script lang="ts">
    import Search from "$lib/Search.svelte";
    import Weather from "$lib/Weather.svelte";
    import Bookmarks from "$lib/Bookmarks.svelte";
    import { fade } from 'svelte/transition';
	import { quintIn, quintOut } from 'svelte/easing';
	import { onMount } from "svelte";
    let ready = false;

    onMount(() => {
        ready = true
    })
    
</script>

<div id="main__content" class="grid grid-rows-6 gap-4 tablet:gap2 align-top overflow-hidden tablet:grid-rows-4">
    <div class="search__area"
    in:fade={{ duration: 250, easing: quintIn, delay: 150 }}
	out:fade={{ duration: 100, easing: quintOut }}
    >
        <Search />
    </div>
    <div class="row-span-2 my-auto"
    in:fade={{ duration: 250, easing: quintIn, delay: 250 }}
	out:fade={{ duration: 100, easing: quintOut }}>
        <Weather />
    </div>
    <div class="row-span-2"
    in:fade={{ duration: 250, easing: quintIn, delay: 550 }}
	out:fade={{ duration: 100, easing: quintOut }}>
        <Bookmarks />
    </div>
</div>



