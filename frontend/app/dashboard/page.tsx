'use client';
import { api } from "@/services/api";
import { parseCookies } from "nookies";
import { useEffect, useState } from "react";
import styles from './styles.module.css';
import { format } from "date-fns";
import GetDay from "@/functions/getDay";
import axios from "axios";


export default function Home(){

  const {'tokenEstufa': token} =  parseCookies();
  const [sensorAtivo, setSensorAtivo] = useState<boolean>(false);

  const [sensor, setSensor] = useState<number>(0);
  const [tempUmi, setTempUmi] = useState<any>(null);
  const [regado, setRegado] = useState<any>(null);
  const [relatorios, setRelatorios] = useState<any>()
  const [boolenaRelatorio, setBoolenaRelatorio] = useState<boolean>(true);

  async function funcSensor(sensor: number) { 
    if (sensor > 0 ) {
      setSensorAtivo(!sensorAtivo)
      setSensor(sensor)
      
      api.defaults.headers['authorization'] = `Bearer ${token}`;
      const UmidadeTemperatura = await api.get(`plantacao/sensor_${sensor}`);
  
      console.log(UmidadeTemperatura);
      const areaRegada = await api.get(`plantacao/areas_regadas/sensor_${sensor}`);
  
      if(UmidadeTemperatura.status === 200 && areaRegada.status === 200) {
        if(UmidadeTemperatura.data.length > 0 ) setTempUmi(UmidadeTemperatura.data);
        if(areaRegada.data.length > 0 ) setRegado(areaRegada.data[0])
      }
    }
  }

  useEffect(() => {
    async function f() {
      api.defaults.headers['authorization'] = `Bearer ${token}`;
      const UmidadeTemperatura = await api.get(`plantacao/sensor_${sensor? sensor : 1}`);

      console.log(UmidadeTemperatura);
      const areaRegada = await api.get(`plantacao/areas_regadas/sensor_${sensor? sensor : 1}`);

      if(UmidadeTemperatura.status === 200 && areaRegada.status === 200) {
        if(UmidadeTemperatura.data.length > 0 ) setTempUmi(UmidadeTemperatura.data);
        if(areaRegada.data.length > 0 ) setRegado(areaRegada.data[0])
      }
    }
    if(sensor > 0) {
      f()
    }

  },[sensor, tempUmi])



  function fecharModalSensor () {
    setSensor(0);
    setRegado(null);
    setSensorAtivo(!sensorAtivo)
    setRelatorios(null)
    setTempUmi(null);
    setBoolenaRelatorio(true);
  }

  function fecharRelatorio() {
    if(!boolenaRelatorio) {
      setRelatorios(null);
    }
    setBoolenaRelatorio(!boolenaRelatorio);
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
    fecharRelatorio()
    api.defaults.headers['authorization'] = `Bearer ${token}`;
    const relatorio = await api.get(`plantacao/relatorio/sensor_${sensor}`);

    if (relatorio.status === 200) {
      setRelatorios(relatorio.data)
    }
  }


  return (
    <>
    <div className={`container`}>
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
                    <div className={`${styles.divTempUmi} ${tempUmi[0]?._value > 25 && styles.divRegarRed }`}>
                      <p>{tempUmi[0]?._value.toFixed(2).toString().replace('.', ',')} C°</p>
                    </div>

                    <h3>Última Atualização</h3>
                    <div className={`${styles.divHorario}`}>
                      <span>{format(new Date(tempUmi[0]?._time), 'dd/MM/yyyy HH:mm:ss')}</span>
                    </div>
                    <br />

                  </div>
                  <div>
                    <h2>Umidade da Área</h2>
                    <div className={`${styles.divTempUmi} ${tempUmi[1]?._value > 1 && styles.divRegarRed }`}>
                      <p>{tempUmi[1]?._value.toFixed(2).toString().replace('.', ',')}</p>
                    </div>
                    
                    <h3>Última Atualização</h3>
                    <div className={`${styles.divHorario}`}>
                      <span>{format(new Date(tempUmi[1]?._time), 'dd/MM/yyyy HH:mm:ss')}</span>
                    </div>
                    <br />

                  </div>
                </div>
                <div className={`${styles.divBotaoRegar}`} >
                  <button className={`${tempUmi[0]?._value > 25 && styles.divRegarRed }`} onClick={ ()=> irrigarArea()}>Irrigar Área</button>

                  {boolenaRelatorio?
                    <button onClick={() => verRelatorio()} title="Ver Relatório">Ver Relatório</button>
                  :
                    !boolenaRelatorio && <button onClick={() => fecharRelatorio()} title="Ver Relatório">Fechar Relatório</button>}

                </div>
                <div className={styles.divTable}>
                  <table className={styles.table}>
                  { relatorios  && 
                    relatorios.map( (e:any) => (
                      <>

                        {e?._field === "temperatura" && (
                          <>
                          <tr>
                            <th>Temperatura</th>
                            <td>{e?._value.toFixed(2).toString().replace('.', ',')}</td>
                            <th>Data de Registro</th>
                            <td>{format(new Date(e?._time), 'dd/MM/yyyy HH:mm:ss')}</td>
                          </tr>
                          </>
                        )}                         
                        
                      </>
                    ))
                  }
                  </table>

                  <table className={styles.table}>
                  { relatorios  && 
                    relatorios.map( (e:any) => (
                      <>
                        {e?._field === "umidade" && (
                          <>
                          <tr>
                            <th>Umidade</th>
                            <td>{e?._value.toFixed(2).toString().replace('.', ',')}</td>
                            <th>Data de Registro</th>
                            <td>{format(new Date(e?._time), 'dd/MM/yyyy HH:mm:ss')}</td>
                          </tr>
                          </>
                        )}                             
                      </>
                    ))
                  }
                  </table>
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
