<script>
    let longitude = "";
    let latitude = "";
    let apiKey = "";
    function saveApi() {
        let url = `https://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&appid=${apiKey}`;
        window.localStorage.setItem("weatherAPI", JSON.stringify({'url': url}))
    }

    $: url = `https://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&appid=${apiKey}`;
</script>


<div class="weather_api_area">
    <label for="Weather API">Weather API</label>
    <a href="{url}">{url}</a>
    <form id="weather__api">
        <input type="text" class="search" placeholder="Longitude" name="q" bind:value={longitude}>
        <input type="text" class="search" placeholder="Latitude" name="q" bind:value={latitude}>
        <input type="text" class="search" placeholder="API Key" name="q" bind:value={apiKey}>
    </form>
    <div class="bottom-area">
        <button class="save__btn" type="submit" value="weather__api" on:click={(e) => saveApi(e)}>Save</button>
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

input:hover {
    background: linear-gradient(rgb(37, 37, 37),rgb(51, 51, 51)) padding-box,
                linear-gradient(to right, rgba(61, 61, 61, 0.11), rgba(129, 129, 129, 0)) border-box;
                border-radius: .5rem;

    border: 1px solid transparent;
}
input:focus {
    background: linear-gradient(rgb(43, 43, 43),rgb(66, 66, 66)) padding-box,
                linear-gradient(to right, rgba(61, 61, 61, 0.11), rgba(129, 129, 129, 0)) border-box;
                border-radius: .5rem;

    border-radius: 2rem;
    border: 1px solid rgba(10, 6, 24, 0.021);
    opacity: .7;
    color: #bebebe;
    outline: none;
}
</style>
