<script>
    import { bookmarkList } from "../../../bookmarksStore"
    import AddBookmark from "./AddBookmark.svelte";
    import Icon from '@iconify/svelte';
    import 'iconify-icon'
    let addBookMark = false
    let name = ""
    let url = ""
    let icon = ""
    let draggingElName


    function handleDblClick(bookmark) {
        addBookMark = true
        name = bookmark.name
        url = bookmark.url
        icon = bookmark.icon
    }

    function handleDragStart(name){
        draggingElName = name
    }
    let afterElement
    let draggable


    function handleDragEnd(name){
        if (afterElement == null) {
            let index = $bookmarkList.findIndex(el => el.name === name)
            let bookmark = $bookmarkList[index]
            $bookmarkList.splice(index, 1)
            $bookmarkList.push(bookmark)
            $bookmarkList = $bookmarkList


        } else {
            let index = $bookmarkList.findIndex(el => el.name === name)
            let afterIndex = ($bookmarkList.findIndex(el => el.name === afterElement.dataset.name))
            let bookmark = $bookmarkList[index]
            $bookmarkList.splice(afterIndex, 0, bookmark)
            $bookmarkList.splice(index + (afterIndex <= index ? 1 : 0), 1)
            $bookmarkList = $bookmarkList
                }   
        draggingElName = ""
    }

    function handleDragOver(e){
        afterElement = getDragAfterElement(e.clientY)
        draggable = document.querySelector(".dragging")
    }

    function getDragAfterElement(y) {
        const container = document.querySelector(".bookmark__table")
        const draggableElements = [...container.querySelectorAll('.draggable:not(.dragging)')]
        return draggableElements.reduce((closest, child) => {
            const box = child.getBoundingClientRect()
            const offset = y - box.top - box.height / 2
            if (offset < 0 && offset > closest.offset){
                return { offset: offset, element: child }
            } else {
                return closest
            }
        }, {offset: Number.NEGATIVE_INFINITY}).element
    }
    
</script>

<div class="add_bookmark">
    {#if addBookMark}
        <AddBookmark {name} {url} {icon} on:close="{() => addBookMark = false}"  />
    {/if}
    
    <div class="bookmarks__table__container">
        <table class="bookmark__table" on:dragover|preventDefault={(e) => handleDragOver(e)}>
            <thead>
                <th>Bookmark Name</th>
                <th>Bookmark URL</th>
                <th class="td__icon"></th>
            </thead>
            <tr>
                <td>
                    <div class="bookmark__input__bar">
                        <input type="text" class="bookmark__input" placeholder="New Bookmark Title...">
                    </div>
                </td>
                <td>
                    <div class="bookmark__input__bar">
                        <input type="text" class="bookmark__input" placeholder="New Bookmark Title...">
                    </div>
                </td>
                <td class="td__icon" on:click="{() => {addBookMark = true}}">
                    <Icon icon="material-symbols:bookmark-add-outline" /> 
                </td>
                
            </tr>
            {#each $bookmarkList as bookmark}
            <tr data-name={bookmark.name} data-url={bookmark.url} data-icon={bookmark.icon} class="draggable {draggingElName === bookmark.name ? 'dragging' : ''}"  draggable="true" on:dblclick={() => handleDblClick(bookmark)} 
                on:dragstart={() => handleDragStart(bookmark.name)}
                on:dragend={() => handleDragEnd(bookmark.name)}>
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
        font-size: 20px;
        background-color: rgba(51, 51, 51, 0.493);
        outline: none;
        border: none;
        color: #a0a0a0;
    }
.button__container{
    margin-top: 1rem;
    margin-bottom: 1rem;
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

.draggable {
    cursor: move;
}

</style>
