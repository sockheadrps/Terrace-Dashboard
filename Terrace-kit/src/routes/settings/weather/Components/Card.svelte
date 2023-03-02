<script lang="ts">
    import Icon from '@iconify/svelte';
	import { getContext } from 'svelte';
    let badVal = true
    export let data: string
    export let dataName: string
    export let checkInput: (a: string) => Promise<boolean>

    $: checkInput(data).then((result:boolean) => badVal = result)
    $: respCode = getContext('respCode')

    

</script>

<div class="h-full grid grid-rows-3">
    <div class="flex justify-center items-center md:text-6xl text-4xl">
        {#if !badVal && data}
            <div>
                <Icon icon="emojione:white-heavy-check-mark" />
            </div>
        {/if}
        {#if badVal && data.length !== 32 && data.length !== 0}
            <div>
                <Icon icon="emojione:cross-mark-button" />
            </div>
        {/if}
    </div>
    <h1 class="md:text-4xl text-2xl">{dataName}</h1>
    <div>
        <input type="text" class="w-full h-10 text-original-base bg-original-fill outline-none border-b-2 border-original-muted hover:bg-original-input-hover text-center {badVal ? "bad__input": "good__input"} {data ? "" : "no__input"}" 
        placeholder={dataName} bind:value={data}>
    </div>
        
</div>