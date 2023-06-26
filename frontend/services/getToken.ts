import { cookies } from "next/headers"

export function  getToken() {
  const cookieStore = cookies()
  return cookieStore.get('tokenEstufa') ; 
}

export function destroyToken() {
  const cookieStore = cookies()
  return cookieStore.delete('tokenEstufa') ;
}