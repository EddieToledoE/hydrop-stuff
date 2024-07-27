const mqtt = require('mqtt');
const http = require('http');
const socketIo = require('socket.io');

// Configuración del broker MQTT de CloudAMQP
const brokerUrl = "mqtt://toad.rmq.cloudamqp.com";
const brokerPort = 1883;

// Credenciales MQTT
const username = "jugilxxo:jugilxxo";
const password = "aqvvDO1Y0hq2iW03wmz08TONcWdov1z0";

// Tema MQTT al que suscribirse
const topicPrefix = "hydrop/668dee66cf7b5b0a30fb22a4/";

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

  socket.on('disconnect', () => {
    console.log('Cliente WebSocket desconectado');
  });
});

// Manejar conexión MQTT
client.on('connect', () => {
  console.log("Conectado al broker MQTT!");
  client.subscribe(`${topicPrefix}#`, (err) => {
    if (err) {
      console.error(`Error al suscribirse al tema: ${err}`);
    }
  });
});

// Manejar mensajes MQTT
client.on('message', (topic, message) => {
  const stationId = topic.split('/')[2]; // Extraer el ID de la estación del tema
  console.log(`Mensaje recibido en el tema ${topic}: ${message.toString()}`);

  // Enviar mensaje a todos los clientes en la sala de la estación
  io.to(stationId).emit('mqtt_message', message.toString());
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
