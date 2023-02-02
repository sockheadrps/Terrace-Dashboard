<script>
    import { each } from "svelte/internal";
    import { bookmarkList, newBookmark } from "../../../bookmarksStore"
    import AddBookmark from "./AddBookmark.svelte";
    let addBookMark = true

    
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
                <!-- <span class="icon">{bookmark.icon}</span> -->
            </li>
            {/each}
        </ol>
    

</div>