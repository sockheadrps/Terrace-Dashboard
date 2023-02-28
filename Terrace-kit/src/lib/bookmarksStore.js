import { onMount } from "svelte";
import { writable } from "svelte/store";

let bookmarkStorage = [
    {name: "Youtube", url: "https://www.youtube.com", "icon": "logos:youtube-icon"},
    {name: "Reddit", url: "https://www.reddit.com", "icon": "logos:reddit-icon"},
    {name: "Twitch", url: "https://www.twitch.com", "icon": "logos:twitch"},
    {name: "Instagram", url: "https://www.instagram.com", "icon": "skill-icons:instagram"},
]


export function loadBookmarks() {
    if(localStorage.getItem("bookmarks") === null) {
        localStorage.setItem("bookmarks", JSON.stringify(bookmarkStorage))
    }
    return JSON.parse(localStorage.getItem("bookmarks"))
}




export function newBookmark(newBookmark) {
    bookmarkStorage = loadBookmarks()
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
    let toDelete = bookmarkStorage.filter(entry => entry.name === name.name)[0]
    console.log(toDelete)
    if (toDelete) {
        let filteredBookmarks = bookmarkStorage.filter(entry => entry.name !== name.name)
        localStorage.setItem("bookmarks", JSON.stringify(filteredBookmarks))
        bookmarkList.set(filteredBookmarks)
        return toDelete
    }
}

export function saveBookmarks(bookmarks) {
    localStorage.setItem("bookmarks", JSON.stringify(bookmarks));
}

export let bookmarkList = writable(bookmarkStorage)
