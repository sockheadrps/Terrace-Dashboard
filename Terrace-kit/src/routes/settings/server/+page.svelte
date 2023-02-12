<script lang="ts">
    import Card from './Components/Card.svelte';
    let serverUrl: string;
    let timerID: number | undefined
    let serverRespCode: number
    import { websocketConnect, websocketDisconnect, state } from '../../../lib/stores'
	import { onMount } from 'svelte'

    $: console.log($state.websocket, "ws")

    onMount(() => {
        let localStorage: {url:string} | null
        localStorage = JSON.parse(window.localStorage.getItem("server"))
        if (localStorage !== null) {
            serverUrl = localStorage.url
        }
    })
    $: onInput(serverUrl)    
    
    function onInput(url: string) {
        serverRespCode = 0
        clearTimeout(timerID)
        if (url !== undefined) {
            timerID = window.setTimeout(() => {
                console.log(url, "url")
                fetch(url)
                    .then((response) => response)
                    .then((response) => {
                        if (url === "http:/" || url === "http:" || response.status === 404) {
                            serverRespCode = 404
                        }else if (response.status && window.location.origin + "/" !== response.url) {
                            serverRespCode = response.status
                        }else {
                        serverRespCode = 404
                        }
                    }) 
                    .catch((e) => {
                        serverRespCode = 404
                    })
            }, 1500);
        }
    }
    
    $: if (serverRespCode === 200) {
        websocketConnect(serverUrl.replace(/(http)s?:\/\//, "ws://"))
    }
    $: if ($state.message !== undefined && $state.message.event === "SERVER-CONNECT") {
        window.localStorage.setItem("server", JSON.stringify({'url': serverUrl}))
        window.setTimeout(websocketDisconnect, 2000)
    }
</script>


<div class="grid grid-rows-5 text-center h-full">
    <label class="text-6xl row-span-1 pt-10" for="Weather API">Connect to Server</label>
    <div class="grid grid-rows-5 border-1 row-span-3 border-red-700 justify-items-center">
        <div class="grid grid-flow-col grid-cols-1 row-span-4 mx-auto gap-2 w-3/4">
            <Card bind:data={serverUrl} code={serverRespCode}/>
        </div>
    </div>
</div>

