var ctx = document.getElementById('sensorChart').getContext('2d');

var sensorChart = new Chart(ctx, {
  type: "line",
  data: {
    labels: [],
    datasets: [{ 
      data: [],
      borderColor: "red",
      fill: false, 
      label: 'Heat Sensor'
    }, { 
      data: [],
      borderColor: "green",
      fill: false,
      label: 'Moister Sensor'
    }, { 
      data: [],
      borderColor: "blue",
      fill: false,
      label: 'Water Sensor'
    }]
  },
  options: {
    responsive: true,
    scales: {
      x: {
        type: 'linear',
        position: 'bottom'
      }
    }
  }
});

// window.setInterval(updateChart, 2000);

function updateChart(sensorData) {
    var time = new Date();
    var formattedTime = time.getHours() + ":" + time.getMinutes() + ":" + time.getSeconds();
    
    if (sensorChart.data.labels.length > 15) {
        sensorChart.data.labels.shift();
        sensorChart.data.datasets.forEach(dataset => {
            dataset.data.shift();
        });
    }

    sensorChart.data.labels.push(formattedTime);
    sensorChart.data.datasets[0].data.push(sensorData.sensor1);
    sensorChart.data.datasets[1].data.push(sensorData.sensor2);
    sensorChart.data.datasets[2].data.push(sensorData.sensor3);
    
    sensorChart.update();
}

function updateActuators(sensorData) {
    const threshold_up = 55;
    const threshold_down = 40;
    const actuator1Status = document.getElementById('actuator1-status');
    const actuator2Status = document.getElementById('actuator2-status');
    const actuator3Status = document.getElementById('actuator3-status');

    actuator1Status.textContent = sensorData.sensor1 > threshold_up || sensorData.sensor1 < threshold_down? 'ON' : 'OFF';
    actuator2Status.textContent = sensorData.sensor2 > threshold_up || sensorData.sensor2 < threshold_down? 'ON' : 'OFF';
    actuator3Status.textContent = sensorData.sensor3 > threshold_up || sensorData.sensor3 < threshold_down? 'ON' : 'OFF';
}


// Function to toggle sensor visibility
function toggleSensor(sensorIndex) {
    const dataset = sensorChart.data.datasets[sensorIndex];
    dataset.hidden = !dataset.hidden;
    sensorChart.update();
}

// Event listeners for buttons
document.getElementById('btn-sensor1').addEventListener('click', () => {
    toggleSensor(0);
});
document.getElementById('btn-sensor2').addEventListener('click', () => {
    toggleSensor(1);
});
document.getElementById('btn-sensor3').addEventListener('click', () => {
    toggleSensor(2);
});


// MQTT Setup
const client = mqtt.connect('ws://127.0.0.1:9001/mqtt');

client.on('connect', function () {
    console.log('Connected to MQTT Broker');
    client.subscribe('sensor/data', function (err) {
        if (!err) {
            console.log('Subscribed to topic sensor/data');
        }
    });
});

client.on('message', function (topic, message) {
    if (topic === 'sensor/data') {
        const sensorData = JSON.parse(message.toString());
        console.log('Received sensor data:', sensorData);
        updateChart(sensorData);
        updateActuators(sensorData);
    }
});

