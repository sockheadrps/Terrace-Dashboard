<script lang="ts">
	import { onMount } from 'svelte';
	import { fade, blur } from 'svelte/transition';
	import { quintIn, quintOut } from 'svelte/easing';
	let timeReady = true;

	let latitude: number;
	let longitude: number;

	function clearTimeouts() {
		const highestId = window.setTimeout(() => {
			for (let i = highestId; i >= 0; i--) {
				window.clearInterval(i);
			}
		}, 0);
	}

	/* import { currentNavStore } from "$lib/stores"; */
	type WeatherApiResponse = {
		current_weather: {
			temperature: number;
			weathercode: number;
			winddirection: number;
		}[];
		main: {
			temp: number;
			feels_like: number;
			humidity: number;
		};
		sys: {
			sunrise: number;
			sunset: number;
		};
		wind: {
			speed: number;
		};
		timezone: string;
	};

	function getLocation() {
		navigator.geolocation.getCurrentPosition((position) => {
			latitude = position.coords.latitude;
			longitude = position.coords.longitude;
		});
	}

	let weatherDescription,
		temp,
		feelsLike,
		humidity,
		sunrise,
		sunset,
		wind,
		timeZone,
		iconUrl,
		icon,
		formattedTime = '',
		formattedDate = '',
		elmWeatherIcon: string,
		elmWeatherIconSrc: string,
		elmTemperature = '73°F',
		elmFeelsLike = '60',
		elmHumidity = '50%',
		elmWindSpeed = '12 mph',
		elmSunrise = '7:00',
		elmSunset = '9:00';

	function weatherApiCall() {
		let url = window.localStorage.getItem("weather")
		if (url !== null){
			fetch(url)
			.then((response) => response.json())
			.then((data) => saveWeather(data));
		}

	}

	function getTime() {
		let myDate = new Date();
		formattedTime = `${myDate
			.toLocaleTimeString(undefined, {
				hour: '2-digit',
				minute: '2-digit',
				second: '2-digit',
				hour12: true
			})
			.replace(/AM|PM/g, '')
			.trim()}`;
		formattedDate = `${myDate.toLocaleDateString(undefined, {
			weekday: 'long',
			month: 'long',
			day: 'numeric',
			year: 'numeric'
		})}`;
		if (!timeReady) timeReady = true;
	}

	function saveWeather(data: WeatherApiResponse) {
		weatherDescription = data.weather[0].description;
		icon = data.weather[0].icon;
		iconUrl = 'http://openweathermap.org/img/wn/' + icon + '@2x.png';
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
		elmTemperature = Math.round(1.8 * (temp - 273) + 32) + ' \u00B0F';
		elmFeelsLike = Math.round(1.8 * (feelsLike - 273) + 32) + ' \u00B0F';
		elmHumidity = humidity + '%';
		elmWindSpeed = wind + 'MPH';
		elmSunrise = new Date(sunrise * 1000).toLocaleTimeString(undefined, {
			hour: '2-digit',
			minute: '2-digit',
			hour12: true
		});
		elmSunset = new Date(sunset * 1000).toLocaleTimeString(undefined, {
			hour: '2-digit',
			minute: '2-digit',
			hour12: true
		});
	}

	onMount(() => {
		clearTimeouts();
		weatherApiCall();
		setInterval(getTime, 1000);
		setInterval(weatherApiCall, 10000);
	});
</script>

<div
	class="grid grid-cols-5 gap-4 text-original-muted justify-center flex-nowrap  rounded-md tablet:h-48"
>
	<div class="w-full bg-original-card-bg-dark pl-4 grid grid-cols-5 col-span-3 rounded-md"
	in:fade={{ duration: 500, easing: quintIn, delay: 200 }}>
		<div class="w-full flex flex-col text-center justify-center col-span-1">
			<h1 id="temperature" class="text-5xl tablet:text-2xl whitespace-nowrap">{elmTemperature}</h1>
			<h4 class="text-2xl tablet:text-sm whitespace-nowrap">feels like</h4>
			<h2 id="feels-like" class="text-xl tablet:text-md whitespace-nowrap">{elmFeelsLike}</h2>
			<div class="tablet:sm">{weatherDescription}</div>
		</div>

		<div class="flex flex-col justify-center">
			<img id="weather-icon" alt={elmWeatherIcon} src={elmWeatherIconSrc} />
		</div>

		<div class="grid grid-cols-2 text-center align-middle col-span-3">
			<div class="my-auto">
				<div class="title text-xl tablet:text-base whitespace-nowrap">Humidity</div>
				<div class="title text-xl tablet:text-base whitespace-nowrap">Wind Speed</div>
				<div class="title text-xl tablet:text-base whitespace-nowrap">Sunrise</div>
				<div class="title text-xl tablet:text-base whitespace-nowrap">Sunset</div>
			</div>
			<div class="my-auto">
				<div id="humidity" class="title text-xl tablet:text-base whitespace-nowrap">{elmHumidity}</div>
				<div id="wind-speed" class="title text-xl tablet:text-base whitespace-nowrap">{elmWindSpeed}</div>
				<div id="sunrise" class="title text-xl tablet:text-base whitespace-nowrap">{elmSunrise}</div>
				<div id="sunset" class="title text-xl tablet:text-base whitespace-nowrap">{elmSunset}</div>
			</div>
		</div>
	</div>
	<div class="grid grid-cols-1 col-span-2 h-full w-full">
		<div class="h-full w-full grid grid-rows-3 gap-4">
			<div
				id="time"
				class="bg-original-card-bg-dark flex justify-center flex-col text-center text-6xl row-span-2 w-full rounded-md tablet:text-4xl"
				in:fade={{ duration: 250, easing: quintIn, delay: 350 }}
				out:fade={{ duration: 100, easing: quintOut }}
			>
					<div in:blur={{ duration: 350, easing: quintIn, delay: 750 }}>
						{formattedTime}
					</div>
			</div>
			<div
				id="date"
				class="bg-original-card-bg-dark flex flex-col text-center text-4xl justify-center rounded-md tablet:text-sm"
				in:fade={{ duration: 250, easing: quintIn, delay: 450 }}
				out:fade={{ duration: 100, easing: quintOut }}
			>
			<div >
				<div in:blur={{ duration: 350, easing: quintIn, delay: 750 }}>
					{formattedDate}
				</div>

			</div>
			</div>
		</div>
	</div>
</div>
