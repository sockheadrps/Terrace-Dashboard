<script>
    import { currentNav } from "../../stores";
    let lat = "39.983334"
    let long = "-82.983330"
    let weatherApiKey = "dbd30986d45f5c219692ea5d83e34a51"
    // const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${long}&appid=${weatherApiKey}`
    let weatherDescription
    let temp
    let feelsLike
    let humidity
    let sunrise
    let sunset
    let wind
    let timeZone
    let iconUrl
    let icon
    // Kelvin to F
    function kelvinToFaren(k) {
        return Math.round(1.8*(k-273) + 32);
    }


        // For sunrise/sunset
    function epochToReadable(epoch) {
    let date = new Date(epoch * 1000);
    let minutes
    // Handles for missing 0 in times like 5:06
    if (date.getMinutes() < 10) {
        minutes = "0" + date.getMinutes()
    } else {
        minutes = date.getMinutes()
    }
    // Converts from 24 hour time to 12 hour time
    if (date.getHours() > 12) {
        return (date.getHours() - 12) + ":" + minutes;
    } else {
        return date.getHours()+ ":" + minutes;
    }
    }

    // For helping getting local time...
    const addZeroIfNeeded = (num) => {
        return (num < 10) ? '0' + num : num.toString();
    }
    let daysOfWeek = {
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
        0: "Sunday"
    }

    let months = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }

    let focusedNav
    const navStore = currentNav.subscribe(value =>{
        focusedNav = value
    })
    // Interval Timer to request Stats
    setInterval(requestTimer, 1000);
    function requestTimer() {
        if (focusedNav ==="Home"){

            let myDate = new Date()
            let hours = addZeroIfNeeded(myDate.getHours());
            if (hours == 0) {
                hours = 12
            }
            if (hours > 12) {
                hours = hours - 12
            }
            let mins = addZeroIfNeeded(myDate.getMinutes());
            let seconds = addZeroIfNeeded(myDate.getSeconds());
            let day = myDate.getDay()
            let dateDay = myDate.getUTCDate()
            let month = myDate.getMonth()
            document.getElementById("time").innerHTML = `${hours}:${mins}:${seconds}`
            document.getElementById("date").innerHTML = `${daysOfWeek[day]}, ${months[month + 1]} ${dateDay} ${myDate.getFullYear()}`
        }
    }


    function saveWeather(data) {
        weatherDescription = data.weather[0].description
        icon = data.weather[0].icon
        iconUrl = "http://openweathermap.org/img/wn/" + icon + "@2x.png"
        temp = data.main.temp
        feelsLike = data.main.feels_like
        humidity = data.main.humidity
        sunrise = data.sys.sunrise
        sunset = data.sys.sunset
        wind = data.wind.speed
        timeZone = data.timezone

        document.getElementById("weather-icon").src = iconUrl
        document.getElementById("temperature").innerHTML = kelvinToFaren(temp) + '&deg;F'
        document.getElementById("feels-like").innerHTML = kelvinToFaren(feelsLike) + '&deg;F'
        document.getElementById("humidity").innerHTML = humidity + "%"
        document.getElementById("wind-speed").innerHTML = wind + "MPH"
        document.getElementById("sunrise").innerHTML = epochToReadable(sunrise) + "AM"
        document.getElementById("sunset").innerHTML = epochToReadable(sunset) + "PM"
    }
    if (document.readyState !== 'loading') {
    initCode();
    } else {
        document.addEventListener('DOMContentLoaded', function () {
            initCode();
        });
    }

    function initCode() {
        try {
        let url = JSON.parse(window.localStorage.getItem("weatherAPI"))
        fetch(url.url)
        .then((response) => response.json())
        .then((data) => saveWeather(data));
        }
        catch (error) {
            console.log("No Weather API set")
        }
    }

</script>

<div class="weather-area">
    <div class="weather-card">
        <div class="temperature-area">
            <h1 id="temperature">73°F</h1>
            <h4>feels like</h4>
            <h2 id="feels-like">60</h2>
            <div>Cloudy</div>
        </div>
        <div class="icon-area">
            <img id="weather-icon" alt="">
        </div>
        <div class="secondary-info">
            <div class="descriptor">
                <div class="title">Humidity</div> 
                <div id="humidity">50%</div>
            </div>
            <div class="descriptor">
                <div class="title">Wind Speed</div>
                <div id="wind-speed">12 mph</div>
            </div>
            <div class="descriptor">
                <div class="title">Sunrise</div>
                <div id="sunrise"> 7:00</div>
            </div>
            <div class="descriptor ">
                <div class="title">Sunset</div>
                <div id="sunset">9:00</div>
            </div>
      </div>

    </div>
    <div class="dt-wrapper">
      <div class="date-time-area">
        <div id="time"></div>
        <div id="date"></div>
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
    background: linear-gradient(to right bottom, rgba(10, 6, 24, 0.75), rgba(10, 6, 24, 0.69));
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

#data {
    text-align: center;
    width: auto;
    min-width: 80px;
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

</style>