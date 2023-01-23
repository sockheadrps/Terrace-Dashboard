<script>
    let bookMarks = [
        {name: "Youtube", url: "http://www.youtube.com", "icon": "book-icon fa-3x fa fa-brands fa-youtube"},
        {name: "Reddit", url: "http://www.reddit.com", "icon": "book-icon fa-3x fa fa-brands fa-reddit-alien"},
        {name: "Twitch", url: "http://www.twitch.com", "icon": "book-icon fa-3x fa fa-brands fa-twitch"},
        {name: "Instagram", url: "http://www.instagram.com", "icon": "book-icon fa-3x fa fa-brands fa-instagram"},
        {name: "Twitch", url: "http://www.twitch.com", "icon": "book-icon fa-3x fa fa-brands fa-twitch"},
    ]

    // Function allows for horizontal scroll of the bookmarks
    function transformScroll(event) {
        if (!event.deltaY) {
            return;
        }
        event.currentTarget.scrollLeft += event.deltaY + event.deltaX;
        event.preventDefault();
    }

    let element = document.scrollingElement || document.documentElement;
    element.addEventListener('wheel', transformScroll);

    // Google search
    function openBookmark(url) {
        window.open(url,'_blank')
    }
</script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">


<div class="bookmark-area">
    <div class="bookmarks" on:mousewheel|preventDefault={transformScroll}>
        {#each bookMarks as book}
        <div on:click on:keydown={() => {openBookmark(book.url)}} class="bookmark">
            <i class={book.icon}></i>
            <div class="title-area">
            <span class="bk-title">{book.name}</span>
            </div>
        </div>
        {/each}
    </div>
</div>

<style>
.bookmark-area {
    display: grid;
    grid-template-columns: 1fr;
    background: linear-gradient(to right bottom, rgba(10, 6, 24, 0.75), rgba(10, 6, 24, 0.69));
    border-radius: 2rem;
    margin-left: 2rem;
    margin-right: 2rem;
    padding-left: 1rem;
    padding-right: 1rem;
    color: #808080;
}

.bookmarks{
    overflow-x: scroll;
    overflow: overlay;
    white-space: nowrap;
    scrollbar-width: 90%;
}

.title-area {
    margin: auto;
}

.book-icon{
    display: inline-block;
}

.bookmark{
    display: inline-block;
    vertical-align: middle;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
    border: 1px solid rgba(10, 6, 24, 0.021);
    background:rgba(64, 64, 73, 0.1);
    border-radius: 2rem;
    backdrop-filter: blur(1.1rem);
    margin: .5rem;
    padding: .5rem;
    cursor: pointer;
    transition: all .2s ease-out;
    min-width:  170px;
}

.bookmark:hover {
    background: linear-gradient(rgba(10, 6, 24, 0.904),rgba(10, 6, 24, 0.877)) padding-box,
                linear-gradient(to right, rgba(50, 2, 94, 0.774), rgb(26, 28, 143)) border-box;
    border-radius: 2rem;
    border: 1px solid transparent;
    opacity: .7;
    color: #525151;
}

.book-icon {
    margin-bottom: .25rem;
}

.bookmarks::-webkit-scrollbar {
    background: rgba(0, 0, 0, 0);
    display: block;
}
.bookmarks::-webkit-scrollbar-track {
    border-radius: 10px;
    background-clip: padding-box;
}

.bookmarks::-webkit-scrollbar-track-piece:end {
    background: transparent;
    margin-right: 50px; 
}

.bookmarks::-webkit-scrollbar-track-piece:start {
    background: transparent;
    margin-left: 50px;
}

.bookmarks::-webkit-scrollbar-thumb {
    background: rgb(24, 27, 90);
    border-radius: 10px;
    border: 5px solid #0000;
    background-clip: padding-box;
  }
.bookmarks::-webkit-scrollbar-thumb:hover {
    background: #222;
    background-clip: padding-box;
}
</style>