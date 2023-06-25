import paho.mqtt.client as mqtt
import argparse
from pathlib import Path
from simulator import Simulator
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import json

# Configurações do MQTT
broker_url = "localhost"  # Endereço IP do HiveMQ
broker_port = 1883  # Porta do HiveMQ
topic_prefix = "irrigation"  # Prefixo dos tópicos a serem inscritos

# Configurações do InfluxDB
token = "6NOxnIEyVHUeJa4nnxTBfP6aBBWAAYVHCaE8Z4Uo3KBd41IezYLIwOZajbxikfg-p5bG3PgDCyd0VfpRD3HnzQ=="
org = "my-org"
url = "http://localhost:8086"
bucket = "irrigation"


# Função de callback para quando a conexão MQTT é estabelecida
def on_connect(client, userdata, flags, rc):
    print("Conectado ao HiveMQ")
    # Inscreva-se nos tópicos com base no prefixo
    client.subscribe(topic_prefix + "/#")


# Função de callback para quando uma mensagem MQTT é recebida
def on_message(client, userdata, msg):
    print(f"Mensagem recebida - Tópico: {msg.topic}, Mensagem: {msg.payload.decode()}")
    # Envia a mensagem para o InfluxDB
    write_to_influxdb(msg.topic, msg.payload.decode())


# Função para validar o arquivo de configurações
def is_valid_file(parser, arg):
    settings_file = Path(arg)
    if not settings_file.is_file():
        return parser.error(f"argument -f/--file: can't open '{arg}'")
    return settings_file


# Função para escrever os dados no InfluxDB
def write_to_influxdb(topic, message):
    write_client = InfluxDBClient(url=url, token=token, org=org)
    write_api = write_client.write_api(write_options=SYNCHRONOUS)

    # Parse a mensagem recebida e grave os dados no InfluxDB
    data = json.loads(message)
    measurement = topic[len(topic_prefix) + 1 :]  # Remove o prefixo do tópico
    point = Point(measurement)

    for key, value in data.items():
        if isinstance(value, bool):
            point = point.field(key, int(value))
        elif isinstance(value, (int, float)):
            point = point.field(key, value)
        else:
            point = point.field(key, str(value))

    write_api.write(bucket=bucket, org=org, record=point)


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


argparser = argparse.ArgumentParser()
argparser.add_argument(
    "-f",
    "--file",
    dest="settings_file",
    type=lambda x: is_valid_file(argparser, x),
    help="settings file",
    default=default_settings(),
)
args = argparser.parse_args()

# Inicia o simulador com as configurações fornecidas
simulator = Simulator(args.settings_file)
simulator.run()
