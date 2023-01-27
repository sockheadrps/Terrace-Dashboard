<script>
    import { onMount, onDestroy } from 'svelte';
    import Chart from 'chart.js/auto';
    export let disk_data
    let diskUsageChartInstance
    let max_data_points = 10;
    let updateCount = 0;
    let diskChart

    $: {
        addData(disk_data)
    }

    const config = {
        type: 'doughnut',
        responsive: false,
        maintainAspectRatio: false,
        labels: [
            'free',
            'Used'
        ],
        data: {
        datasets: [{
            label: "Storage Usage",
            data: [1, 1],
            backgroundColor: [
                'rgba(189, 27, 15, .4)',
                'rgba(33, 31, 81, .4)',
            ],
            borderColor: "rgba(100, 100, 100, 0.904)",
            hoverOffset: 4
        }]
        },
        options: Object.assign({}, {
        title:{
            display: true,
            text: "Storage Usage",
            fontSize: 18
        }
        })
    };


    function addData(data) {
        if(data && diskUsageChartInstance !== undefined){
            if (diskUsageChartInstance.data.labels.length <= max_data_points){
                diskUsageChartInstance.data.datasets[0].data[0] = data.disk_used;
                diskUsageChartInstance.data.datasets[0].data[1] = data.disk_free;
            }
        updateCount++;
        diskUsageChartInstance.update();
        }
    };

    function resetDiskData() {
        disk_data = [];
    }

    onMount(()=> {
      const ctx = diskChart.getContext('2d');
      // Initialize chart using default config set
      diskUsageChartInstance = new Chart(ctx, config);
    })

    onDestroy(() => resetDiskData());

  </script>

<div class="chart__area">
    <div class="title__area">
        <div class="title">Storage</div>
    </div>
    <div class="disk__chart">
        <canvas id="disk__use__chart" bind:this={diskChart} />
    </div>
    <div class="sub__data">
        <div class="data" id="disk__total" >Disk Total: {disk_data ? disk_data.disk_total :""}GB</div>
        <div class="data" id="disk__available">Disk Availble: {disk_data ? disk_data.disk_free : ""}GB</div>
        <div class="data" id="disk__used">Disk Used: {disk_data ? disk_data.disk_used : ""}GB</div>
        <div class="data" id="disk__percentage">Disk Percentage: {disk_data ? disk_data.disk_percentage : ""}%</div>
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

.disk__chart{
    margin: auto;
    background: rgba(9, 6, 24, 0.048);
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
