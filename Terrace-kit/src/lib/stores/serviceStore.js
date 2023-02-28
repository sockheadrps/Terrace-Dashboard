import { writable } from 'svelte/store';

/**
 * @type  {Array.<{name: String, icon: String}>}
 */
let serviceStorage = [];

export function loadServices() {
	if (localStorage.getItem('services') === null) {
		localStorage.setItem('services', JSON.stringify(serviceStorage));
	}
	return JSON.parse(localStorage.getItem('services'));
}

/**
 * @param {Object} newService
 */
export function newService(newService) {
	console.log({ newService });
	serviceStorage = loadServices();
	let index = serviceStorage.findIndex((n) => {
		return newService.name === n.name;
	});
	console.log(index);
	if (index > -1) {
		serviceStorage[index] = newService;
	} else {
		console.log('pushing....');
		serviceStorage.push(newService);
	}
	localStorage.setItem('services', JSON.stringify(serviceStorage));
	serviceList.set(serviceStorage);
}

export function deleteService(name) {
	serviceStorage = JSON.parse(localStorage.getItem('services'));
	let toDelete = serviceStorage.filter((entry) => entry.name === name.name)[0];
	if (toDelete) {
		let filteredServices = serviceStorage.filter((entry) => entry.name !== name.name);
		localStorage.setItem('services', JSON.stringify(filteredServices));
		serviceList.set(filteredServices);
		return toDelete;
	}
}

export function saveServices(services) {
	localStorage.setItem('services', JSON.stringify(services));
}

export let serviceList = writable(serviceStorage);
