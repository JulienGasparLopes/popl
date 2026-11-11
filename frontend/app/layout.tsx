import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { Suspense } from "react";
import { getSession } from "./getSession";
import "./globals.css";
import { Sidebar } from "./sidebar";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "PoPL",
  description: "Path of Private League",
};

const RootComponent = async ({ children }: { children: React.ReactNode }) => {
  const session = await getSession();

  return (
    <>
      <Sidebar session={session} />
      <div className="p-16 w-full h-full overflow-scroll">{children}</div>
    </>
  );
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}>
      <body className="min-h-full flex h-full overflow-hidden">
        <Suspense fallback="Loading...">
          <RootComponent children={children} />
        </Suspense>
      </body>
    </html>
  );
}
