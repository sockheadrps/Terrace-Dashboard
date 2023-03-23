<!-- <script lang="ts">
	import { state, websocketSend } from '../../../lib/stores';
    import { onDestroy, onMount } from 'svelte';
    onMount(() => {
        websocketSend("HARDWARE-REQUEST", {"REQUESTED-CLIENT": "hardware"});
    })
    onDestroy(() => {
        websocketSend("HARDWARE-TERMINATE");
    })

</script> -->
<script>
	import { onDestroy, onMount } from 'svelte';
	import { state, websocketSend } from '$lib/stores';
	import Cpu from './HwTypes/Cpu.svelte';
	import Ram from './HwTypes/Ram.svelte';
	import Storage from './HwTypes/Storage.svelte';
	let cpu_data;
	let ram_data;
	let disk_data;
	let hardwareData;

	onMount(() => {
		websocketSend('HARDWARE-REQUEST', { 'REQUESTED-CLIENT': 'hardware' });
	});
	onDestroy(() => {
		websocketSend('HARDWARE-TERMINATE');
	});

	// Handle WS connection and messages.
	$: if ($state.wsMessage !== undefined) {
		console.log($state.wsMessage);
		switch ($state.wsMessage.event) {
			case 'DISCONNECT':
				websocketSend('CONNECTIONS-REQUEST', {});
				break;
			case 'HARDWARE-DATA':
				console.log('Data, ', $state.wsMessage['data']);
				if ($state.wsMessage['data'] !== undefined) {
					update($state.wsMessage['data']);
					break;
				}
		}
	}

	let data = {
		'cpu-type': 'AMD Ryzen 7 2700X Eight-Core Processor',
		'cpu-count': 16,
		'cpu-freq': 4000,
		'cpu-usage': 20,
		'ram-total': 16,
		'ram-usage': 11.3104515,
		disks: [
			{
				'disk-name': 'C:\\',
				'disk-total': 477,
				'disk-available': 23
			},
			{
				'disk-name': 'D:\\',
				'disk-total': 224,
				'disk-available': 28
			}
		]
	};

	function update(data) {
		if (data !== undefined) {
			cpu_data = {
				cpu_type: data['cpu-type'],
				cpu_count: data['cpu-count'],
				cpu_usage: data['cpu-usage'],
				cpu_frequency: data['cpu-freq']
			};
			let ram_avail = Math.round(data['ram-total'] - data['ram-usage']);
			let ram_percent = (Math.round(data['ram-usage']) / data['ram-total']) * 100;
			ram_data = {
				ram_total: data['ram-total'],
				ram_available: ram_avail,
				ram_percentage: ram_percent
			};
			let disk_used = data.disks[0]['disk-total'] - data.disks[0]['disk-available'];
			let disk_percent = Math.round((disk_used / data.disks[0]['disk-total']) * 100) / 100;
			disk_data = {
				disk_total: data.disks[0]['disk-total'],
				disk_free: data.disks[0]['disk-available'],
				disk_used: disk_used,
				disk_percentage: disk_percent
			};
		}
	}
    update(data)
</script>

<div class="chart__area">
	<div class="cpu__chart chart">
		<Cpu bind:cpu_data />
	</div>
	<div class="ram__chart chart">
		<Ram bind:ram_data />
	</div>
	<div class="disk__chart chart">
		<Storage bind:disk_data />
	</div>
</div>

<style>
	.chart__area {
		display: grid;
		grid-template-columns: 1fr 1fr 1fr;
		align-items: center;
		grid-template-rows: 1fr 8fr 1fr;
		margin-left: 1rem;
		margin-right: 1rem;
	}

	.chart {
		margin-left: 1rem;
		margin-right: 1rem;
		background: rgba(12, 12, 12, 0.918);

		height: 100%;
		border-radius: 2rem;
	}

	.cpu__chart {
		grid-row: 2/3;
		color: #808080;
	}

	.ram__chart {
		grid-column: 2;
		grid-row: 2/3;
		color: #808080;
	}

	.disk__chart {
		grid-column: 3;
		grid-row: 2/3;
		color: #808080;
	}
</style>
