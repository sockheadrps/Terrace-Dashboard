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
    .nav__area {
        overflow-y: hidden;
    }
    .main__area {
        overflow-y: auto;
    }

    


</style>
