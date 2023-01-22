<script defer>
    import { state } from "../../stores";
    import Cpu from "./Cpu.svelte";
    import Ram from "./Ram.svelte"
    import Storage from "./Storage.svelte";
    let cpu_data
    let ram_data
    let disk_data
    let data = ""



    function update(data) {
        console.log('updating in hardware')
        for (const [key, value] of Object.entries(data)) {
             data[key] = value
            }
        if (data) {
            cpu_data = {"cpu_count": data.cpu_count, "cpu_usage": data.cpu_usage, "cpu_frequency": data.cpu_frequency.current_frequency}
            ram_data = {"ram_total": data.ram_total, "ram_available": data.ram_available, "ram_percentage": data.ram_percentage}
            disk_data = {"disk_total": data.disk_total, "disk_free": data.disk_free, "disk_used": data.disk_used, "disk_percentage": data.disk_percentage}
        }
        
        };

    $: {
        state.subscribe(value => {
            try {
                if (value['hardwareData']){
                    update(value['hardwareData'][0])
                }
            }
            catch (error) {
                console.log(error)
            }
    });
        }

</script>

<div class="chart__area">
    <div class="cpu__chart chart">
        <Cpu cpu_data={cpu_data} />
    </div>
    <div class="ram__chart chart">
        <Ram ram_data={ram_data} />
    </div>
    <div class="disk__chart chart">
        <Storage disk_data={disk_data} />
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
        background: linear-gradient(to right bottom, rgba(31, 22, 82, 0.411), rgba(9, 6, 24, 0.384));
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


