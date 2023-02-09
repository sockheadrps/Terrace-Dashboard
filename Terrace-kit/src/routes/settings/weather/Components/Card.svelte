<script lang="ts">
    import Icon from '@iconify/svelte';
    import { fade } from 'svelte/transition';
    let badVal = true
    export let data: string
    export let dataName: string
    export let checkInput: (a: string) => Promise<boolean>

    $: console.log({badVal, data})
    $: checkInput(data).then((result:boolean) => badVal = result)

</script>

<div class="grid grid-rows-3">
    <div class="flex justify-center items-center text-6xl">
        {#if !badVal && data || badVal === 200}
            <div in:fade>
                <Icon icon="emojione:white-heavy-check-mark" />
            </div>
        {/if}
        {#if badVal && data.length !== 32 && data.length !== 0}
            <div in:fade>
                <Icon icon="emojione:cross-mark-button" />
            </div>
        {/if}
        {#if badVal === 401}
            <div in:fade>
                <Icon icon="emojione:slightly-frowning-face" />
            </div>
        {/if}
    </div>
    <h1 class="text-4xl">{dataName}</h1>
    <div class="row-span-1">
        <input out:fade type="text" class="w-full h-10 text-original-base bg-original-fill outline-none border-b-2 border-original-muted hover:bg-original-input-hover text-center {badVal ? "bad__input": "good__input"} {data ? "" : "no__input"}" 
        placeholder={dataName} bind:value={data}>
    </div>
        
</div>