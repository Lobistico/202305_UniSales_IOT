"use client";
import { createContext, useEffect, useState } from "react";
import {setCookie, parseCookies } from 'nookies'
import { api } from "@/services/api";
import axios from "axios";
import { useRouter } from "next/navigation";

type AuthContextType = {
  isAuthenticated: boolean,
  user: string | null,
  signIn: (formData : FormData) => Promise<object|void>
}

export const AuthContext = createContext({} as AuthContextType)


export function  AuthProvider({ children }
  : {
    children: React.ReactNode
  }) {

    const router = useRouter();
    const [user, setUser] = useState<string | null>(null);
    const isAuthenticated = !!user;

    useEffect( () => {
      const {'tokenEstufa': token} =  parseCookies()

      if(token) {
        api.get('/usuarios/me').then((response) => {
            if(response.status == 200) {  
              setUser(response.data[0].email)
            }
          });
        
      }
    },[])

    async function signIn(formData : FormData) {

      try {
        const response = await axios.post('http://127.0.0.1:8080/api/v1/usuarios/login', formData)
  
        if(response.status === 200) {
          const token = response.data.access_token;
          setCookie(undefined, 'tokenEstufa',  token, {
            maxAge: 60 * 60 * 4,
          });
          api.defaults.headers['authorization'] = `Bearer ${token}`;
  
          router.push('/dashboard')
        } else {
          return response.data;
        }
        
      } catch (error) {
        console.error("Erro no servidor, tente novamente mais tarde!");
      } 
        
    }

  return (

    <AuthContext.Provider value={{ user, isAuthenticated, signIn}}>
      {children}
    </AuthContext.Provider>
  )

}