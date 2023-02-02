import { writable } from "svelte/store";

let bookmarkStorage = [
    {name: "Youtube", url: "http://www.youtube.com", "icon": "logos:youtube-icon"},
    {name: "Reddit", url: "http://www.reddit.com", "icon": "logos:reddit-icon"},
    {name: "Twitch", url: "http://www.twitch.com", "icon": "logos:twitch"},
    {name: "Instagram", url: "http://www.instagram.com", "icon": "skill-icons:instagram"},
]

if(localStorage.getItem("bookmarks") === undefined)
    localStorage.setItem("bookmarks", JSON.stringify(initBookmarks))
else
    bookmarkStorage = JSON.parse(localStorage.getItem("bookmarks"))


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
