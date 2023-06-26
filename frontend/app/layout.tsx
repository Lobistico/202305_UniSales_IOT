'use client';
import './globals.css'
import { Inter } from 'next/font/google'
const inter = Inter({ subsets: ['latin'] })

import logoEsDev from './../public/img/logo-esdev.ico'
import { AuthProvider } from '@/contexts/AuthContext'
import { usePathname, useRouter } from 'next/navigation'
import { checkIsPublicRoutes } from '@/functions/check-is-public-route'
import PrivateRoute from '@/contexts/PrivateRoute';
import Footer from '@/components/footer';
import Header from '@/components/header';
import { useEffect, useState } from 'react';
import { parseCookies } from 'nookies';
import { api } from '@/services/api';
import { APP_ROUTES } from '@/constants/app-routes';

export const metadata = {
  title: 'Controle de Estufas',
  description: 'Essa é a tela para fazer o cadastro no sistema',

}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {

  const pathname = usePathname();
  const isPublic = checkIsPublicRoutes(pathname);
  const {push} = useRouter();

  const [isToken, setIsToken] = useState<string>();
  const [logado, setLogado] = useState<boolean>();

  useEffect( () => {
    const { 'tokenEstufa': token } = parseCookies();
    setIsToken(token)

    async function getUser() {
      try {
        api.defaults.headers['authorization'] = `Bearer ${token}`;
        const {data} = await api.get('/usuarios/me')
        setLogado(!!data)
      } catch (error) {
        setLogado(false)
      }
      
    }
    getUser()

    
  },[isToken, isPublic, logado, push])
  


  return (
    <html lang="pt-BR">
      <body className={inter.className}>

        <AuthProvider>

          {isPublic && (
            <>
              <Header />
              {children}
              <Footer/>
            </>

          )}

          {!isPublic && (
            <PrivateRoute>
                <Header />
                {children}
                <Footer/>
            </PrivateRoute>
          )}
         
        </AuthProvider>  
      </body>
    </html>
  )
}
