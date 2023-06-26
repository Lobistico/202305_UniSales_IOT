"use client";
import axios from "axios";
import styles from './styles.module.css'
import { useRouter } from "next/navigation";
import { useState } from "react";


export default function Home() {

  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  // const [imagem, setImagem] = useState('');
  // const [file, setFile] = useState<File>();
  const [senha, setSenha] = useState('');

  const [load, setLoad] = useState<boolean>(false);
  const [error, setError] = useState('');

  const router = useRouter();
  async function handleCreateUser(event: React.FormEvent) {
    event.preventDefault();
    setLoad(true);
    try {
      // if(!file) return;

      const data = {
        nome,
        email,
        senha,
      }

      const resultAxios = await axios.post("http://localhost:8080/api/v1/usuarios/signup", data);

      if (resultAxios.status === 201 ) {
        router.push('/login');
      }

    }
    catch (err: any) {
      console.log(err.response?.data);
      
      if(err.response?.data?.detail) {
        setError(err.response?.data.detail)
      } else {
        setError(err.response?.data);

      }
    }


    setLoad(false);
  }

  return (
    <>
      <div className={`container`}>
        <h1  className={`titulo`}>cadastrar a conta</h1>
        <form onSubmit={handleCreateUser} className="m-bot5 m-top5" >
          <input type="text" 
          placeholder="Entre com o seu Nome"
          value={nome}
          onChange={(e) => setNome(e.target.value)}
          required
          />
          
          <input type="email"
          placeholder="Entre com o Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          />
          
          <input type="password"
          placeholder="Digite sua Senha"
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
          required 
          minLength={6}
          />

          {/* <label className={`border-img m-bot3`}>
            <input 
              type="file" 
              hidden
              onChange={ ({target}) => {
                if(target.files) {
                  const file = target.files[0];
                  setImagem(URL.createObjectURL(file));
                  setFile(file);
                }
              }}
            />
            <div className="w-40 aspect-video rounded flex items-center justify-center border2 border-dashed cursor-pointer">
              {imagem ? (
                <img src={imagem} alt="" />
              ):(
                <span>Selecione a Imagem</span>
              )}
            </div>
          </label> */}

          {load && load? (
            <button disabled>Cadastrando...</button>
            ): (
            <button className={`top3`}>Cadastrar</button>
          )}


        </form>
        {error && (
          <div className={styles.modal}>

            {error}
            <div>
              <div onClick={() => setError('')} className={styles.buttonX}>
                <button>X</button>
              </div>
            </div>
          </div>
        )}
      </div>

    </>
  )
}