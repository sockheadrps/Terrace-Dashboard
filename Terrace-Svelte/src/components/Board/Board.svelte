<script>
    import NavBar from "../NavBar/NavBar.svelte";
    import Home from "../Home/Home.svelte";
    import Settings from "../Settings/Settings.svelte";
    import Hardware from "../Hardware/Hardware.svelte";
    import NotesHome from "../Notes/NotesHome.svelte";
    import { currentNav, wsSend, wsDisconnect, activeHardwareClient } from "../../stores";
    export let navItems
    export let activeNav = "Notes"

    function storeNav(activeNav) {
    	currentNav.update(value => activeNav)
    }

    const setView = (e) => {
        if (activeNav === "Hardware"){
            wsDisconnect(activeHardwareClient)
        }
        if (e.srcElement.classList[0] == "Hardware"){
            console.log('if 1')
            activeNav = "Hardware"
            storeNav(activeNav)
            activeHardwareClient.update(value => e.srcElement.innerText)
            wsSend({"event": "HARDWARE-REQUEST", "requested-client": e.srcElement.innerText})

        } else {
            console.log("🚀 ~ file: Board.svelte:30 ~ setView ~ activeNav", activeNav)
            activeNav = e.srcElement.innerText
            storeNav(activeNav)
            }
	    }
</script>

    <div id="board">
        <NavBar {navItems} on:click={setView}/>
        {#if (activeNav == "Notes")}
            <NotesHome />
        {:else if activeNav == "Home"}
            <Home />
        {:else if activeNav == "Settings"}
            <Settings />
        {:else if activeNav == "Hardware"}
            <Hardware />

        {/if}
    </div>

<style>
    
#board{
    display: grid;
    height: 90%;
    user-select: none;
    grid-template-columns: 15% 85%;
    min-width: 1100px;
    background: linear-gradient(
        to left top,
         rgba(194, 194, 194, 0.068), 
         rgba(9, 11, 61, 0.486)
         );
    
    z-index: 4;
    backdrop-filter: blur(.23rem);
    margin: 3rem;
    border-radius: 2rem;
}
</style>