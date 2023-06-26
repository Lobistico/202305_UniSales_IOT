import Footer from "@/components/footer"
import Header from "@/components/header"


export const metadata = {
  title: 'Cadastre-se',
  description: 'Essa é a tela para fazer o cadastro no sistema',
}

export default function LoginLayout({
  children, // will be a page or nested layout
}: {
  children: React.ReactNode
}) {
  return (
    
    <section>

      {/* Include shared UI here e.g. a header or sidebar */}

      <main>
        {children}
      </main>
    </section>
  )
}