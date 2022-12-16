// Weather API
import {lat, long, weatherApiKey} from "/static/weatherAPI.js";
const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${long}&appid=${weatherApiKey}`


let statsButton = document.getElementsByClassName("stats-btn")[0]

const translateAmount = 100;
let translate = 0;


let home = document.getElementsByClassName("home")
let stats = document.getElementsByClassName ("stats")


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

document.addEventListener('DOMContentLoaded', function() {
  fetch(url)
  .then((response) => response.json())
  .then((data) => saveWeather(data));
});


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
  7: "Sunday"
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


// Interval Timer to request Stats
setInterval(requestTimer, 1000);
function requestTimer() {
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

