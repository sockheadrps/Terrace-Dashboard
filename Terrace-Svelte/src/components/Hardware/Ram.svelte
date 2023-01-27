<script>
    import { onMount, onDestroy } from 'svelte';
    import Chart from 'chart.js/auto';
    let ramUsageChartInstance
    let max_data_points = 25;
    let updateCount = 0;
    let ramChart
    export let ram_data

    $: {
        addData(ram_data)
    }

    let commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        fill: true,
        scales: {
        x: {
            color: "#808080",
            grid: {
                display: false
            },
            ticks: {
                color: "#808080"
            },
        },
        y: {
            beginAtZero: true,
            max: 100,
            grid: {
                color: "rgba(33,31,51,0.2)"
            },
            ticks: {
                color: "#808080"
            },
        }
        },
        legend: {display: false},
        tooltips:{
        enabled: false
        }
    };
      const config = {
        type: 'line',
        data: {
        datasets: [{
        label: "Ram Usage",
        // Line fill
        backgroundColor: "rgba(63, 63, 63, 0.904)",
        // Line Color
        borderColor: "rgba(75, 75, 75, 0.904)",
        data: 0,
        borderWidth: 1,
        pointRadius: 0,
      }]
    },
        options: Object.assign(commonOptions, {
        responsive: true,
        title:{
            display: true,
            text: "RAM Usage",
            fontSize: 18
            }
        })
      };


    function addData(data) {
        if(data && ramUsageChartInstance !== undefined){
            let time = new Date().getHours() + ":" + String(new Date().getMinutes()).padStart(2, "0")

            // Updates datepoints for the chart, up to the max datapoints limit
            if (ramUsageChartInstance.data.labels.length <= max_data_points) {
                ramUsageChartInstance.data.labels.push(time);
                ramUsageChartInstance.data.datasets.forEach((dataset) =>{dataset.data.push(data.ram_percentage)});

            // Shifts the array if it has more values than desired to display
            } else if(ramUsageChartInstance.data.labels.length > max_data_points) {
            ramUsageChartInstance.data.labels.shift();
            ramUsageChartInstance.data.datasets.forEach((dataset) =>{dataset.data.shift()});
            }
        updateCount++;
        ramUsageChartInstance.update();
        }
    };

    function resetRamData() {
        ram_data = [];
    }

    onMount(()=> {
      const ctx = ramChart.getContext('2d');
      // Initialize chart using default config set
      ramUsageChartInstance = new Chart(ctx, config);
    })

    onDestroy(() => resetRamData());

  </script>

<div class="chart__area">
    <div class="title__area">
        <div class="title">RAM</div>
    </div>
    <div class="ram__chart">
        <canvas id="ram__use__chart" bind:this={ramChart} />
    </div>
    <div class="sub__data">
        <div class="data">RAM total: {ram_data ? ram_data.ram_total : ""}GB</div>
        <div class="data">RAM Available: {ram_data ? ram_data.ram_available : ""}GB</div>
        <div class="data">RAM Percentage: {ram_data ? ram_data.ram_percentage : ""}%</div>
    </div>
</div>

<style>
.chart__area {
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 1fr 4fr 2fr;
    align-items: stretch;
    height: 100%;
}

.title__area{
    background: linear-gradient(
        to left top,
         rgba(27, 27, 27, 0.911),
         rgba(20, 20, 20, 0.904)
         );
    border-radius: 2rem 2rem 0rem 0rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.title{
    font-size: 2.5rem;
    font-weight: 600;
}


.sub__data {
    background: linear-gradient(
        to left top,
        rgba(20, 20, 20, 0.904),
        rgba(27, 27, 27, 0.911)
         );
    border-radius: 0rem 0rem 2rem 2rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.data{
    font-size: larger;
    margin: .5rem;
}
</style>
