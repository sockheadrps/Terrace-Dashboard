<script>
    import { onMount, onDestroy } from 'svelte';
    import Chart from 'chart.js/auto';
    export let ram_data = []
    let ramUsageChartInstance
    let max_data_points = 10;
    let updateCount = 0;
    let ramChart

    $: {
        ram_data;
        updateData()
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
            text: "RAM Usage",
            fontSize: 18
            }
        }) 
      };


    function addData(data) {
        if(data){
            let today = new Date();
            let time
            if (today.getMinutes < 10){
                time = today.getHours() + ":0" + today.getMinutes();
            }else{
                time = today.getHours() + ":" + today.getMinutes();
            }
            
            if (ramUsageChartInstance.data.labels.length <= max_data_points){
                ramUsageChartInstance.data.labels.push(time);
                ramUsageChartInstance.data.datasets.forEach((dataset) =>{dataset.data.push(data.ram_percentage)});


            } else if(ramUsageChartInstance.data.labels.length > max_data_points){          
            // For shifting the x axis markers
            ramUsageChartInstance.data.labels.shift();
            ramUsageChartInstance.data.datasets.forEach((dataset) =>{dataset.data.shift()});
            }
        updateCount++;
        ramUsageChartInstance.update();
        }
    };

  function updateData() {
    try {
        if (ram_data.ram_total !== undefined){
            console.log(ram_data)
            ram__total.innerHTML = "Ram Total: " + ram_data.ram_total.toString() + "GB"
            ram__available.innerHTML = "Ram available: " + ram_data.ram_available.toString() + "GB"
            ram__used.innerHTML = "Ram Percentage Used: " + ram_data.ram_percentage.toString() + "%"
            addData(ram_data)
            }
        } catch (error) {
            console.log(error)
        }
        
    }    
    
    function resetRamData() {
        ram_data = []
        console.log("destroyed " + ram_data)
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
        <div class="data" id="ram__total" >{ram_data.ram_total}</div>
        <div class="data" id="ram__available">{ram_data.ram_available}</div>
        <div class="data" id="ram__used">{ram_data.ram_percentage}</div>
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
