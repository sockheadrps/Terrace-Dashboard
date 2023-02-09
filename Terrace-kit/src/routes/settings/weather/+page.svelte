<script lang="ts">
    import Icon from '@iconify/svelte';
    import { fade } from 'svelte/transition';
    import Card from './Components/Card.svelte';
    let longitude = "";
    let badLong = true
    let latitude = "";
    let badLat = true
    let apiKey = "";
    let badKey = true
    let respCode = 0
    let response = 0
    let codes = {
        200: "Saved",
        401: "Bad API Key!"
    }
    let showFlag = true
    let timeoutId = undefined

    function saveApi() {
        let url = `https://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&appid=${apiKey}`;
        window.localStorage.setItem("weatherAPI", JSON.stringify({'url': url}))
    }


    function checkApi() {
        console.log(apiKey.length)
        // let url = `https://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&appid=${apiKey}`;
        let url = `https://api.open-meteo.com/v1/forecast?latitude=39&longitude=-83&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m` 

         return fetch(url)
                .then((response) => response.json())
                .then((data) => console.log(data))
    }

    checkApi()


    $: {
        if (timeoutId){
                clearTimeout(timeoutId)
                timeoutId = undefined
                console.log('timer canceled')
        }
        if (respCode === 200) {
            timeoutId = setTimeout(() => {
            showFlag = false
            }, 1000)
        } else{
            showFlag = true
        }
    }

        
</script>


<div class="grid grid-rows-5 text-center h-full">
    <label class="text-6xl row-span-1 pt-10" for="Weather API">Weather API</label>
    <div class="grid grid-rows-5 border-1 row-span-4 border-red-700 justify-items-center">
        <div class="grid grid-cols-3 gap-x-20 row-span-2 mx-auto ">
            <Card bind:data={latitude} dataName={"Latitude"} checkInput={async(value) => 
                isNaN(value) || parseFloat(value) > 90 || parseFloat(value) < -90
            } />
            <Card bind:data={longitude} dataName={"Longitude"} checkInput={async(value) => 
                isNaN(value) || parseFloat(value) > 180 || parseFloat(value) < -180
            } />
            <Card bind:data={apiKey} dataName={"API Key"} checkInput={async (value) => value.length === 32 && (response = await checkApi(value)) === 200} />
        </div>
        <div class="row-span-2 w-1/2">
            {#if response === 200}
                <div class="bg-green-500 border-2 h-10 mx-20"></div>
            {:else if (response === 401 || response === 400)}
                <div class="bg-yellow-500 border-2 h-10 mx-20"></div>
            {:else}
                <div class="opacity-0 border-2 h-10 mx-20"></div>
            {/if}


        </div>
    </div>
</div>


    <!-- <div class="">
        <div class="input__area">
            <div class="icon">
                {#if !badLat && latitude}
                    <div in:fade>
                        <Icon icon="emojione:white-heavy-check-mark" />
                    </div>
                {/if}
                {#if badLat && latitude}
                    <div in:fade>
                        <Icon icon="emojione:cross-mark-button" />
                    </div>
                {/if}
            </div>
            <h1>Latitude</h1>
                <input out:fade type="text" class="search {badLat ? "bad__input": "good__input"} {latitude ? "" : "no__input"}" 
                placeholder="Latitude" name="q" bind:value={latitude} on:input={checkInput}>
        </div>

        <div class="input__area">
            <div class="icon" >
                {#if !badLong && longitude}
                    <div in:fade>
                        <Icon icon="emojione:white-heavy-check-mark" />
                    </div>
                {/if}
                {#if badLong && longitude}
                    <div in:fade>
                        <Icon icon="emojione:cross-mark-button" />
                    </div>
                {/if}

            </div>
            <h1>Longitude</h1>

                <input out:fade type="text" class="search {badLong ? "bad__input": "good__input"} {longitude ? "" : "no__input"}"
                placeholder="Longitude" name="q" bind:value={longitude} on:input={checkInput}>
        </div>

        <div class="input__area">
            <div class="icon">
                {#if respCode == 200}
                <div in:fade>
                    <Icon icon="emojione:white-heavy-check-mark" />
                </div>
                {/if}
                {#if respCode == 401}
                <div in:fade>
                    <Icon icon="emojione:slightly-frowning-face" />
                </div>
                {/if}
                {#if respCode == 0 && apiKey}
                <div in:fade>
                    <Icon icon="emojione:cross-mark-button" />
                </div>
                {/if}
            </div>
            <h1>API Key</h1>
                <input out:fade type="text" class="search {respCode === 200 ? "good__input" : ""} {respCode === 401 ? "error__input" : ""} 
                {respCode === 0 && apiKey ? "bad__input" : ""}" 
                placeholder="API Key" name="q" bind:value={apiKey} on:input={checkApiKey}>
        </div>
    </div> -->
<!--         
    <div class="bottom-area">
        {#if respCode !== 0 && showFlag}
            <div on:load={() => console.log('hi')} transition:fade class="flag" 
            class:good__input={respCode === 200} class:error__input={respCode === 401} class:bad__input={respCode === 0}>
            {codes[respCode]}
            </div>
        {/if}
    </div> -->


<!-- <style>

.bottom-area {
    margin-top: 4rem;
    text-align: center;
}

.inputs{
    height: 100px;
}
.input__area {
    display: inline-block;
    min-width: 200px;

}

.flag {
    display: inline-block;
    margin-top: 3rem;
    border-radius: .5rem;
    width: 16rem;
    height: 2.5rem;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
    border: 1px solid rgba(10, 6, 24, 0.021);
    background:rgba(125, 125, 129, 0.1);
    transition: all .01s ease-out;
    font-size: larger;
    color: rgb(136, 136, 136);
}

.icon {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 100px;
    font-size: 30px;
    text-align: end;
}

h1 {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    font-size: 30px;
    text-align: end;
}


label{
    margin-bottom: 2rem;
    font-size: 40px;
}

input {
    display: inline-block;
    background-color: rgb(26, 27, 31);
    border-radius: .5rem;
    text-align: center;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
    border: 1px solid rgba(10, 6, 24, 0.021);
    background:rgba(64, 64, 73, 0.1);
    color: #808080;
    height: 2rem;
}

.bad__input {
    background:rgba(151, 80, 59, 0.493);
}

.good__input {
    background:rgba(59, 151, 79, 0.253);
}

.error__input {
    background:rgba(173, 133, 4, 0.568);
}

.no__input {
    background:rgba(64, 64, 73, 0.1);
}

input:hover {
    opacity: .6;
    border: 1px solid transparent;
}
input:focus {
    border-radius: 2rem;
    border: 1px solid rgba(10, 6, 24, 0.021);
    opacity: .7;
    color: #bebebe;
    outline: none;
}
</style> -->
