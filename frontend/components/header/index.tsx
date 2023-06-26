import Image from "next/image";
import Link from "next/link";
import logoEsDev from './../../public/img/logo-esdev.png';
import userDefault from '../../public/img/user.png';
import styles from './styles.module.css'
import { destroyCookie, parseCookies } from "nookies";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { api } from "@/services/api";

export default function Header() {

  // const pathname = usePathname();
  const router = useRouter();
  const [isToken, setIsToken] = useState<string>();
  const [logado, setLogado] = useState<boolean>();
  const [userMe, setUserMe] = useState<any>(false);
  const [visible, setVisible] = useState<boolean>(false)

  function deslogar() {
    destroyCookie(undefined, "tokenEstufa");
    const { 'tokenEstufa': token } = parseCookies();
    setIsToken(token)
    router.push("/login");
  }
  
  useEffect( ()=>{
    const { 'tokenEstufa': token } = parseCookies();
    setIsToken(token)

    async function getUser() {
      try {
        api.defaults.headers['authorization'] = `Bearer ${token}`;
        const {data} = await api.get('/usuarios/me')

        setUserMe(data[0])

        setLogado(!!data)
      } catch (error) {
        setLogado(false)
        setUserMe(false)
      }
    }
    getUser()

  },[isToken, userMe])
  
  return (
    <>
    <header className={styles.header}>
      <nav className={`container ${styles.display}`}>
        <Link
          href={  (isToken && logado) ? `/dashboard` : `/`}
        >
          <div className={styles.blocoLogo}>
            <div>
              <Image
              src={logoEsDev}
              alt="Imagem da logo ESDEV"
              />
            </div>

            <div>
              ES DEV
            </div>          
          </div>
        </Link>

        <ul className={styles.menusLinks}>
        {
          isToken === undefined && logado === undefined ? null : (

            !isToken && !logado ?(
              <>
                <li>
                  <Link href={'/login'}>Fazer Login</Link>
                </li>
                <li>
                  <Link href={'/signup'}>Cadastre-se</Link>
                </li>
              </>
            ): (
              <>
                <li>
                  <Link href={'/dashboard'}>Dashboard</Link>
                </li>
                
                <li>
                  <div className={styles.menusUser}>
                    <div className={styles.circuloHeader} onClick={ () => setVisible(!visible)}>
                    <Image
                      src={ userDefault }
                      alt="Imagem da logo ESDEV"
                    />
                    </div>
                    {visible && (
                      <div className={styles.drop}>
                        <ul>
                          <li><p title={userMe?.email}>{userMe?.nome}</p></li>
                          <li><button onClick={deslogar}>Deslogar</button></li>
                        </ul>
                      </div>
                    )}
                  </div>
                </li>
              </>
            )

          )
        }
        
        </ul>        
      </nav>
    </header>
    </>
  );
}