<script>
    let settingsItems = ["Weather", "Bookmarks"];
</script>

<nav id="navbar">
    <div class="nav__top"></div>
    <div id="nav__items">
        {#each settingsItems as setting}
            <a href="/settings/{setting.toLowerCase()}">
                <button class="nav__item route">{setting}</button>
            </a>
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
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    justify-content: start;
    padding-left: 2rem;
    padding-right: 2rem;
}


.nav__item{
    margin: 0px;
    background: none;
    border: none;
    color: #808080;
    font-size: 18px;
    cursor: pointer;
    background: rgba(12, 12, 12, 0.918);
    transition: all .2s ease-out;
    padding: 1rem;
    width: 100%;
    border-radius: 0rem 0rem 1rem 1rem;
}


.nav__item:hover {
    background: rgba(0, 0, 0, 0.959);
  }

.active {
    background: rgba(41, 41, 41, 0.918);

}

</style>
