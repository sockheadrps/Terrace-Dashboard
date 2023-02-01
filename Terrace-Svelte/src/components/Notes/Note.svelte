<script>
    import Markdown from 'svelte-exmarkdown';
    import CodeMirror from 'svelte-codemirror-editor';
    import { markdown } from '@codemirror/lang-markdown';
    import { oneDark } from '@codemirror/theme-one-dark';
    import { notesStore, storeNote, currentIdStore, getNote} from "../../notesStore";
    import codePlugin from "./CodeHighlight";
    import { gfmPlugin } from "svelte-exmarkdown/gfm";
    let edit = true
    let inputTimeout
    const plugins = [codePlugin, gfmPlugin];
    let noteChanged = Date.now()


    let md = '';
    let title = '';

    // Timeout function to save the note after some period of time
    function onInput(title, markdown) {
        function saveNote() {
            let note = storeNote(title, markdown, $currentIdStore);

            if($currentIdStore === undefined)
                $currentIdStore = note.id;

            $notesStore[note.id] = note;
            $notesStore = $notesStore; // ensure update
        }
        clearTimeout(inputTimeout);
        inputTimeout = setTimeout(saveNote, 1500);
    }

    $: {
        console.log($currentIdStore)
        // If no note is selected / the add button has be clicked
        if ($currentIdStore === undefined) {
            md = '';
            title = '';
        } else {
        // If a note in the notebar as been selected, set the note view title and body
            let currentNote = getNote($currentIdStore)
            noteChanged = Date.now()

            title = currentNote.title;
            md = currentNote.body;
        }
    }

    $: if((title || md) && (Date.now() - noteChanged  > 50)) {
        onInput(title, md);
    }
</script>

<div class="main">
    <div class="top__bar">
        <div class="edit__area">
            <button class="edit__button" on:click={() => edit = !edit} >
                <i class="fa-solid fa-pen-to-square"></i>
            </button>
            <input class="edit__{edit} edit__title" type="text" placeholder="Title..." bind:value="{title}" />
        </div>
        <div class="title__area">
            <div class="bar__title">{title}</div>
        </div>
    </div>
    <div class="note__area">
        <div class="input edit__{edit}">
            <CodeMirror
                bind:value={md}
                lang={markdown()}
                theme={oneDark}
                styles={{
                    "&": {
                        textAlign: "left",
                        width: "100%",
                        height: "100%"
                    }
                }}
            />
        </div>
        <div class="output edit__{edit}">
            <Markdown {md} {plugins} />
        </div>
    </div>
</div>

<style>
    :global(.codemirror-wrapper) {
        height: 100%;
    }

    .main {
        display: grid;
        grid-template-columns: 1fr;
        grid-template-rows: 1fr 10fr;
        height: 100%;
    }

    .top__bar {
        display: grid;
        grid-template-columns: 2fr 3fr;
        grid-row: 1;
        color: aliceblue;
        align-items: center;
    }

    .edit__area{
        grid-column: 1;
        text-align: left;
        margin-left: 1rem;
    }

    .edit__button {
        border-radius: 2rem;
        margin: 0px;
        height: 60px;
        background: none;
        border: none;
        color: #808080;
        font-size: 18px;
        cursor: pointer;
        background: rgba(12, 12, 12, 0.918);
    }

    .title__area {
        grid-column: 2;
        text-align: center;
    }

    button{
        width: 6rem;
    }

    .note__area {
        display: grid;
        grid-template-columns: 2fr 3fr;
        margin-left: 1rem;
        margin-bottom: 0px;
    }

    .edit__false {
        display: grid;
    }
    .edit__true.edit__title {
        background-color: rgba(39, 39, 39, 0.705);
        border-radius: 1.2em;
        color: #808080;
        border: none;
        padding: 1rem;
    }

    .edit__true.edit__title:focus {
        outline: none !important;
        box-shadow: 0 0 2px #719ECE;
        border: #303030;
    }

    .input{
        grid-column: 1;
    }

    .input.edit__false {
        display: none;
    }

    input.edit__false {
        display: none;
    }

    .output{
        grid-column: 2;
        color: #c4c4c4;
        display: block;
        word-break: break-all;
        text-align: start;
        padding-left: 2rem;
    }

    .output.edit__false{
        grid-column: 1;
    }
</style>
