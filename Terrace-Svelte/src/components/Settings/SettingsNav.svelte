<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();
    export let settingsItems = ["Weather"];
    export let activeSetting;

</script>

<nav id="navbar">
    <div class="nav__top"></div>
    <div id="nav__items">
        {#each settingsItems as setting}
            <div class="nav__lay"></div>
            <button on:click={() => activeSetting=setting} class="{setting.toLowerCase()} nav__item route {activeSetting === setting ?'active' : ''}" id={setting.toLowerCase()+"__nav"}>{setting}
            </button>
        {/each}
    </div>
</nav>

<style>

#navbar {
    display: grid;
    min-width: 100px;
    grid-template-columns: 100%;
    grid-gap: 0px;
    border-radius: 2rem 2rem 0rem 0rem;
}


#nav__items{
    display: flex;
    flex-direction: row;
    padding-left: 2rem;
    padding-right: 2rem;
}


.nav__item{
    width: 20%;
    margin: 0px;
    background: none;
    border: none;
    color: #808080;
    font-size: 18px;
    cursor: pointer;
    background: rgba(12, 12, 12, 0.918);
    transition: all .2s ease-out;
    padding: 1rem;
    border-radius: 0rem 0rem 1rem 1rem;
}


.nav__item:hover {
    background: rgba(0, 0, 0, 0.959);
  }

.active {
    background: rgba(41, 41, 41, 0.918);

}

</style>
