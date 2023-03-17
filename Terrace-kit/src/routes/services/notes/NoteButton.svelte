<script>
    import { currentIdStore, notesStore, deleteNote, deleting } from "../../../lib/stores/notesStore";
    export let id, note


    function doDelete(id) {
        const del = confirm("Are you sure you want to delete this note?");
        if (del) {
            delete $notesStore[id]
            deleteNote(id)
            $notesStore = $notesStore
            if ($currentIdStore === id) {
                $currentIdStore = undefined;
            }
        }
    }

</script>


<button on:click={() => $currentIdStore = id} on:dblclick={() => doDelete(id)} class="note">
    <span class="body"></span>
    <span class="title">
        {note.title}
    </span>
</button>


<style>
    button {
    cursor: pointer;
    border: none;
    outline: none;
}

.note{
    display: grid;
    height: 120px;
    width: 100%;
    background:rgba(64, 64, 73, 0.1);
    vertical-align: middle;
    outline: none;
    border: none;
    color: antiquewhite;
}

.note:hover {
    background: linear-gradient(rgb(0, 0, 0),rgb(15, 15, 15)) padding-box,
                linear-gradient(to right, rgba(84, 69, 99, 0.034), rgba(101, 101, 143, 0)) border-box;
}


.notes::-webkit-scrollbar {
    background: #0000;
    width: 20px;
  }
.notes::-webkit-scrollbar-track {
    border-radius: 10px;
    background-clip: padding-box;
  }
.notes::-webkit-scrollbar-thumb {
    background: #0D0D0D;
    border-radius: 10px;
    background-clip: padding-box;
  }
.notes::-webkit-scrollbar-thumb:hover {
    background: #222;
    background-clip: padding-box;
}


</style>
