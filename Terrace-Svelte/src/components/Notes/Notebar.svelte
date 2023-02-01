<script>
    import { currentNavStore } from '../../stores';
    import { notesStore, currentIdStore, deleteNote } from '../../notesStore'
    import NoteButton from './NoteButton.svelte';


</script>

<head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css" integrity="sha512-MV7K8+y+gLIBoVD59lQIYicR65iaqukzvf/nwasF0nqhPay5w/9lJmVM2hMDcnK1OnMGCdVK+iQrJ7lzPJQd1w==" crossorigin="anonymous" referrerpolicy="no-referrer" />
</head>
<div class="notes__nav">
    <button on:click={() => currentNavStore.set("Home")} class="back"><i class="fa fa-solid fa-rotate-left" style="vertical-align: middle"></i></button>
    <div class="notes">
        {#each Object.entries($notesStore) as [id, note]}
            <NoteButton {id} {note} />
        {/each}
    </div>
    <button on:click={() => ($currentIdStore = undefined)} class="button__container">
        <i class="back-icon fa fa-2x fa-duotone fa-plus"></i>
    </button>
</div>

<style>

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Asap', sans-serif;
    font-family: 'Spline Sans', sans-serif;
    line-height: 1.5;
  }


.notes__nav{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: linear-gradient(
        to left top,
         rgba(27, 27, 27, 0.911),
         rgba(20, 20, 20, 0.904)
         );
    border: none;
    color: #ffffff;
    font-size: 1.25em;
    font-weight: bold;
    width: 100%;
    height: 100%;
    user-select: none;
}

.notes {
    height:100%;
    overflow-y: scoll;
}

.back {
    border-radius: 2rem 0rem 0rem 0rem;
    display: block;
    margin: 0px;
    width: 100%;
    height: 60px;
    background: none;
    border: none;
    color: #808080;
    font-size: 18px;
    cursor: pointer;
    background:rgba(64, 64, 73, 0.1);
}

.back:hover {
    background: linear-gradient(rgb(0, 0, 0),rgb(15, 15, 15)) padding-box,
                linear-gradient(to right, rgba(84, 69, 99, 0.034), rgba(101, 101, 143, 0)) border-box;
}

button {
    cursor: pointer;
    border: none;
    outline: none;
}

.button__container{
    background: linear-gradient(
        #2e2e2e00,
        #1d1d1d 95%
         );
    backdrop-filter: blur(.2rem);
    display: block;
    color: #808080;
    height: 90px;
    align-items: center;
    bottom: 0px;
    position: sticky;
    padding: auto;
}

.button__container:hover {
    background: linear-gradient(rgb(0, 0, 0),rgb(15, 15, 15)) padding-box,
                linear-gradient(to right, rgba(84, 69, 99, 0.034), rgba(101, 101, 143, 0)) border-box;
}

</style>
