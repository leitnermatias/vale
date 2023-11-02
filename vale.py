import datetime
import requests
import urllib3
import sys
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


CLASS_EXECUTIVE = 44
STATION_MARIO_CARVALHO = "03"
BELO_HORIZONTE_CODE = 7185
MARIO_CARVALHO_CODE = 7179

def create_payload(
        class_code: int,
        station: str,
        destiny: int,
        origin: str,
        date_timestamp: str,
        quantity: int
):
    return {
        "codigoClasse": class_code,
        "codigoFerrovia": station,
        "codigoLocalDestino": destiny,
        "codigoLocalOrigem": origin,
        "dataIda": date_timestamp,
        "detalheVenda": [{"detalhe": 33, "funcionario": False, "qtd": quantity}],
    }

today = datetime.datetime.now()
if len(sys.argv) > 1:
    today = datetime.datetime(2023, int(sys.argv[1]), 1)

print("Looking starting from: ", today)
dates = [today + datetime.timedelta(days=i) for i in range(38)]

found_going = []
found_coming = []

for date in dates:
    payload_going = create_payload(class_code=CLASS_EXECUTIVE, station=STATION_MARIO_CARVALHO, destiny=MARIO_CARVALHO_CODE, origin=BELO_HORIZONTE_CODE, date_timestamp=int(datetime.datetime.timestamp(date) * 1000), quantity=3)

    res_going = requests.post("https://tremdepassageiros.vale.com/sgpweb/rest/externo/VendaInternet/publico/pesquisaPassagem", json=payload_going, verify=False)

    response_json = res_going.json()

    if response_json["excessao"]:
        exception_type = response_json["excessao"]["tipo"]

        if exception_type == "N":
            continue
    
    found_going.append({"response": response_json, "date": date})

print("\tFound going to MARIO CARVALHO for dates:")
[print("\t\t" + date.strftime("%A %d/%m/%Y")) for date in [found["date"] for found in found_going]]

for date in dates:
    payload_coming = create_payload(class_code=CLASS_EXECUTIVE, station=STATION_MARIO_CARVALHO, destiny=BELO_HORIZONTE_CODE, origin=MARIO_CARVALHO_CODE, date_timestamp=int(datetime.datetime.timestamp(date) * 1000), quantity=3)

    res_coming = requests.post("https://tremdepassageiros.vale.com/sgpweb/rest/externo/VendaInternet/publico/pesquisaPassagem", json=payload_coming, verify=False)

    response_json = res_coming.json()

    if response_json["excessao"]:
        exception_type = response_json["excessao"]["tipo"]

        if exception_type == "N":
            continue
    
    found_coming.append({"response": response_json, "date": date})

print("\n\n\tFound going to BELO HORIZONTE for dates:")
[print("\t\t" + date.strftime("%A %d/%m/%Y")) for date in [found["date"] for found in found_coming]]
