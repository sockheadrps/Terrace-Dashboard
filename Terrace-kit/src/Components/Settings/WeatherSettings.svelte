<script>
    import Input from "../Input/Input.svelte";
    let longitude = "";
    let badLong = true
    let latitude = "";
    let badLat = true
    let apiKey = "";
    let badKey = true
    let respCode = 0
    function saveApi() {
        let url = `https://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&appid=${apiKey}`;
        window.localStorage.setItem("weatherAPI", JSON.stringify({'url': url}))
    }

    function checkStorageForApi() {
        window.localStorage.getItem("weatherAPI")
        console.log(window.localStorage.getItem("weatherAPI"))
    }
    checkStorageForApi()
    function checkLat() {
        if (isNaN(parseFloat(latitude)) || parseFloat(latitude) > 90 || parseFloat(latitude) < -90) 
            badLat = true
        else
            badLat = false
    }

    function checkLong() {
        if (isNaN(parseFloat(longitude)) || (parseFloat(longitude) > 180 || parseFloat(longitude) < -180))
            badLong = true
        else 
             badLong = false
    }

    function checkApiKey() {
        if (apiKey.length !== 32)
            badKey = true
        else
            badKey = false
    }

    function checkApi() {
        let url = `https://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&appid=${apiKey}`;

         return fetch(url)
                .then((response) => response.json())
                .then((data) => data.cod)
    }

    $: url = `https://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&appid=${apiKey}`;

    $: {
        if(!badKey && !badLat && !badLong) {
            checkApi().then((code) => {
                respCode = code
            })
        } else {
            respCode = 0
        }
    }

    $: respCode = respCode
    
</script>

<!-- <div class="weather_api_area">
    <label for="Weather API">Weather API</label>
    <a href="{url}">{url}</a>
    <form id="weather__api">
        <input type="text" class="search {badLat === true ? "bad__input": ""} {badLat === false ? "good__input": ""} {latitude === "" ? "no__input" : ""}" 
        placeholder="Latitude" name="q" bind:value={latitude} on:input={checkLat}>

        <input type="text" class="search {badLong === true ? "bad__input": ""} {badLong === false ? "good__input": ""} {longitude === "" ? "no__input" : ""}"
        placeholder="Longitude" name="q" bind:value={longitude} on:input={checkLong}>
        
        <input type="text" class="search {badKey === true ? "bad__input": ""} {badKey === false ? "good__input": ""} {apiKey === "" ? "no__input" : ""}" placeholder="API Key" name="q" bind:value={apiKey} on:input={checkApiKey}>
    </form>
    <div class="bottom-area">
        <button class="save__btn {respCode === 200 ? "good__input" : ""} {respCode === 401 ? "error__input" : ""} {respCode === 0 ? "bad__input" : ""}" 
        type="submit" value="weather__api" on:click={() => saveApi()}>Save</button>
    </div>
</div> -->

<div class="h-full grid grid-rows-6">
    <div class="row-start-2 row-span-4 w-full bg-slate-500 grid grid-rows-3 gap-4 items-center justify-center">
        <label for="Weather API" class="border-2 border-red-500">Weather Api</label>
        <div class="row-span-3 border-2 border-green-500">01</div>
    </div>
</div>

<style>

#weather__api {
    margin-top: 2rem;

}
.weather_api_area {
    margin-top: 6rem;
    display: flex;
    flex-direction: column;
}

.bottom-area {
    text-align: center;
}

.save__btn {
    margin-top: 1rem;
    border-radius: .5rem;
    text-align: center;
    width: 16rem;
    height: 2.5rem;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
    border: 1px solid rgba(10, 6, 24, 0.021);
    background:rgba(125, 125, 129, 0.1);
    cursor: pointer;
    transition: all .01s ease-out;
    font-size: larger;
    color: rgb(136, 136, 136);
}

.save__btn:hover {
    background: linear-gradient(rgb(37, 37, 37),rgb(51, 51, 51)) padding-box,
                linear-gradient(to right, rgba(61, 61, 61, 0.11), rgba(129, 129, 129, 0)) border-box;
                border-radius: .5rem;

    border: 1px solid transparent;
    color: #e9e9e9;
}

label{
    margin-bottom: 2rem;
    font-size: 40px;
}

input {
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
    background:rgba(151, 80, 59, 0.884);
}

.good__input {
    background:rgba(59, 151, 79, 0.568);
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
</style>