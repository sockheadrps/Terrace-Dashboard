//Websocket connection
var socket = new WebSocket("ws://localhost:80/ws/stats");

// On open function
socket.onopen = function(event) {
  console.log('connect on open')
  socket.send(JSON.stringify({event: "CONNECT", "client-type": "DASHBOARD"}));
};

window.addEventListener('beforeunload', function (e) {
  e.preventDefault();
  socket.send(JSON.stringify({event: "DISCONNECT", "client-type": "DASHBOARD"}));
  socket.close()
});

// Setting up HTML Elements

let cpu_count = document.getElementById("cpu_count")
let cpu_usage = document.getElementById("cpu_usage")
let cpu_frequency = document.getElementById("cpu_frequency")
let core_temperature = document.getElementById("core_temperature")
let ram_total = document.getElementById("ram_total")
let ram_availble = document.getElementById("ram_available")
let ram_percentage = document.getElementById("ram_percentage")
let disk_total = document.getElementById("disk_total")
let disk_free = document.getElementById("disk_free")
let disk_used = document.getElementById("disk_used")
let disk_percentage = document.getElementById("disk_percentage")
let clients = []
const services = document.getElementById('services');
const hwButtons = document.getElementsByClassName("hw-clients")[0]
let serviceClients = []
let hwClients = []
let homePage = document.getElementsByClassName('home')[0]
let statsPage = document.getElementsByClassName('stats')[0]
let backButton = document.getElementsByClassName('back-overlay')[0]
let notesButton = document.getElementsByClassName("notes-btn")[0]
let serviceArea = document.getElementsByClassName("services-area")[0]

backButton = document.getElementsByClassName('back-overlay')[0]
backButton.addEventListener('click', () => {
  homePage.classList.toggle('hidden');
  statsPage.classList.toggle('hidden');
  backButton.classList.toggle('hidden')
});


function addService(serviceName) {
  for (i of serviceClients){
    let newService = document.createElement("div")
    newService.classList.add("service")
    newService.setAttribute("id", i)
    newService.innerText = serviceName
    serviceArea.appendChild(newService)
  }

}


let statsPageState = document.getElementsByClassName('stats')[0]
let backButtonState = document.getElementsByClassName('back-overlay')[0]
let currentHardware 

backButton.addEventListener('click', () => {
  socket.send(JSON.stringify({event: "HARDWARE-TERMINATE", "requested-client": currentHardware }));
  currentHardware = null
})


function addHwButtons(hwClients) {
  // check if a new client has connected vs hwClientslist
  for (i of hwClients){
    let new_hw = document.createElement("button")
    let lightDiv = document.createElement("div")
    let nameSpan = document.createElement("span")
    lightDiv.classList.add("light")
    new_hw.classList.add('btn')
    nameSpan.classList.add("label")
    new_hw.id = i
    nameSpan.innerText = i
    new_hw.append(nameSpan)
    new_hw.append(lightDiv)
    hwButtons.append(new_hw)
    new_hw.addEventListener('click', () => {
      homePage.classList.toggle('hidden');
      statsPage.classList.toggle('hidden');
      backButton.classList.toggle('hidden');

      if (!statsPageState.classList.contains('hidden')){
        socket.send(JSON.stringify({event: "HARDWARE-REQUEST", "requested-client": i }));
        currentHardware = i
      }
    });
  }
}


// Main Websocket Communication
socket.onmessage = function(event) {
    let data = JSON.parse(event.data);
    console.log(data)


    switch(data.event) {
      case "CONNECT":
        if (data['client-type'] === "HARDWARE") {
          hwClients.push(data["client-name"])
          addHwButtons(hwClients)
        } else if (data["client-type"] === "SERVICE") {
          serviceClients.push(data["client-name"])
          console.log(serviceClients)
          addService(serviceClients)
        }

        if (data['hardware-list']){
          for (let i of data['hardware-list']) {
            console.log(i)
            if (!hwClients.includes(i)){
              hwClients.push(i)
            }
          }
          addHwButtons(hwClients)
        }
        if (data['service-list']){
          for (let i of data['service-list'])
            if (!serviceClients.includes(i)){
              serviceClients.push(i)
              console.log(i)
            }
          addService(serviceClients)
        }
        break;

      case "DISCONNECT":
        if (data['client-type'] === "HARDWARE") {
        hwClients = hwClients.filter(item => item !== data['client-name'])
        document.getElementById(data['client-name']).remove()
        } else if (data["client-type"] === "SERVICE") {
          serviceClients = serviceClients.filter(item => item !== data['client-name'])
          document.getElementById(data['client-name']).remove()
        }        
        break;
    }

    if (data.event === 'HARDWARE-DATA') {
      updateData(data.data)
    }

};

window.onbeforeunload = function() {
  socket.onclose = function () {}; // disable onclose handler first
  websocket.close();
};


// Chart configs
let updateInterval = 1000 //in ms
let max_data_points = 60;


//Globals
let updateCount = 0;


// Chart Objects
let cpuUsageChart = document.getElementById("cpuUsage");
let ramUsageChart = document.getElementById("ramUsage");
let diskUsageChart = document.getElementById("diskUsage");


// Common Chart Options (Line)
let commonOptions = {
    responsive: true,
    maintainAspectRatio: false,
    // Line fill
    backgroundColor: "rgba(2, 2, 2, 0.8)",
    // Line Color
    borderColor: "#808080",
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


// cpuUsageChart Instance
var cpuUsageChartInstance = new Chart(cpuUsageChart, {
    type: 'line',
    data: {
      datasets: [{
          label: "CPU Usage",
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
});

// ramUsageChart Instance
var ramUsageChartInstance = new Chart(ramUsageChart, {
    type: 'line',
    data: {
      datasets: [{
          label: "RAM Usage",
          data: 0,
          borderWidth: 1,
          pointRadius: 0,
      }]
    },
    options: Object.assign(commonOptions, {
      title:{
        display: true,
        text: "RAM Usage",
        fontSize: 18
      }
    })
});

// diskUsageChart Instance
var diskUsageChartInstance = new Chart(diskUsageChart, {
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
            'rgba(189, 27, 15, .8)',
            'rgba(33, 31, 81, .9)',
          ],
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
});

// Function to push data to chart object instances
function addData(data) {
    if(data){
        let today = new Date();
        let time
        if (today.getMinutes < 10){
            time = today.getHours() + ":0" + today.getMinutes();
        }else{
            time = today.getHours() + ":" + today.getMinutes();
        }
        
        if (cpuUsageChartInstance.data.labels.length <= max_data_points){
            // CPU Usage
            cpuUsageChartInstance.data.labels.push(time);
            cpuUsageChartInstance.data.datasets.forEach((dataset) =>{dataset.data.push(data.cpu_usage)});

            // RAM Usage
            ramUsageChartInstance.data.labels.push(time);
            ramUsageChartInstance.data.datasets.forEach((dataset) =>{dataset.data.push(data.ram_percentage)});

            // Disk Usage
            diskUsageChartInstance.data.datasets[0].data[0] = data.disk_used;
            diskUsageChartInstance.data.datasets[0].data[1] = data.disk_free;

        } else if(cpuUsageChartInstance.data.labels.length > max_data_points){          
          // For shifting the x axis markers
          // CPU Usage
          cpuUsageChartInstance.data.labels.shift();
          cpuUsageChartInstance.data.datasets.forEach((dataset) =>{dataset.data.shift()});
        
          // RAM Usage
          ramUsageChartInstance.data.labels.shift();
          ramUsageChartInstance.data.datasets[0].data.shift();
        }
      updateCount++;
      cpuUsageChartInstance.update();
      ramUsageChartInstance.update();
      diskUsageChartInstance.update();
      }
  };

  // Update HTML elements
function updateData(data) {
    addData(data)
    cpu_count.innerHTML = "Core count: " + data.cpu_count.toString()
    cpu_usage.innerHTML = "CPU usage: " + data.cpu_usage.toString() + "%"
    cpu_frequency.innerHTML = "CPU Frequency: " + data.cpu_frequency.current_frequency.toString() + " GHz"
    ram_total.innerHTML = "RAM total: " +  data.ram_total.toString() + " GB"
    ram_available.innerHTML = "RAM Available: " + data.ram_available.toString() + " GB"
    ram_percentage.innerHTML = "Percentage of RAM used: " + data.ram_percentage.toString() + "%"
    disk_total.innerHTML = "Storage space total: " + data.disk_total.toString() + " GB"
    disk_free.innerHTML = "Storage Space Free: " + data.disk_free.toString() + " GB"
    disk_used.innerHTML = "Storage Space used: " + data.disk_used.toString() + " GB"
    disk_percentage = "Storage Space Used: "+ data.disk_percentage.toString() + "%"
}
updateData()