/* eslint-disable max-len */
import { writable } from 'svelte/store';
const notes = [];

Object.keys(localStorage).forEach((element) => {
    if (parseInt(element)) {
        notes.push(JSON.parse(localStorage.getItem(String(element))));
    }
});
export const notesStore = writable(notes);

// eslint-disable-next-line require-jsdoc
export function storeNote (title, markdown, id) {
    console.log('id ' + id);
    let note = JSON.parse(localStorage.getItem(String(id)));
    console.log(note);
    // If note exists, update note data
    if (note !== null) {
        note.body = markdown;
        note.timeStamp = new Date().toISOString();
    // Otherwise add new note
    } else {
        note = {
            id: Date.now(),
            title,
            body: markdown,
            timeStamp: new Date().toISOString()
        };
    }
    // Save to local storage
    console.log(note)
    localStorage.setItem(note.id, JSON.stringify(note));
    return note;
}

// eslint-disable-next-line require-jsdoc
export function getNote (id) {
    const note = JSON.parse(localStorage.getItem(String(id)));
    console.log('getNote')
    console.log(note)
    return note;
}

export const currentIdStore = writable();
