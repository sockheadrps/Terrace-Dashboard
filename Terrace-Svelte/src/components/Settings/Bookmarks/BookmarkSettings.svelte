<script>
    import { bookmarkList } from "../../../bookmarksStore"
    import AddBookmark from "./AddBookmark.svelte";
    import Icon from '@iconify/svelte';
    import 'iconify-icon'
    let addBookMark = true

    $: {console.log($bookmarkList)}
    
</script>

<div class="add_bookmark">
    <button on:click="{() => addBookMark = true}">
        Add Bookmark
    </button>
    {#if addBookMark}
        <AddBookmark on:close="{() => addBookMark = false}" />
    {/if}
        <ol>
            {#each $bookmarkList as bookmark}
            <li>
                <span class="name">{bookmark.name}</span>
                <span class="url">{bookmark.url}</span>
                <Icon icon={bookmark.icon} />    
            </li>
            {/each}
        </ol>
</div>

<style>
button {
    cursor: pointer;
}
</style>
