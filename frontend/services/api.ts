import axios from "axios";
import { parseCookies } from "nookies";



const {'tokenEstufa': token} =  parseCookies()

export const api = axios.create({
  baseURL: 'http://127.0.0.1:8080/api/v1/'
});

if (token ) {
  api.defaults.headers['Authorization'] = 'Bearer ' + token;	
}