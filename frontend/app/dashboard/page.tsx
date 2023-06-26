'use client';
import { api } from "@/services/api";
import { parseCookies } from "nookies";
import { useState } from "react";
import styles from './styles.module.css';
import { format } from "date-fns";
import GetDay from "@/functions/getDay";
import axios from "axios";


export default function Home(){

  const {'tokenEstufa': token} =  parseCookies();
  const [sensorAtivo, setSensorAtivo] = useState<boolean>(false);

  const [sensor, setSensor] = useState<number>();
  const [tempUmi, setTempUmi] = useState<any>(null);
  const [regado, setRegado] = useState<any>(null);
  const [relatorios, setRelatorios] = useState<any>(null)

  async function funcSensor(sensor: number) { 
    setSensorAtivo(!sensorAtivo)
    setSensor(sensor)
    api.defaults.headers['authorization'] = `Bearer ${token}`;
    const UmidadeTemperatura = await api.get(`plantacao/sensor_${sensor}`);

    const areaRegada = await api.get(`plantacao/areas_regadas/sensor_${sensor}`);

    if(UmidadeTemperatura.status === 200 && areaRegada.status === 200) {
      if(UmidadeTemperatura.data.length > 0 ) setTempUmi(UmidadeTemperatura.data);
      if(areaRegada.data.length > 0 ) setRegado(areaRegada.data[0])
    }
  }

  function fecharModalSensor (){
    setRegado(null);
    setSensorAtivo(!sensorAtivo)
  }

  async function irrigarArea() {
    const data = {
      regado: true,
      sensor: `sensor_${sensor}`
    }
    const headers = {
      // Cabeçalhos da requisição
      'Content-Type': 'application/json', // Exemplo de cabeçalho Content-Type
      'Authorization': `Bearer ${token}`, // Exemplo de cabeçalho de autorização
    };

    const areaRegada = await axios.post(`http://localhost:8080/api/v1/plantacao/regar`, data, {headers});
    if(areaRegada.status == 201) {
      const areaRegada = await api.get(`plantacao/areas_regadas/sensor_${sensor}`);
      if(areaRegada.status === 200) {
        setRegado(areaRegada.data[areaRegada.data.length - 1])
      }
    }
  }

  async function verRelatorio( ) {
    api.defaults.headers['authorization'] = `Bearer ${token}`;
    const relatorio = await api.get(`plantacao/relatorio/sensor_${sensor}`);
    if (relatorio.status === 200) {
      setRelatorios(relatorio.data)
    }
    console.log(relatorio)
  }


  return (
    <>
    <div className={`container`}>
      <h1 className={`titulo m-bot5`}> DashBoard</h1>
      <div className={styles.sensores}>
        <div onClick={() => funcSensor(1)}>
          Sensor 1
        </div>
        <div  onClick={() => funcSensor(2)}>
          Sensor 2
        </div>
        <div  onClick={() => funcSensor(3)}>
          Sensor 3
        </div>
      </div>
    </div>
    
    { sensorAtivo && 
      <div className={styles.fundoModalSensor}>
        <div className={styles.modalSensor} >
          <div className={styles.navbarModal}>
            <h1>Sensor da Área {sensor} da Estufa</h1>
            <button onClick={()=> fecharModalSensor()}>Sair</button>
          </div>

            {tempUmi && (
              <>
                <div className={styles.flexTempUmi}>
                  <div>
                    <h2>Temperatura da Área</h2>
                    {tempUmi[0]?._value.toFixed(2).toString().replace('.', ',')} C°

                    <h3>Última Atualização</h3>
                    {format(new Date(tempUmi[0]?._time), 'dd/MM/yyyy HH:mm:ss')}
                    <br />
                    <button title="Ver Relatório de Temperatura">Ver Relatório</button>
                  </div>
                  <div>
                    <h2>Umidade da Área</h2>
                    {tempUmi[1]?._value.toFixed(2).toString().replace('.', ',')}
                    
                    <h3>Última Atualização</h3>
                    {format(new Date(tempUmi[1]?._time), 'dd/MM/yyyy HH:mm:ss')}
                    <br />
                    <button onClick={() => verRelatorio()} title="Ver Relatório de Umidade">Ver Relatório</button>
                    {/* { relatorios  && 
     
                        relatorios.forEach((element: any) => (
                          <>
                          {element?._field === "umidade" && (
                            <>
                              <p>Temperatura: {element?._value} C°</p>
                              <p>Data: {element?._time} C°</p>
                              <hr />
                            </>
                          )} 
                          </>

                        ))
                        
                      } */}

                  </div>
                </div>
                <div className={`${tempUmi[0]?._value > 25 && styles.divBotaoRegarRed } ${styles.divBotaoRegar}`} >
                  <button onClick={ ()=> irrigarArea()}>Irrigar Área</button>
                  <legend>{typeof regado == "string" && regado}</legend>

              </div>
              </>
            )}

          <div className={styles.rodapeModalSensor}>
            {regado? (
              <>
                <h3>Esta área do Sensor foi regada no dia {format(new Date(regado?._time), 'dd/MM/yyyy HH:mm:ss')} - {GetDay(new Date(regado?._time))} </h3>
                
              </>
            ): (
              <>
                <h3>Esta área do Sensor ainda não foi regada</h3>
              </>
            ) }

          </div>
        </div>


      </div>
    
    }
    </>
  )
}
