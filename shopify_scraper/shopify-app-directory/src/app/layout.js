import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'Shopify Apps Directory',
  description: 'A directory of Shopify apps with detailed information',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={`${inter.className} min-h-screen bg-gray-50`}>{children}</body>
    </html>
  )
}
