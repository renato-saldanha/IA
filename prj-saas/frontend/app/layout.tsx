import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SaaS de Suporte ao Cliente",
  description: "Plataforma completa de help desk com chat, tickets e base de conhecimento",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}

