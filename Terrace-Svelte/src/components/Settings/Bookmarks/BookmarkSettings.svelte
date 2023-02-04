<script>
    import { bookmarkList, saveBookmarks } from "../../../bookmarksStore"
    import AddBookmark from "./AddBookmark.svelte";
    import Icon from '@iconify/svelte';
    import 'iconify-icon'
    let addBookMark = false
    let name = ""
    let url = ""
    let icon = ""
    let index
    let afterIndex


    function handleDblClick(bookmark) {
        addBookMark = true
        name = bookmark.name
        url = bookmark.url
        icon = bookmark.icon
    }

    function handleDragEnd(){
        let bookmark = $bookmarkList[index]

        $bookmarkList.splice(index, 1);
        $bookmarkList.splice(afterIndex, 0, bookmark);

        $bookmarkList = $bookmarkList
        saveBookmarks();
        index = undefined;
    }
</script>

<div class="add_bookmark">
    {#if addBookMark}
        <AddBookmark bind:name bind:url bind:icon on:close="{() => {addBookMark = false;name='';url='';icon=''}}"  />
    {/if}
    
    <div class="bookmarks__table__container">
        <table class="bookmark__table">
            <thead>
                <tr>
                    <th>Bookmark Name</th>
                    <th>Bookmark URL</th>
                    <th class="td__icon"></th>
                </tr>
                <tr>
                    <td>
                        <div class="bookmark__input__bar">
                            <span class="bookmark__input" contenteditable="true" spellcheck="false" placeholder="Title" bind:textContent={name}></span>
                        </div>
                    </td>
                    <td>
                        <div class="bookmark__input__bar">
                            <span class="bookmark__input" contenteditable="true" spellcheck="false" placeholder="URL" bind:textContent={url}></span>
                        </div>
                    </td>
                    <td class="td__icon">
                        <button on:click="{() => addBookMark = true}">
                            <Icon icon="material-symbols:bookmark-add-outline" /> 
                        </button>
                    </td>
                </tr>
            </thead>
            <tbody>
                {#each $bookmarkList as bookmark, idx (idx)}
                <tr data-name={bookmark.name} class="draggable {index === idx ? 'dragging' : ''}"
                    draggable="true"
                    on:dblclick={() => handleDblClick(bookmark)} 
                    on:dragstart={() => index = idx}
                    on:dragover={() => afterIndex = idx}
                    on:dragend={handleDragEnd}>
                    
                    <td>
                        <div class="bookmark__input__bar">
                            <span class="bookmark__input" contenteditable="true" spellcheck="false" bind:textContent={bookmark.name} on:input={saveBookmarks}></span>
                        </div>
                    </td>
                    <td>
                        <div class="bookmark__input__bar">
                            <span class="bookmark__input" contenteditable="true" spellcheck="false" bind:textContent={bookmark.url} on:input={saveBookmarks}></span>
                        </div>
                    </td>
                    <td class="td__icon">
                        <Icon icon={bookmark.icon} /> 
                    </td>
                </tr>
                {/each}
            </tbody>
        </table>
    </div>
</div>
<style>


.bookmarks__table__container{
    margin-top: 5rem;
}

.bookmark__input__bar{
    vertical-align: middle;
    position: relative;
    z-index: 1;
}

.bookmark__input {
    display: inline-block;
    cursor: text;
    min-width: 12rem;
    max-width: 30rem;
    width: auto;
    font-size: 15px;
    background-color: inherit;
    outline: none;
    border: none;
    color: #838383;
    transition: 0.2s background-color ease-in-out;
    padding: 5px 4px 5px 4px;
    border-radius: 5px;
}

.bookmark__input:focus {
    background-color: rgba(51, 51, 51, 0.493);
}

:global(.bookmark__input[contentEditable="true"]:empty:before) {
    content: attr(placeholder);
    color: #636363;
}

.bookmark__table{
    border-collapse: collapse;
    width: 90%;
    margin-left: 5%;
    user-select: none;
}

.bookmark__table td, .bookmark__table th {
    padding: 8px;
    text-align: left;
    user-select: none;
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
    font-size: 25px;
}

button {
    cursor: pointer;
    background: none;
    border: none;
    outline: none;
    font-size: 25px;
    color: inherit;
    transition: 0.2s color ease-in-out;
}

button:hover {
    outline: 1px solid transparent;
    color: #c4c3c3;
}

.draggable {
    cursor: move;
}

</style>
