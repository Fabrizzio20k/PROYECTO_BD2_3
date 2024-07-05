import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Image search Simulator",
  description: "Simulador de búsqueda de imágenes",
  icons: [
    "./icon.ico"
  ]
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body className="bg-midnight-950">{children}</body>
    </html>
  );
}
