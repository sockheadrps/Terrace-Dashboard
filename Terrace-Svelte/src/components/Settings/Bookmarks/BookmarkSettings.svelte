<script>
    import { bookmarkList } from "../../../bookmarksStore"
    import AddBookmark from "./AddBookmark.svelte";
    import Icon from '@iconify/svelte';
    import 'iconify-icon'
    let addBookMark = false
    let name = ""
    let url = ""
    let icon = ""

    function handleDblClick(bookmark) {
        addBookMark = true
        name = bookmark.name
        url = bookmark.url
        icon = bookmark.icon
    }
    
</script>

<div class="add_bookmark">
    <div class="button__container">
        <button on:click="{() => addBookMark = true}">
            <Icon icon="material-symbols:add-box" />
        </button>
    </div>

    {#if addBookMark}
        <AddBookmark {name} {url} {icon} on:close="{() => addBookMark = false}"  />
    {/if}
    
    <div class="bookmarks__table__container">
        <table class="bookmark__table">
            <tr>
                <th>Bookmark Name</th>
                <th>Bookmark URL</th>
                <th class="td__icon">Bookmark Icon</th>
            </tr>
            {#each $bookmarkList as bookmark}
            <tr on:dblclick={() => handleDblClick(bookmark)}>
                <td>
                    <span class="name">{bookmark.name}</span>
                </td>
                <td>
                    <span class="url">{bookmark.url}</span>
                </td>
                <td class="td__icon">
                    <Icon icon={bookmark.icon} /> 
                </td>
            </tr>
            {/each}
        </table>
    </div>

</div>

<style>

.button__container{
    margin-top: 1rem;
    margin-bottom: 1rem;
    margin-left: 5%;
}

.bookmark__table{
    border-collapse: collapse;
    width: 90%;
    margin-left: 5%;
}

.bookmark__table td, .bookmark__table th {
    /* border: 1px solid rgb(255, 255, 255); */
    padding: 8px;
    text-align: left;

}

.bookmark__table tr:nth-child(even){
    background-color: #20202071;
}

.bookmark__table th {
    padding-top: 12px;
    padding-bottom: 12px;
    text-align: left;
    background-color: #35353577;
}

.bookmark__table .td__icon {
    text-align: center;
}
button {
    cursor: pointer;
}

button{
    display: flex;
    border-radius: .5rem;
    text-align: center;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
    border: 1px solid rgba(10, 6, 24, 0.021);
    background:rgba(125, 125, 129, 0.1);
    cursor: pointer;
    transition: all .01s ease-out;
    font-size: 40px;
    color: rgb(136, 136, 136);
    padding: 5px 40px 5px 40px;
}

button:hover {
    background: linear-gradient(rgb(37, 37, 37),rgb(51, 51, 51)) padding-box,
                linear-gradient(to right, rgba(61, 61, 61, 0.11), rgba(129, 129, 129, 0)) border-box;
                border-radius: .5rem;

    border: 1px solid transparent;
    color: #c4c3c3;
}
</style>
