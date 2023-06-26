import { AuthContext } from "@/contexts/AuthContext";
import { useContext } from "react";

export default function getUser(){ 
  const {user} = useContext(AuthContext)
  console.log(user)
}