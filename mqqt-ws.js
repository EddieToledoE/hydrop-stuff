const mqtt = require('mqtt');
const http = require('http');
const socketIo = require('socket.io');

// Configuración del broker MQTT de CloudAMQP
const brokerUrl = "mqtt://toad.rmq.cloudamqp.com";
const brokerPort = 1883;

// Credenciales MQTT
const username = "jugilxxo:jugilxxo";
const password = "aqvvDO1Y0hq2iW03wmz08TONcWdov1z0";

// Temas MQTT al que suscribirse
const sensorTopic = "hydrop/668dee66cf7b5b0a30fb22a4/6699defcf167387f3335e144/sensor_data";
const pumpStatusTopic = "hydrop/668dee66cf7b5b0a30fb22a4/6699defcf167387f3335e144/pump_status";
const nutrientDispenserStatusTopic = "hydrop/668dee66cf7b5b0a30fb22a4/6699defcf167387f3335e144/nutrient_dispenser_status";
const pumpCommandTopic = "hydrop/668dee66cf7b5b0a30fb22a4/6699defcf167387f3335e144/pump/command";
const nutrientDispenserCommandTopic = "hydrop/668dee66cf7b5b0a30fb22a4/6699defcf167387f3335e144/nutrient_dispenser/command";

// Crear cliente MQTT
const client = mqtt.connect(brokerUrl, {
  port: brokerPort,
  username: username,
  password: password,
});

// Crear servidor HTTP y Socket.io
const server = http.createServer();
const io = socketIo(server, {
  cors: {
    origin: "http://localhost:3000",
    methods: ["GET", "POST"]
  }
});

// Manejar conexión de cliente Socket.io
io.on('connection', (socket) => {
  console.log('Cliente WebSocket conectado');

  socket.on('join_station', (stationId) => {
    console.log(`Cliente unido a la estación: ${stationId}`);
    socket.join(stationId); // Unir al cliente a la sala de la estación
  });

  socket.on('pump_command', (command) => {
    console.log(`Comando de bomba recibido: ${JSON.stringify(command)}`);
    client.publish(pumpCommandTopic, JSON.stringify(command), (err) => {
      if (err) {
        console.error('Error al publicar comando de bomba:', err);
      } else {
        console.log('Comando de bomba publicado:', command);
      }
    });
  });

  socket.on('nutrient_dispenser_command', (command) => {
    console.log(`Comando de dispensador de nutrientes recibido: ${JSON.stringify(command)}`);
    client.publish(nutrientDispenserCommandTopic, JSON.stringify(command), (err) => {
      if (err) {
        console.error('Error al publicar comando de dispensador de nutrientes:', err);
      } else {
        console.log('Comando de dispensador de nutrientes publicado:', command);
      }
    });
  });

  socket.on('disconnect', () => {
    console.log('Cliente WebSocket desconectado');
  });
});

// Manejar conexión MQTT
client.on('connect', () => {
  console.log("Conectado al broker MQTT!");
  client.subscribe([sensorTopic, pumpStatusTopic, nutrientDispenserStatusTopic], (err) => {
    if (err) {
      console.error(`Error al suscribirse al tema: ${err}`);
    }
  });
});

// Manejar mensajes MQTT
client.on('message', (topic, message) => {
  const stationId = topic.split('/')[2]; // Extraer el ID de la estación del tema
  console.log(`Mensaje recibido en el tema ${topic}: ${message.toString()}`);

  if (topic === sensorTopic) {
    io.to(stationId).emit('sensor_data', JSON.parse(message.toString()));
  } else if (topic === pumpStatusTopic) {
    io.to(stationId).emit('pump_status', JSON.parse(message.toString()));
  } else if (topic === nutrientDispenserStatusTopic) {
    io.to(stationId).emit('nutrient_dispenser_status', JSON.parse(message.toString()));
  }
});

client.on('error', (error) => {
  console.error(`Error del cliente MQTT: ${error}`);
});

client.on('close', () => {
  console.log('Conexión con el broker MQTT cerrada');
});

// Iniciar servidor HTTP en el puerto 8080
const PORT = 8080;
server.listen(PORT, () => {
  console.log(`Servidor WebSocket escuchando en el puerto ${PORT}`);
});
