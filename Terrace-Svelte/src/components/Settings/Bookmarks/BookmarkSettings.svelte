<script>
    import { bookmarkList } from "../../../bookmarksStore"
    import AddBookmark from "./AddBookmark.svelte";
    import Icon from '@iconify/svelte';
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
                <!-- Doesnt seem to load the icon -->
                <Icon icon={bookmark.icon} />    
            </li>
            {/each}
        </ol>
</div>