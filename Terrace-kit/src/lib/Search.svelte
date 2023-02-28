<script lang="ts">
    import Icon from "@iconify/svelte";
    const actions = ["https://www.google.com/search", "https://www.youtube.com/results?search_query="]
    let clicked = "",
        action  = 0;
    let value: string
    let google = true
    import { fade } from "svelte/transition";

    function changeSearch() {
        google = ! google
        clicked = clicked ? "" : "clicked";
        action = action ? 0 : 1;
    }
</script>


<div class="w-full rounded-md hover:bg-original-input-hover transition-colors mt-5">
    <div class="flex flex-row h-14">
        <div class="text-3xl inline-block relative">
                {#if google}
                <div class="absolute top-1/2 -translate-y-1/2 pl-4" 
                in:fade|local={{ delay: 400, duration: 400 }} out:fade|local={{ duration: 400 }}
                on:click={() => changeSearch()} on:keydown={(e) => {if (e.key == "Enter") changeSearch()}}>
                    <Icon icon="flat-color-icons:google" />
                </div>

                {:else}
                <div class="text-2xl absolute top-1/2 -translate-y-1/2 pl-4" in:fade|local={{ delay: 400, duration: 400 }}
                on:click={() => changeSearch()} on:keydown={(e) => {if (e.key == "Enter") changeSearch()}} out:fade|local={{ duration: 400 }}>
                    <Icon icon="logos:youtube-icon" />
                </div>
                {/if}
        </div>
        <div class="w-full">
            <form class="h-full w-full" action="{actions[action]}" method="get">
                <input type="text" class="h-full w-full rounded-md text-original-muted bg-original-card-bg-dark outline-none pl-16 focus:bg-original-input-hover placeholder:focus:text-[rgba(100,100,100,.70)] " 
                placeholder="Search..." name="q" bind:value />
            </form>
        </div>
    </div>
</div>
