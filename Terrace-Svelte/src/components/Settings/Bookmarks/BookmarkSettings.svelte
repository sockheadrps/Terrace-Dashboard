<script>
    import { bookmarkList, saveBookmarks } from "../../../bookmarksStore"
    import AddBookmark from "./AddBookmark.svelte";
    import Icon from '@iconify/svelte';
    import 'iconify-icon'
    let currentBookmark
    let name = ""
    let url = ""
    let body
    let index
    let afterIndex


    function editBookmark(bookmark) {
        currentBookmark = bookmark;
    }

    function handleDragEnd(){
        let startKeys = transitionKeys();
        let endKeys = move([...startKeys], index, afterIndex);

        animateShift(startKeys, endKeys);
        move($bookmarkList, index, afterIndex);

        $bookmarkList = $bookmarkList;
        saveBookmarks();
    }


    function transitionKeys() {
        return Array.from(body.children).map((e) => e.getBoundingClientRect());
    }

    function animateShift(startKeys, endKeys) {
        requestAnimationFrame(() => {
            let children = Array.from(body.children);
            children.forEach((e, idx) => {
                e.style.transition = 'transform 0s';
                e.style.transform = `translate(${endKeys[idx].x - startKeys[idx].x}px, ${endKeys[idx].y - startKeys[idx].y}px)`;
            });


            requestAnimationFrame(() => {
                let cnt = index < afterIndex ? 0 : index - afterIndex - 1;
                children.forEach((e, idx) => {
                    if(idx !== afterIndex) {
                        e.style.transition = `transform 500ms ${cnt*50}ms ease-in-out`;
                        if(index < afterIndex)
                            cnt += index <= idx ? 1 : 0;
                        else
                            cnt -= idx < index ? 1 : 0;
                    } else {
                        e.style.transition = `transform ${450+Math.abs(afterIndex-index)*50}ms ease-in-out`;
                    }
                    e.style.transform = '';
                });
            });
        });
    }

    function move(arr, origIdx, newIdx) {
        let val = arr[origIdx];
        arr.splice(origIdx, 1);
        arr.splice(newIdx, 0, val);
        return arr;
    }
</script>

<div class="add_bookmark">
    {#if currentBookmark !== undefined}
        <AddBookmark bind:currentBookmark on:close="{() => {currentBookmark=undefined;name='';url=''}}"  />
    {/if}
    
    <div class="bookmarks__table__container">
        <table class="bookmark__table">
            <thead>
                <tr>
                    <th>
                        <div class="bookmark__input__bar">
                            <span class="bookmark__input" contenteditable="true" spellcheck="false" placeholder="Title" bind:textContent={name}></span>
                        </div>
                    </th>
                    <th>
                        <div class="bookmark__input__bar">
                            <span class="bookmark__input" contenteditable="true" spellcheck="false" placeholder="URL" bind:textContent={url}></span>
                        </div>
                    </th>
                    <th class="td__icon">
                        <button on:click="{() => editBookmark({ name, url })}">
                            <Icon icon="material-symbols:bookmark-add-outline" /> 
                        </button>
                    </th>
                </tr>
            </thead>
            <tbody bind:this={body}>
                {#each $bookmarkList as bookmark, idx (idx)}
                <tr class="draggable"
                    draggable="true"
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
                        <button on:click={() => editBookmark(bookmark)}>
                            <Icon icon={bookmark.icon} /> 
                        </button>
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

th .bookmark__input:focus {
    background-color: rgba(62, 62, 62, 0.493);
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
