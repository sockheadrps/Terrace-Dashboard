import { writable } from "svelte/store";

let bookmarkStorage = [
    {name: "Youtube", url: "https://www.youtube.com", "icon": "logos:youtube-icon"},
    {name: "Reddit", url: "https://www.reddit.com", "icon": "logos:reddit-icon"},
    {name: "Twitch", url: "https://www.twitch.com", "icon": "logos:twitch"},
    {name: "Instagram", url: "https://www.instagram.com", "icon": "skill-icons:instagram"},
]


if(localStorage.getItem("bookmarks") === null)
    localStorage.setItem("bookmarks", JSON.stringify(bookmarkStorage))
else
    bookmarkStorage = JSON.parse(localStorage.getItem("bookmarks"))


export function newBookmark(newBookmark) {
    let index = bookmarkStorage.findIndex((n) => {
         return newBookmark.name === n.name
    })
    if (index > -1) {
        bookmarkStorage[index] = newBookmark
    } else {
        bookmarkStorage.push(newBookmark)
    }
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

export function saveBookmarks() {
    localStorage.setItem("bookmarks", JSON.stringify(bookmarkStorage));
}

export let bookmarkList = writable(bookmarkStorage)
