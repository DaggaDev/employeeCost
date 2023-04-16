import streamlit as st

def formatAsKroner(value):
    value=float("{:.2f}".format(value))
    valueString=format(value, ",").replace(",",".")
    valueString="kr " + ",".join(valueString.rsplit(".", 1))
    return valueString

g=111477

st.title("Ansattekostnader")
col1, col2, col3= st.columns(3)

st.subheader("Input")
salary=st.slider("Avtalt årslønn i kroner", min_value=200000, max_value=2000000, value=500000, step=10000)
vacationWeeks=st.select_slider('Antall uker ferie', ['4', '5'])
pension71=st.slider("Pensjon fra første krone til 7,1G", min_value=2.0, max_value=7.0, value=4.0, step=0.1)
pension12=st.slider("Pensjon fra 7,1G til 12G", min_value=0.0, max_value=25.1, value=4.0, step=0.1)
ysinsurance=st.slider("Yrkesskadeforsikring (obligatorisk)", min_value=0, max_value=15000, value=4000)
otherinsurance=st.slider("Andre forsikringer", min_value=0, max_value=15000, value=6800)
cellphone=st.slider("Mobil kostander", min_value=0, max_value=15000, value=7500, step=100)
otherEq=st.slider("Annet utstyr (PC, sekk/veske, etc.). Dette er årlig bergent kostnad, husk levetid.", min_value=0, max_value=50000, value=20000, step=100)

payedSalary=salary-(salary/260*int(vacationWeeks)*5)

if vacationWeeks=='4':
    vacationMoney=payedSalary*0.102
else:
    vacationMoney=payedSalary*0.12

if int(salary)<7.1*g:
    pensionCost=int(salary)*float(pension71)/100
elif int(salary)<12*g:
    pensionCost=float(pension71)/100 *7.1*g + (int(salary)-(7.1*g)) * (float(pension71)+float(pension12))/100
else:
    pensionCost=float(pension71)/100 *7.1*g + ((g*12)-(g*7.1)) * (float(pension71)+float(pension12))/100

employeeTax=payedSalary*0.141+vacationMoney*0.141+pensionCost*0.141
if int(salary)>=750000:
    employeeTax=employeeTax+(payedSalary+vacationMoney-750000)*0.05

totalCost=payedSalary+vacationMoney+employeeTax+pensionCost+int(ysinsurance)+int(otherinsurance)+cellphone+otherEq

col1.metric(label="Utbetalt i løpet av året", value=formatAsKroner(payedSalary))
col2.metric(label="Utbetalt i måneden", value=formatAsKroner(payedSalary/11))
col3.metric(label="Feriepenger beregnet", value=formatAsKroner(vacationMoney))
col1.metric(label="Beregnet arbeidsgiveravgift", value=formatAsKroner(employeeTax))
col2.metric(label="Beregnet pensjonskostnad", value=formatAsKroner(pensionCost))
col3.metric(label="Totalt beregnet kostnad", value=formatAsKroner(totalCost))

