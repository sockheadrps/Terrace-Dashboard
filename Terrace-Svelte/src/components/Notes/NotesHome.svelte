<script>
    import Notebar from './Notebar.svelte';
    import Note from './Note.svelte'

</script>

    <div class="nav__area">
        <Notebar />
    </div>
    <div class="main__area">
        <Note />
    </div>

<style>

    .nav__area{
        grid-column: 1;
    }


</style>