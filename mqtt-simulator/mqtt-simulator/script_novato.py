import paho.mqtt.client as mqtt
import argparse
from pathlib import Path
from simulator import Simulator

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

# INFLUX DB
import influxdb_client
import os
import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "pCEvuFp9aKDrFFXPKbTDQUN80BLtemqAmHoxpW7lR4md-ZUmcdlIp4IH8Nq-E_U-pu3didUA-FK4T907DSG7-Q=="
org = "my-org"
url = "http://localhost:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
bucket = "irrigation"

write_api = write_client.write_api(write_options=SYNCHRONOUS)

for value in range(5):
    point = Point("measurement1").tag("tagname1", "tagvalue1").field("field1", value)
    write_api.write(bucket=bucket, org=org, record=point)
    time.sleep(1)  # separate points by 1 second

query_api = write_client.query_api()

query = """from(bucket: "irrigation")
 |> range(start: -10m)
 |> filter(fn: (r) => r._measurement == "measurement1")"""
tables = query_api.query(query, org="my-org")

for table in tables:
    for record in table.records:
        print(record)


# Inicia o simulador com as configurações fornecidas
simulator = Simulator(args.settings_file)
simulator.run()
