<script lang="ts">
	export let value = '';
    export let placeholder = "..."
    import Icon from "@iconify/svelte";
</script>


<div class="flex flex-row justify-between h-12 mt-4">
    <div class="text-3xl inline-block relative">
        <div class="absolute top-1/2 -translate-y-1/2 text-original-muted pl-4">
            <Icon icon="material-symbols:search" />
        </div>
    </div>
    <div class="w-full">
        <input type="text" class="h-full w-full inline-block rounded-md text-original-base bg-original-card-bg-dark outline-none hover:bg-original-input-hover pl-14" 
        placeholder={placeholder} bind:value />
    </div>
</div>


