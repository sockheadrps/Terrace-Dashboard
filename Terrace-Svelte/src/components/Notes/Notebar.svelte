<script>
    import { currentNavStore } from '../../stores';
    import { notesStore, currentIdStore } from '../../notesStore'


</script>

<head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css" integrity="sha512-MV7K8+y+gLIBoVD59lQIYicR65iaqukzvf/nwasF0nqhPay5w/9lJmVM2hMDcnK1OnMGCdVK+iQrJ7lzPJQd1w==" crossorigin="anonymous" referrerpolicy="no-referrer" />
</head>
<div class="notes__nav">
    <button on:click={() => currentNavStore.set("Home")} class="back"><i class="fa fa-solid fa-rotate-left" style="vertical-align: middle"></i></button>
    <div class="notes">
        {#each Object.entries($notesStore) as [id, note]}
            <button on:click={() => $currentIdStore = id} class="note">
                <span class="body">
                </span>
                <span class="title">
                    {note.title}
                </span>
            </button>
        {/each}
    </div>
    <button on:click={() => ($currentIdStore = undefined)} class="button__container">add</button>
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
    display: grid;
    grid-column: 1;
    grid-template-rows: 1fr 11fr 1fr;
    border: 1px solid red;
    background: linear-gradient(
       rgba(23, 24, 71, 0.05),
       rgba(24, 26, 75, 0.027)
       );
    border: none;
    color: #ffffff;
    font-size: 1.25em;
    font-weight: bold;
    width: 100%;
    user-select: none;
}

.back {
    border-radius: 2rem 0rem 0rem 0rem;
    background:rgba(11, 11, 51, 0.377);
    display: flex;
    justify-content: center;
    align-items: center;
}

.back:hover {
    background: rgba(12, 7, 31, 0.781);
}

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
    background: rgba(12, 7, 31, 0.781);
}


.notes__nav::-webkit-scrollbar {
    background: #0000;
    width: 20px;
  }
.notes__nav::-webkit-scrollbar-track {
    border-radius: 10px;
    background-clip: padding-box;
  }
.notes__nav::-webkit-scrollbar-thumb {
    background: #0D0D0D;
    border-radius: 10px;
    background-clip: padding-box;
  }
.notes__nav::-webkit-scrollbar-thumb:hover {
    background: #222;
    background-clip: padding-box;
}

.button__container{
    background: linear-gradient(
        #1e1e2b00,
        #181823 95%
         );
    backdrop-filter: blur(.2rem);
    display: flex;
    align-items: center;
    border-radius: .5rem .5rem 0 0;
    bottom: 0px;
    position: sticky;

}
</style>
