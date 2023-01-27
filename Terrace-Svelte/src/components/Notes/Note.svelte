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

    console.log($notesStore)

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
        console.log(markdown)
        clearTimeout(inputTimeout);
        inputTimeout = setTimeout(saveNote, 1500);
    }

    $: {
        // If no note is selected / the add button has be clicked
        if ($currentIdStore === undefined) {
            md = '';
            title = '';
        } else {
        // If a note in the notebar as been selected, set the note view title and body
            let currentNote = getNote($currentIdStore);
            title = currentNote.title;
            md = currentNote.body;
        }
    }

    $: if(title || md) onInput(title, md);
</script>

<div class="main">
    <div class="top__bar">
        <div class="edit__area">
            <button on:click={() => edit = !edit} >Edit</button>
            <input class="edit__{edit}" type="text" bind:value="{title}" />
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
                        position: "relative",
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
        background: linear-gradient(to right bottom, rgba(10, 6, 24, 0.75), rgba(10, 6, 24, 0.69));
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
    }

    .title__area {
        grid-column: 2;
        text-align: center;
    }

    .bar__title {

    }

    button{
        width: 6rem;
    }

    input{

    }

    .note__area {
        display: grid;
        grid-template-columns: 2fr 3fr;
    }

    .edit__false {
        display: grid;
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
        color: red;
        display: block;
        word-break: break-all;
        text-align: start;
        padding-left: 2rem;
    }

    .output.edit__false{
        grid-column: 1;
    }
</style>
