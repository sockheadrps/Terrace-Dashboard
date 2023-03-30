/* eslint-disable max-len */
import { writable } from 'svelte/store';
const notes = {};

if (typeof localStorage !== 'undefined') {
    Object.keys(localStorage).forEach((element) => {
        if (parseInt(element)) {
            notes[element] = JSON.parse(localStorage.getItem(element));
        }
    });
}

export const notesStore = writable(notes);

// eslint-disable-next-line require-jsdoc
export function storeNote (title, markdown, id) {
    console.log('Storing note...');
    let note = JSON.parse(localStorage.getItem(id));
    // If note exists, update note data
    if (note !== null) {
        note.title = title;
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
    localStorage.setItem(note.id, JSON.stringify(note));
    return note;
}

// eslint-disable-next-line require-jsdoc
export function getNote (id) {
    const note = JSON.parse(localStorage.getItem(id));
    return note;
}

export function deleteNote (id) {
    localStorage.removeItem(id)
    delete notes[id]

}

export const deleting = writable(false);
export const currentIdStore = writable();
