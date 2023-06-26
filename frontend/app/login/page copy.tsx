"use client"; // This is a client component
import hookCep from "@/components/hooks/viaCep";
import { hookEstados, hookMunicipios } from "@/components/hooks/viaIbge";
import { ViaCep } from "@/interfaces/viaCep";
import { viaEstados } from "@/interfaces/viaEstados";
import { viaMunicipios } from "@/interfaces/viaMunicipios";
import { useEffect, useState } from "react";

export default function Home() {
  const [viaCep, setViaCep] = useState<ViaCep>();
  const [viaEstados, setViaEstados] = useState<[viaEstados]>();
  const [viaMunicipios, setviaMunicipios] = useState<[viaMunicipios]>();

  const [estado, setEstado] = useState('');
  const [municipios, setMunicipios] = useState('');
  const [cep, setCep] = useState('');

    

  useEffect( () => {
    async function functionEstados() {
      const result = await hookEstados();
      if(result) {
        setViaEstados(result);
      }
    }  
    functionEstados();

    async function functionMunicipios(estado: string) {
      const result = await hookMunicipios(estado);
      if(result) {
        setviaMunicipios(result);
      }
    }   
    functionMunicipios(estado);

    async function functionCep(cep: string) {
      const resultCep = await hookCep(cep);
      if(resultCep) {
        setViaCep(resultCep);
      }
    }
    functionCep(cep) 

  },[estado, municipios]);
  
    

  return (
    <>
      <h1>Login </h1>
      
      {viaCep && (
        <>
          <h1>{viaCep.cep} </h1>
          <h1>{viaCep.bairro} </h1>
          <h1>{viaCep.complemento} </h1>
          <h1>{viaCep.ddd} </h1>
        </>
        )
      }

      <select onChange={(e) => setEstado(e.target.value)}>
        {viaEstados && viaEstados.map( (e) =>(
          <option 
            key={e.id} 
            value={e.sigla}
          >{e.nome}</option>
        ))}

      </select>

      
      <select onChange={(e) => setMunicipios(e.target.value)}>
        {viaMunicipios && viaMunicipios.map( (e) =>(
          <option 
            key={e.id} 
            value={e.id} 
          >{e.nome}</option>
        ))}

      </select>

      
    </>
  );
}

