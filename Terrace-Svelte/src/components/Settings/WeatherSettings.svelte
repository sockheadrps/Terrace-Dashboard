<script>
    let longitude = ""
    let latitude = ""
    let apiKey = ""
    function saveApi() {
        let url = `https://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&appid=${apiKey}`
        window.localStorage.setItem("weatherAPI", JSON.stringify({'url': url}))
    }

    $: url = `https://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&appid=${apiKey}`
</script>


<div class="weather_api_area">
    <label for="Weather API">Weather API</label>
    <a href="{url}">{url}</a>
    <form id="weather__api">
        <input type="text" class="search" placeholder="Longitude" name="q" bind:value={longitude}>
        <input type="text" class="search" placeholder="Latitude" name="q" bind:value={latitude}>
        <input type="text" class="search" placeholder="API Key" name="q" bind:value={apiKey}>
    </form>
    <button class="save__btn" type="submit" value="weather__api" on:click={(e) => saveApi(e)}>Save</button>

</div>



<style>

#weather__api {
    margin-top: 2rem;

}
.weather_api_area {
    margin-top: 6rem;
}

.save__btn {
    margin-top: 1rem;
    border-radius: .5rem;
    text-align: center;
    width: 25%;
    height: 25%;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
    border: 1px solid rgba(10, 6, 24, 0.021);
    background: rgb(24, 13, 70);    
    cursor: pointer;
    transition: all .2s ease-out;
    font-size: larger;
    color: rgb(136, 136, 136);
}

.save__btn:hover {
    background: linear-gradient(rgba(10, 6, 24, 0.904),rgba(10, 6, 24, 0.877)) padding-box,
                linear-gradient(to right, rgba(50, 2, 94, 0.774), rgb(26, 28, 143)) border-box;
                border-radius: .5rem;

    border: 1px solid transparent;
    opacity: .99;
    color: #525151;
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
}

input:focus {
    background: linear-gradient(rgba(55, 43, 100, 0.904),rgba(45, 26, 112, 0.877)) padding-box,
                linear-gradient(to right, rgba(50, 2, 94, 0.774), rgb(26, 28, 143)) border-box;
    border-radius: 2rem;
    border: 1px solid rgba(10, 6, 24, 0.021);

    opacity: .7;
    color: #525151;
    outline: none;
}
</style>