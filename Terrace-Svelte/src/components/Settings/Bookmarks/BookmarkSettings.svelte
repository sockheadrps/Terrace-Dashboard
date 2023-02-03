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

button{
        margin-top: 1rem;
        border-radius: .5rem;
        text-align: center;
        width: 16rem;
        height: 2.5rem;
        -webkit-box-sizing: border-box;
        -moz-box-sizing: border-box;
        box-sizing: border-box;
        border: 1px solid rgba(10, 6, 24, 0.021);
        background:rgba(125, 125, 129, 0.1);
        cursor: pointer;
        transition: all .01s ease-out;
        font-size: larger;
        color: rgb(136, 136, 136);
	}

    button:hover {
        background: linear-gradient(rgb(37, 37, 37),rgb(51, 51, 51)) padding-box,
                    linear-gradient(to right, rgba(61, 61, 61, 0.11), rgba(129, 129, 129, 0)) border-box;
                    border-radius: .5rem;

        border: 1px solid transparent;
        color: #c4c3c3;
    }
</style>
