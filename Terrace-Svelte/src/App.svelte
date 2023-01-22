<script>
    import Board from "./components/Board/Board.svelte";
	import Background from "./components/BackGrnd/BackGrnd.svelte";
	import {connect, state} from './stores.js'

	connect()


</script>

<main>
	<Background />
	<Board />
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		/* max-width: 240px; */
		margin: 0 auto;
	}
	@media (min-width: 640px) {
		main {
			max-width: 700;
		}
	}
</style>