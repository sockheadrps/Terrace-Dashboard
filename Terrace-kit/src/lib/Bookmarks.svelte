<script lang="ts">
    import { bookmarkList, loadBookmarks } from '$lib/bookmarksStore'
    import Icon, { disableCache } from '@iconify/svelte';
	import { onMount } from 'svelte';
	import { quadIn } from 'svelte/easing';
	import { blur } from 'svelte/transition';
    let timing: number = 100;
    onMount(() => {
        $bookmarkList = loadBookmarks();
    })

    console.log(timing)

</script>


<div class="bookmark-area rounded-md">
    <div class="flex flex-row my-auto">
        {#each $bookmarkList as book, index}
        <div class="m-auto text-center h-full"
        in:blur={{delay: (index * 150) + 100, easing: quadIn}}
        >
            <a href={book.url} class="bookmark rounded-md inline-block" >
                <div class="flex flex-row justify-center">
                    <Icon icon={book.icon} style="font-size: 2.5rem;" />
                </div>
                <div class="title-area inline-block">
                    <span class="bk-title">{book.name}</span>
                </div>
            </a>
        </div>
        {/each}
    </div>
</div>

<style>
.bookmark-area {
    display: grid;
    background: linear-gradient(
        to left top,
         rgba(24, 24, 24, 0.822),
         rgba(15, 15, 15, 0.863)
         );
    /* border-radius: 2rem; */
    padding-left: 1rem;
    padding-right: 1rem;
    color: #808080;
}

.title-area {
    margin: auto;
}


.bookmark{
    display: inline-block;
    vertical-align: middle;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
    border: 1px solid rgba(10, 6, 24, 0.021);
    background:rgba(64, 64, 73, 0.1);
    backdrop-filter: blur(1.1rem);
    margin: .5rem;
    padding: .5rem;
    cursor: pointer;
    transition: all .2s ease-out;
    min-width:  170px;
    text-decoration: none;
}

a { color: inherit; }

.bookmark:hover {
    background: linear-gradient(rgb(0, 0, 0),rgb(15, 15, 15)) padding-box,
                linear-gradient(to right, rgba(84, 69, 99, 0.034), rgba(101, 101, 143, 0)) border-box;
    border: 1px solid transparent;
    opacity: .7;
    color: #525151;
}

</style>
