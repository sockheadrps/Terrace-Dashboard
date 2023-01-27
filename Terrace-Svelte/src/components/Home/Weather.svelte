<script>
    import { currentNavStore } from "../../stores";
    let lat = "39.983334",
        long = "-82.983330",
        weatherApiKey = "dbd30986d45f5c219692ea5d83e34a51",
        weatherDescription, temp, feelsLike, humidity, sunrise, sunset, wind, timeZone, iconUrl, icon, formattedTime = "", formattedDate = "", focusedNav,
        elmWeatherIcon, elmWeatherIconSrc,
        elmTemperature = "73°F",
        elmFeelsLike = "60",
        elmHumidity = "50%",
        elmWindSpeed = "12 mph",
        elmSunrise = "7:00",
        elmSunset = "9:00";


    function weatherApiCall() {
        let url = JSON.parse(window.localStorage.getItem("weatherAPI"));
        fetch(url.url)
                .then((response) => response.json())
                .then((data) => saveWeather(data))
    }

    setInterval(() => {
        try {
            weatherApiCall()
            } catch (error) {
                console.log("No Weather API set")
            }
    }, 5000)

    setInterval(() => {
        if ($currentNavStore == "Home") {
            let myDate = new Date();
            formattedTime = `${myDate.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true }).replace(/AM|PM/g, "").trim()}`;
            formattedDate = `${myDate.toLocaleDateString(undefined, { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' })}`;
        }
    }, 1000);

    function saveWeather(data) {
        weatherDescription = data.weather[0].description;
        icon = data.weather[0].icon;
        iconUrl = "http://openweathermap.org/img/wn/" + icon + "@2x.png";
        temp = data.main.temp;
        feelsLike = data.main.feels_like;
        humidity = data.main.humidity;
        sunrise = data.sys.sunrise;
        sunset = data.sys.sunset;
        wind = data.wind.speed;
        timeZone = data.timezone;
        //Math.round(1.8 * (k - 273) + 32)
        elmWeatherIcon = icon;
        elmWeatherIconSrc = iconUrl;
        elmTemperature = Math.round(1.8 * (temp - 273) + 32) + ' \u2109';
        elmFeelsLike = Math.round(1.8 * (feelsLike - 273) + 32) + ' \u2109';
        elmHumidity = humidity + "%";
        elmWindSpeed = wind + "MPH";
        elmSunrise = new Date(sunrise * 1000).toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit', hour12: true });
        elmSunset = new Date(sunset * 1000).toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit', hour12: true });
    }

    function initCode() {
        try {
            weatherApiCall()
            } catch (error) {
                console.log("No Weather API set")
            }
    }

</script>

<svelte:window on:load={initCode()} />

<div class="weather-area">
    <div class="weather-card">
        <div class="temperature-area">
            <h1 id="temperature">{elmTemperature}</h1>
            <h4>feels like</h4>
            <h2 id="feels-like">{elmFeelsLike}</h2>
            <div>Cloudy</div>
        </div>
        <div class="icon-area">
            <img id="weather-icon" alt={elmWeatherIcon} src={elmWeatherIconSrc}>
        </div>
        <div class="secondary-info">
            <div class="descriptor">
                <div class="title">Humidity</div>
                <div id="humidity">{elmHumidity}</div>
            </div>
            <div class="descriptor">
                <div class="title">Wind Speed</div>
                <div id="wind-speed">{elmWindSpeed}</div>
            </div>
            <div class="descriptor">
                <div class="title">Sunrise</div>
                <div id="sunrise">{elmSunrise}</div>
            </div>
            <div class="descriptor ">
                <div class="title">Sunset</div>
                <div id="sunset">{elmSunset}</div>
            </div>
      </div>

    </div>
    <div class="dt-wrapper">
        <div class="date-time-area">
            <div id="time">{formattedTime}</div>
            <div id="date">{formattedDate}</div>
        </div>
    </div>
</div>

<style>
.weather-area {
    user-select: none;
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    justify-content: center;
    background: linear-gradient(
        to left top,
         rgba(24, 24, 24, 0.822),
         rgba(15, 15, 15, 0.863)
         );
    border-radius: 2rem;
    margin: 0rem 2rem;
    padding: 2rem;
    height: auto;
    width: auto;
    color: #808080;
    align-items: center;
}

.temperature-area {
    display: flex;
    flex-direction: column;
    margin-right: 1rem;
    justify-content: center;
}

.weather-card {
    margin-left: 2rem;
    display: flex;
    justify-content: space-evenly;
    justify-content: start;
    width: 100%;
    height: 100%;
}

.icon-area{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin: auto;
}

.secondary-info{
    width: auto;
    display: flex;
    flex-flow: column;
    margin-left: 2rem;
    min-width: 150px;
    margin: auto;
}

.title {
    width: auto;
    min-width: 150px;
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    align-items: flex-start;
}

.descriptor {
    display: flex;
    align-items: left;
}

.dt-wrapper {
    /* border: 1px solid rgb(245, 245, 245);  */
    height: 100%;
    width: 100%;
    margin: auto;
    min-width: 350px;
}


.date-time-area {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: auto;
    height: 100%;
}

#time {
    justify-content: center;
    font-size: 45px;
}

#date {
    font-size: 25px;
}

h1{
    white-space: nowrap;
}

.secondary-info > div {
    white-space: nowrap;
}

</style>
