"use client";
import { useContext, useState } from "react";
import styles from  './styles.module.css'
import { AuthContext } from "@/contexts/AuthContext";



 // This is a client component
export default function Home() {

  const {signIn} = useContext(AuthContext)
  const [load, setLoad] = useState<boolean>(false);

  const  [usuario, setUsuario] = useState('alef@gmail.com');
  const [senha, setSenha] = useState('123456');

  const handleLogin = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoad(true);
    const formData = new FormData();

    formData.append('username', usuario);
    formData.append('password', senha);

    try {
      await signIn(formData);
    } catch (error: any) {
      console.log(error?.response.data );
    }

    setLoad(false);
  }
  
  return (
    <>
      <div className={`${styles.blocoLogin} container`}>
        <h1 className={`titulo m-bot5`}>Login </h1>

        <form className={`${styles.blocoLogin}`} onSubmit={handleLogin}>
          <input 
          type="text" 
          value={usuario}
          onChange={ (e)=> {setUsuario(e.target.value)}}
          placeholder="Usuário"
          />

          <input 
          type="password"
          value={senha}
          onChange={(e) => {setSenha(e.target.value)}}
          placeholder="Senha"
          />

          {load && load? (
            <button disabled>Logando...</button>
            ): (
            <button>Logar</button>
          )}
        </form>

      </div>
      
    </>
  );
}

