import paho.mqtt.client as mqtt

broker_url = "localhost"  # Endereço IP do HiveMQ
broker_port = 1883  # Porta do HiveMQ
topic_prefix = "irrigation"  # Prefixo dos tópicos a serem inscritos

# Função de callback para quando a conexão MQTT é estabelecida
def on_connect(client, userdata, flags, rc):
    print("Conectado ao HiveMQ")
    # Inscreva-se nos tópicos com base no prefixo
    client.subscribe(topic_prefix + "/#")

# Função de callback para quando uma mensagem MQTT é recebida
def on_message(client, userdata, msg):
    print(f"Mensagem recebida - Tópico: {msg.topic}, Mensagem: {msg.payload.decode()}")
    

# Cria um cliente MQTT
mqtt_client = mqtt.Client()

# Define as funções de callback
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Conecta ao HiveMQ
mqtt_client.connect(broker_url, broker_port, 60)

# Inicia o loop para receber mensagens MQTT
mqtt_client.loop_forever()
