<script>
    import { onMount, onDestroy } from 'svelte';
    import Chart from 'chart.js/auto';
    let cpuUsageChartInstance
    let max_data_points = 25;
    let updateCount = 0;
    let cpuChart
    export let cpu_data  

    $: {
        addData(cpu_data)
    }

    // Common Chart Options (Line)
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
        label: "CPU Usage",
        // Line fill
        backgroundColor: "rgba(9, 6, 24, 0.6)",
        // Line Color
        borderColor: "rgba(31, 22, 82, 0.6",
        data: 0,
        borderWidth: 1,
        pointRadius: 0,
      }]
    },
        options: Object.assign(commonOptions, {
        responsive: true,
        title:{
            display: true,
            text: "CPU Usage",
            fontSize: 18
            }
        }) 
      };


    function addData(data) {
        if(data !== undefined && cpuUsageChartInstance !== undefined) {
            let time = new Date().getHours() + ":" + String(new Date().getMinutes()).padStart(2, "0")
            
            // Updates datepoints for the chart, up to the max datapoints limit
            if (cpuUsageChartInstance.data.labels.length <= max_data_points){
                cpuUsageChartInstance.data.labels.push(time);
                cpuUsageChartInstance.data.datasets.forEach((dataset) =>{dataset.data.push(data.cpu_usage)});

            // Shifts the array if it has more values than desired to display
            } else if(cpuUsageChartInstance.data.labels.length > max_data_points){          
            cpuUsageChartInstance.data.labels.shift();
            cpuUsageChartInstance.data.datasets.forEach((dataset) =>{dataset.data.shift()});
            }
        updateCount++;
        cpuUsageChartInstance.update();
        }
    };
    
    function resetCpuData() {
        cpu_data = []
    }

    onMount(()=> {
      const ctx = cpuChart.getContext('2d');
      // Initialize chart using default config set
      cpuUsageChartInstance = new Chart(ctx, config);
    })
    onDestroy(() => resetCpuData());

  </script>

<div class="chart__area">
    <div class="title__area">
        <div class="title">CPU</div>
    </div>
    <div class="cpu__chart">
        <canvas id="cpu__use__chart" bind:this={cpuChart} />
    </div>
    <div class="sub__data">
        <div class="data">Core count: {cpu_data ? cpu_data.cpu_count : ""}</div>
        <div class="data">CPU Usage: {cpu_data ? cpu_data.cpu_usage : ""}%</div>
        <div class="data">CPU Frequency: {cpu_data ? cpu_data.cpu_frequency: ""}Ghz</div>
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
    to bottom,
        rgba(23, 77, 156, 0.384), 
        rgba(31, 22, 82, 0.411)
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
    to top,
        rgba(23, 77, 156, 0.384), 
        rgba(31, 22, 82, 0.411)
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
