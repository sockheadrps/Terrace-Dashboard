<script>
    import NavBar from "../NavBar/NavBar.svelte";
    import Home from "../Home/Home.svelte";
    import Settings from "../Settings/Settings.svelte";
    import Hardware from "../Hardware/Hardware.svelte";
    import NotesHome from "../Notes/NotesHome.svelte";
    import { currentNav, wsSend, terminateHwCommunication, activeHardwareClient } from '../../stores.js'
    export let navItems
    export let activeNav = "Notes"


    // If current view is a HW client and the view is changed, send a disconnect message to the active hw client
    const setView = (e) => {
        if (activeNav === "Hardware"){
            terminateHwCommunication(activeHardwareClient)
        }
        // If view is switched to hardware, send a websocket message requesting the appropriate hw clients
        // data stream, and update the current nav
        if (e.srcElement.classList[0] == "Hardware"){
            activeNav = "Hardware";
            currentNav.update(value => activeNav)
            activeHardwareClient.update(value => e.srcElement.innerText)
            wsSend({"event": "HARDWARE-REQUEST", "requested-client": e.srcElement.innerText})

        // Otherwise, update the current nav to reflect the target nav view
        } else {
            activeNav = e.srcElement.innerText;
            currentNav.update(value => activeNav)
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