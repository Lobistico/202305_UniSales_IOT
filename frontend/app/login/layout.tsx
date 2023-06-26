import Footer from "@/components/footer"
import Header from "@/components/header"
// import { AuthProvider } from "@/contexts/AuthContext"


export const metadata = {
  title: 'Login',
  description: 'Essa é a tela para Logar no sistema',
}

export default function LoginLayout({
  children, // will be a page or nested layout
}: {
  children: React.ReactNode
}) {
  return (
    <>
      
        {/* Include shared UI here e.g. a header or sidebar */}

        <main className="centralizarBloco">
          {children}
        </main>      
    </>
  )
}
