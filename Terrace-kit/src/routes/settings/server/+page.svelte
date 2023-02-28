<script lang="ts">
    import Card from './Components/Card.svelte';
    let serverUrl: string;
    let timerID: number | undefined
    let serverRespCode: number
    import { websocketConnect, websocketDisconnect, state } from '../../../lib/stores'
	import { onMount } from 'svelte'
    import { fade } from 'svelte/transition';
    import { quintIn } from 'svelte/easing';


    onMount(() => {
        let localStorage: {url:string} | null
        localStorage = JSON.parse(window.localStorage.getItem("server"))
        if (localStorage !== null) {
            let regexedUrl = localStorage.url.replace(/(ws)s?:\/\//, "http://")
            console.log({regexedUrl})
            serverUrl = regexedUrl
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
                            console.log(response.status, window.location.origin, response.url)
                            serverRespCode = response.status
                        }else if (response.status == 200) {
                            console.log("we 200")
                            serverRespCode = response.status
                        }else {
                            console.log('else', serverRespCode)
                            console.log(response.status, window.location.origin, response.url)
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
        let regexedUrl = serverUrl.replace(/\/$/, "")
        regexedUrl = regexedUrl.replace(/(http)s?:\/\//, "ws://")
        websocketConnect(regexedUrl)
    }

    $: if ($state.wsMessage !== undefined && $state.wsMessage.event === "SERVER-CONNECT") {
        let regexedUrl = serverUrl.replace(/\/$/, "")
        regexedUrl = regexedUrl.replace(/(http)s?:\/\//, "ws://")
        window.localStorage.setItem("server", JSON.stringify({'url': regexedUrl}))
        window.setTimeout(websocketDisconnect, 1000)
    }
</script>


<div class="grid grid-rows-5 text-center h-full"
    in:fade={{duration:250, easing: quintIn, delay: 250}}>
    <label class="text-6xl row-span-1 py-10" for="Weather API">Connect to Server</label>
    <div class="grid grid-rows-5 row-span-4 justify-items-center">
        <div class="grid grid-flow-col grid-cols-1 row-span-4 mx-auto gap-2 w-3/4">
            <Card bind:data={serverUrl} code={serverRespCode}/>
        </div>
    </div>
</div>

