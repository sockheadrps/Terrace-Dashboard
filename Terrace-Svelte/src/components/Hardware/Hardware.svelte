<script>
    import { state } from "../../stores";
    import Cpu from "./Cpu.svelte";
    import Ram from "./Ram.svelte"
    import Storage from "./Storage.svelte";
    let cpu_data
    let ram_data
    let disk_data
    let hardwareData


    function update(data) {
        if (data !== undefined) {
            console.log(data)
            cpu_data = {"cpu_count": data.cpu_count, "cpu_usage": data.cpu_usage, "cpu_frequency": data.cpu_frequency.current_frequency};
            ram_data = {"ram_total": data.ram_total, "ram_available": data.ram_available, "ram_percentage": data.ram_percentage};
            disk_data = {"disk_total": data.disk_total, "disk_free": data.disk_free, "disk_used": data.disk_used, "disk_percentage": data.disk_percentage};
        }
    };


    state.subscribe(value => {
        try {
            if (value['hardwareData'][0] !== undefined) {
                hardwareData = (value['hardwareData'][0])
                update(hardwareData)
            }
        } catch (error) {
            console.log(error)
        }
    });

</script>

<div class="chart__area">
    <div class="cpu__chart chart">
        <Cpu bind:cpu_data={cpu_data} />
    </div>
    <div class="ram__chart chart">
        <Ram bind:ram_data={ram_data} />
    </div>
    <div class="disk__chart chart">
        <Storage bind:disk_data={disk_data} />
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
