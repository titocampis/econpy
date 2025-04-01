# pylint: skip-file
# https://taxdown.es/irpf/tabla-tramos/

# Config
dirty_wage = 30000

# Constants
PER_SS = 0.0635
app_irpf_sp = {
    "tramo_1": {"min": 0, "max": 12450, "irpf": 0.095},
    "tramo_2": {"min": 12450, "max": 20200, "irpf": 0.12},
    "tramo_3": {"min": 20200, "max": 35200, "irpf": 0.15},
    "tramo_4": {"min": 35200, "max": 60000, "irpf": 0.185},
    "tramo_5": {"min": 60000, "max": 300000, "irpf": 0.225},
    "tramo_6": {"min": 300000, "max": float("inf"), "irpf": 0.245},
}

app_irpf_cat = {
    "tramo_1": {"min": 0, "max": 12450, "irpf": 0.105},
    "tramo_2": {"min": 12450, "max": 17707, "irpf": 0.12},
    "tramo_3": {"min": 17707, "max": 21000, "irpf": 0.14},
    "tramo_4": {"min": 21000, "max": 33007, "irpf": 0.15},
    "tramo_5": {"min": 33007, "max": 53407, "irpf": 0.188},
    "tramo_6": {"min": 53407, "max": 90000, "irpf": 0.215},
    "tramo_10": {"min": 90000, "max": 120000, "irpf": 0.235},
    "tramo_11": {"min": 120000, "max": 175000, "irpf": 0.245},
    "tramo_12": {"min": 175000, "max": float("inf"), "irpf": 0.255},
}

# SS
ss = dirty_wage * PER_SS
base_imponible = dirty_wage - ss

# Statal IRPF
for key, elem in app_irpf_sp.items():
    if dirty_wage == 0:
        per_irpf_sp = 0
    if elem["min"] <= dirty_wage and dirty_wage < elem["max"]:
        per_irpf_sp = elem["irpf"]

# Autonomic IRPF
for key, elem in app_irpf_cat.items():
    if dirty_wage == 0:
        per_irpf_cat = 0
    if elem["min"] <= dirty_wage and dirty_wage < elem["max"]:
        per_irpf_cat = elem["irpf"]

# Resultados
per_irpf_total = per_irpf_sp + per_irpf_cat
irpf_total = dirty_wage * 0.5 * per_irpf_total
salario_neto = base_imponible - irpf_total

print(
    "\n*********************************************************************\n"
    f"Salario Bruto anual               = {dirty_wage:,.0f}€\n"
    f"Cuotas SS anual                   = {ss:,.2f}€ "
    f"({100 * PER_SS:,.2f}%)\n"
    f"Deducción IRPF Estatal anual      = {per_irpf_sp * 100:,.2f}%\n"
    f"Deducción IRPF Autonomica anual   = {per_irpf_cat * 100:,.2f}%\n"
    f"Deducción Total IRPF anual        = {irpf_total:,.2f}€ "
    f"({(100/2 * per_irpf_total):,.2f}%)\n"
    f"Salario Neto anual                = {salario_neto:,.2f}€\n"
    f"Salario Bruto mensual (12 pagas)  = {(dirty_wage/12):,.2f}€\n"
    f"Salario Neto mensual  (12 pagas)  = {(salario_neto/12):,.2f}€\n"
    "*********************************************************************\n"
)
