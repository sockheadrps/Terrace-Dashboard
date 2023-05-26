<script lang="ts">
    import Card from './Components/Card.svelte';
    let serverUrl: string;
    let timerID: number | undefined
    let serverRespCode: number
	import { onMount } from 'svelte'
    import { fade } from 'svelte/transition';
    import { quintIn } from 'svelte/easing';


</script>


<div class="grid grid-rows-6 text-center h-full"
    in:fade={{duration:250, easing: quintIn, delay: 250}}>
    <label class="text-4xl row-span-1 text-original-base my-auto" for="Register">Sign up</label>
    <div class="grid grid-rows-5 row-span-5 justify-items-center">
        <div class="grid grid-flow-col grid-cols-1 row-span-4 mx-auto gap-2 w-3/4">
            <Card bind:data={serverUrl} code={serverRespCode}/>
        </div>
    </div>
</div>

