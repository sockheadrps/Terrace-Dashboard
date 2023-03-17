<script>
    import Notebar from './Notebar.svelte';
    import Note from './Note.svelte'

</script>

    <div class="nav__area scroll">
        <Notebar />
    </div>
    
    <div class="main__area scroll">
        <Note />
    </div>

<style>

    .nav__area{
        overflow-y: overlay;
        border-radius: 2rem 0rem 0 2rem;
    }

    .main__area {
        overflow-y: auto;
    }

    .scroll::-webkit-scrollbar {
        display: block;
        background: rgba(0, 0, 0, 0);
    }

    .scroll::-webkit-scrollbar-track {
        border-radius: 10px;
        background-clip: padding-box;
        margin-right: -1rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    .scroll::-webkit-scrollbar-track-piece:end {
        background: transparent;
    }

    .scroll::-webkit-scrollbar-track-piece:start {
        background: transparent;
    }

    .scroll::-webkit-scrollbar-thumb {
        background: rgb(44, 44, 44);
        border-radius: 10px;
        border: 5px solid #0000;
        background-clip: padding-box;
    }
    .scroll::-webkit-scrollbar-thumb:hover {
        background: #222;
        background-clip: padding-box;
    }


</style>
