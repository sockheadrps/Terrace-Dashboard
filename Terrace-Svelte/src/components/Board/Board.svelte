<script>
    import NavBar from "../NavBar/NavBar.svelte";
    import Home from "../Home/Home.svelte";
    import Settings from "../Settings/Settings.svelte";
    import Hardware from "../Hardware/Hardware.svelte";
    import NotesHome from "../Notes/NotesHome.svelte";
    import { currentNavStore, wsSend, terminateHwCommunication, activeHardwareClient } from '../../stores.js'

    const setView = (e) => {
        if ($currentNavStore === "Hardware"){
            // If current view is a HW client and the view is changed, send a disconnect message to the active hw client
            terminateHwCommunication(activeHardwareClient)
        }
        // If view is switched to hardware, send a websocket message requesting the appropriate hw clients
        // data stream, and update the current nav
        if (e.srcElement.classList[0] == "Hardware"){
            $currentNavStore = "Hardware";
            $activeHardwareClient = e.srcElement.innerText
            wsSend({"event": "HARDWARE-REQUEST", "requested-client": e.srcElement.innerText})

        // Otherwise, update the current nav to reflect the target nav view
        } else {
            $currentNavStore = e.srcElement.innerText;
        }
	}
</script>

    <div id="board">
        {#if $currentNavStore !== "Notes"}
            <NavBar on:click={setView}/>
        {/if}
        {#if $currentNavStore == "Notes"}
            <NotesHome />
        {:else if $currentNavStore == "Home"}
            <Home />
        {:else if $currentNavStore == "Settings"}
            <Settings />
        {:else if $currentNavStore == "Hardware"}
            <Hardware />
        {/if}
    </div>

<style>

#board{
    display: grid;
    height: 90vh;
    grid-template-columns: 15% 85%;
    min-width: 1100px;
    background: linear-gradient(
        to left top,
         rgba(36, 36, 36, 0.822),
         rgba(20, 20, 20, 0.863)
         );

    z-index: 4;
    backdrop-filter: blur(.23rem);
    margin: 3rem;
    border-radius: 2rem;
}


</style>
