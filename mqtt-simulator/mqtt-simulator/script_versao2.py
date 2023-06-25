import paho.mqtt.client as mqtt
import argparse
from pathlib import Path
from simulator import Simulator
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
import json

# Configurações do MQTT
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


# Função para validar o arquivo de configurações
def is_valid_file(parser, arg):
    settings_file = Path(arg)
    if not settings_file.is_file():
        return parser.error(f"argument -f/--file: can't open '{arg}'")
    return settings_file


# Cria um cliente MQTT
mqtt_client = mqtt.Client()

# Define as funções de callback
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Conecta ao HiveMQ
mqtt_client.connect(broker_url, broker_port, 60)

# Inicia o loop para receber mensagens MQTT
mqtt_client.loop_start()


# Configurações do simulador
def default_settings():
    base_folder = Path(__file__).resolve().parent.parent
    settings_file = base_folder / "config/settings.json"
    return settings_file


parser = argparse.ArgumentParser()
parser.add_argument(
    "-f",
    "--file",
    dest="settings_file",
    type=lambda x: is_valid_file(parser, x),
    help="settings file",
    default=default_settings(),
)
args = parser.parse_args()

# Lê as configurações do JSON
with open(args.settings_file) as json_file:
    config = json.load(json_file)

influx_config = config["INFLUX_DB"]
url = influx_config["URL"]
token = influx_config["TOKEN"]
org = influx_config["ORG"]
bucket = influx_config["BUCKET"]

# Cria o ponto de dados
point = Point("weatherstation")
point.tag("location", "San Francisco")

# Adiciona os campos ao ponto de dados com base nas configurações do JSON
for data in influx_config["DATA"]:
    field_name = data["NAME"]
    field_type = data["TYPE"]
    field_value = None

    if field_type == "bool":
        field_value = True
    elif field_type == "int":
        min_value = data.get("MIN_VALUE", 0)
        max_value = data.get("MAX_VALUE", 100)
        field_value = (
            25.9  # Substitua pelo valor adequado ou aplique a lógica necessária
        )
        # Verifique se há uma configuração de passo máximo e aplique-a, se necessário

    point.field(field_name, field_value)

point.time(datetime.utcnow(), WritePrecision.MS)

# Cria o cliente do InfluxDB
client = InfluxDBClient(url=url, token=token, org=org)

# Grava o ponto de dados
