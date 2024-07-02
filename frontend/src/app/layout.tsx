import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Image search Simulator",
  description: "Simulador de búsqueda de imágenes",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
