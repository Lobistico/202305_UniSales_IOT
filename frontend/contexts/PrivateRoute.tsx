'use client';
import { APP_ROUTES } from "@/constants/app-routes";
import { checkIsPublicRoutes } from "@/functions/check-is-public-route";
import { api } from "@/services/api";
import { usePathname, useRouter } from "next/navigation";
import { parseCookies } from "nookies";

import { ReactNode, useEffect, useState } from "react";


type PrivateRouteProps = {
  children: ReactNode;
};

const PrivateRoute = ({children}: PrivateRouteProps) => {

    const {'tokenEstufa': token} =  parseCookies()
    const isUserAuthenticated = token;

    const pathname = usePathname();
    const isPublic = checkIsPublicRoutes(pathname);
    

    const {push} = useRouter();

    const [logado, setLogado] = useState<boolean>();

    useEffect( ()=>{


      async function getUser() {
        try {
          api.defaults.headers['authorization'] = `Bearer ${token}`;
          const {data} = await api.get('/usuarios/me')
          setLogado(!!data)

        } catch (error) {

          if (!isUserAuthenticated) { 
              push(APP_ROUTES.public.login)
          }

          setLogado(false)
        }
      }
      getUser()

    },[ isUserAuthenticated, push, logado ]);

    return (

      <>
        {!isUserAuthenticated &&  null}
        {isUserAuthenticated && children}
      </>

    )
};

export default PrivateRoute;

