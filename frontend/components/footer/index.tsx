"use client";
import Image from "next/image";
import { useEffect, useState } from "react";
import logoEsDev from './../../public/img/logo-esdev.png'
import Link from "next/link";

import styles from  './styles.module.css'

export default function Footer() {
  const [anoAtual, setAnoAtual] = useState<string>('');
  useEffect(() => {
    const obterAnoAtual = () => {
      const dataAtual = new Date();
      const ano = dataAtual.getFullYear();
      setAnoAtual(ano.toString());
    };

    obterAnoAtual();
  }, []);

  return (
    <>
      <footer className={`${styles.fundo}` }>
        <div className={`container`}>
        <div className={styles.display}>
            <div>
              <p>Sistema para o Controle inteligente de Estufas.</p>
              <p>Este Site foi Desenvolvido por:</p>
                <p><b>
                  <Link href="https://www.linkedin.com/in/renato-lopes-44a12920b/" target="_blank" rel="noopener">Renato Lopes</Link>, <Link href="https://www.linkedin.com/in/eric-dourado-de-santana-dos-santos-ab3826211/" target="_blank" rel="noopener">Eric Dourado</Link>, <br/>
                  <Link href="https://www.linkedin.com/in/eduardolrodrigues/" target="_blank" rel="noopener">Eduardo Rodrigues</Link>, <Link href="https://www.linkedin.com/in/luiz-fernando-ferreira-a5b474278/" target="_blank" rel="noopener">Luiz Fernando</Link>, <br/>
                  <Link href="https://www.linkedin.com/in/paulo-coura-barbosa/" target="_blank" rel="noopener">Paulo Coura</Link>, <Link href="https://www.linkedin.com/in/%C3%A1lef-coutinho-692855204/" target="_blank" rel="noopener">Alef Coutinho</Link>
                </b></p>
            </div>
            <div>
              <p>Alunos do Centro Universitário UniSales de Vitória, ES.</p>
              <p>Além de alunos, o grupo conta com analistas e desenvolvedores com experiência no mercado Tech.<br/>
              Mentorados por <b>Lucas Barboza e Renan Freitas</b></p>
            </div>
          </div>
        
          <div className={`${styles.display} p-top3 border-top-white m-top3`} >
            <h3>Copyright © {anoAtual} Sistema de Controle de Estufas. Todos os direitos reservados.</h3>
            <Link href={'/'}>
              <Image
                src={logoEsDev}
                alt="Imagem da logo ESDEV"
                width="32"
              />
            </Link>
          </div>
        </div>
          
      </footer>
    </>
  );
}