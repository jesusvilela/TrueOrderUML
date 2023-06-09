import os
import subprocess
import mammoth
from pathlib import Path
import re

uml_text = '''
@startuml

top to bottom direction

scale max 3000 height
scale max 3000 width

actor "User" as user

User -> OfferManagement : Request Offers
User -> OrderManagement : Place Order
User -> FlightScheduleData : Request Flight Data

package "Offer Management System" as OfferManagement {
  [Amadeus Altéa Inventory] as amadeus_altea
  [Sabre AirVision Marketing & Planning Suite] as sabre_airvision
}

package "Order Management System" as OrderManagement {
  [IBS Software iFly Res] as ibs_ifly_res
  [Radixx Res] as radixx_res
}

package "Flight and Schedule Data System" as FlightScheduleData {
  [OAG Schedules Analyzer] as oag_schedules
  [Innovata Schedule Reference Service] as innovata_schedule
}

OrderManagement -> RevenueAccounting : Update Revenue Data
OrderManagement -> ThirdPartyDelivery : Request Third Party Services
OrderManagement -> AutomatedCheckin : Request Check-in Services
OrderManagement -> Middleware : Integrate External Services
OrderManagement -> PaymentHub : Process Payments
OrderManagement -> FlightScheduleData : Get Flight Data
OrderManagement -> ESPReservation : Process Reservations

package "Revenue Accounting System" as RevenueAccounting {
  [Accelya REVERA] as accelya_revera
  [Mercator Sirius] as mercator_sirius
}

package "Third-Party Delivery Systems" as ThirdPartyDelivery {
  [Farelogix FLX Merchandise] as farelogix_flx
  [Datalex Digital Commerce Platform] as datalex_digital
}

package "Automated Check-in Service (DCS)" as AutomatedCheckin {
  [Amadeus Altea DCS] as amadeus_altea_dcs
  [SabreSonic DCS] as sabresonic_dcs
}

package "Middleware" as Middleware {
  [MuleSoft Anypoint Platform] as mulesoft_anypoint
  [TIBCO Cloud Integration] as tibco_cloud
}

package "Payment Hub" as PaymentHub {
  [Adyen Payment Platform] as adyen_payment
  [Worldpay from FIS] as worldpay_fis
}

package "ESP (Electronic Sales Platform) Reservation Service" as ESPReservation {
  [Navitaire New Skies] as navitaire_new_skies
  [SITA Horizon] as sita_horizon
}

@enduml
'''

uml_file = 'architecture.uml'
png_file = 'architecture.png'

with open(uml_file, 'w') as f:
    f.write(uml_text)

#call plantuml.jar to generate png
subprocess.call(['java', '-jar', 'plantuml-1.2023.4.jar', '-tpng', '-o', os.path.dirname(os.path.abspath(png_file)), uml_file])

input_file = "True Order Architecture based on IATA.docx"
output_file = "index.html"
image_file = "architecture.png"  # Use the vertically cascading UML diagram

import matplotlib.pyplot as plt

def create_cost_chart(cost_data, output_file):
    labels = list(cost_data.keys())
    costs = list(cost_data.values())

    plt.bar(labels, costs)
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Market Solutions')
    plt.ylabel('Estimated Yearly Cost (USD)')
    plt.title('Activity Based Cost Estimates')

    plt.savefig(output_file, bbox_inches='tight')
    plt.close()

cost_data = {
    'Amadeus Altéa': 120000,
    'Sabre AirVision': 110000,
    'IBS iFly Res': 90000,
    'Radixx Res': 95000,
    'Accelya REVERA': 80000,
    'Mercator Sirius': 85000,
    'Farelogix FLX': 60000,
    'Datalex Digital': 70000,
    'Amadeus Altea DCS': 75000,
    'SabreSonic DCS': 80000,
    'MuleSoft Anypoint': 40000,
    'TIBCO Cloud': 45000,
    'Adyen Payment': 30000,
    'Worldpay FIS': 35000,
    'OAG Schedules': 50000,
    'Innovata SRS': 55000,
    'Navitaire New Skies': 70000,
    'SITA Horizon': 75000,
}

cost_chart_file = 'cost_chart.png'
create_cost_chart(cost_data, cost_chart_file)

def docx_to_html(docx_file, architecture_image_file, cost_chart_image_file):
    with open(docx_file, "rb") as file:
        result = mammoth.convert_to_html(file)
        html_content = f'<!DOCTYPE html><html><head><meta charset="utf-8"><title>True Order UML</title></head><body><a href="{architecture_image_file}" target="_blank">'
        html_content += f'<img src="{architecture_image_file}" alt="Architecture" style="width:auto; height:auto;"></a>'
        html_content += result.value
        html_content += f'<div style="page-break-before: always;"></div>'
        html_content += f'<h2>Addendum: Activity Based Cost Estimates</h2>'
        html_content += f'<img src="{cost_chart_image_file}" alt="Cost Chart" style="width:80%; height:auto;">'
        return html_content


def save_as_html(content, file_name):
    with open(file_name, "w", encoding="utf-8") as output:
        output.write(content)

content = docx_to_html(input_file, image_file, cost_chart_file)

save_as_html(content, output_file)


