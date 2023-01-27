<script>
	import Children from 'svelte-exmarkdown/renderer/Children.svelte';
	export let children;
</script>

<code>{children[0].value}</code>

<style>
	code {
		background-color: #111;
		color: #EEE;
		padding: 3px;
		border-radius: 4px;
	}
</style>

