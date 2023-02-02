import { writable } from "svelte/store";

let initBookmarks = [
    {name: "Youtube", url: "http://www.youtube.com", "icon": "book-icon fa-3x fa fa-brands fa-youtube"},
    {name: "Reddit", url: "http://www.reddit.com", "icon": "book-icon fa-3x fa fa-brands fa-reddit-alien"},
    {name: "Twitch", url: "http://www.twitch.com", "icon": "book-icon fa-3x fa fa-brands fa-twitch"},
    {name: "Instagram", url: "http://www.instagram.com", "icon": "book-icon fa-3x fa fa-brands fa-instagram"},
]
// TODO only if doesnt exist
localStorage.setItem("bookmarks", JSON.stringify(initBookmarks))
let bookmarkStorage = JSON.parse(localStorage.getItem("bookmarks") )


export function newBookmark(name, url, icon) {
    const newBookmark = {
        name: name,
        url: url,
        icon: icon
    }
    bookmarkStorage.push(newBookmark)
    localStorage.setItem("bookmarks", JSON.stringify(bookmarkStorage))
    bookmarkList.set(bookmarkStorage)
}

export function deleteBookmark(name) {
    bookmarkStorage = JSON.parse(localStorage.getItem("bookmarks"))
    let toDelete = bookmarkStorage.filter(entry => entry.name === name)[0]
    if (toDelete) {
        let filteredBookmarks = bookmarkStorage.filter(entry => entry.name !== name)
        localStorage.setItem("bookmarks", JSON.stringify(filteredBookmarks))
        bookmarkList.set(filteredBookmarks)
        return toDelete
    }
}

export let bookmarkList = writable(bookmarkStorage)
