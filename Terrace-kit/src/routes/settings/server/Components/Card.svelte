<script lang="ts">
    import Icon from '@iconify/svelte';
    import { fade } from 'svelte/transition';
    export let data: string
    export let code = 0

    let message = {
        0: "No Server Connection",
        404: "Inaccessible Server",
        200: "Connected!"
    }
    
</script>

<div class="grid grid-rows-4 bg-original-card-bg-dark px-20 rounded-lg min-w-full border-1">
    <div class="flex flex-col justify-center items-center text-6xl row-span-2" >
        {#if code === 200}
            <div class="absolute pb-10" in:fade|local={{ delay: 400, duration: 400 }} out:fade|local={{ duration: 400 }}>
                <Icon icon="emojione:white-heavy-check-mark" />
            </div>
        {/if}
        {#if code === 404}
            <div class="absolute pb-10" in:fade|local={{ delay: 400, duration: 400 }} out:fade|local={{ duration: 400 }}>
                <Icon icon="emojione:cross-mark-button" />
            </div>
        {/if}
        {#if code === 0}
            <div class="absolute pb-10" in:fade|local={{ delay: 400, duration: 400 }} out:fade|local={{ duration: 400 }}>
                <Icon icon="codicon:debug-disconnect" />
            </div>
        {/if}
        <span class="absolute text-3xl pt-20">{message[code]}</span>

    </div>
    <div class="row-span-2 flex flex-col-reverse justify-center">
        <input type="text" class="w-full h-10 text-original-base bg-original-fill outline-none rounded-lg border-original-muted hover:bg-original-input-hover text-center" 
        placeholder="Server IP..." bind:value={data}>
    </div>
</div>