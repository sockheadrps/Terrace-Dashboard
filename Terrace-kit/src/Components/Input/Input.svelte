<script lang="ts">
	export let value = '';
    export let placeholder = "..."
</script>

<input type="text" class="w-full h-full text-original-base bg-original-fill outline-none border-b-2 border-original-muted hover:bg-original-input-hover" 
placeholder={placeholder} bind:value />

