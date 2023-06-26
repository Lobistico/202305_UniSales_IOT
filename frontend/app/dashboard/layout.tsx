import Footer from "@/components/footer"
import Header from "@/components/header"

export const metadata = {
  title: 'Dashboard',
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
