import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

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

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}>
      <body className="min-h-full flex">
        <nav className="p-8 shadow-xl/30 min-w-60">
          <div className="flex content-center flex-col items-center mb-16 leading-none">
            <h1>Path</h1>
            <h1>of</h1>
            <h1>Private</h1>
            <h1>League</h1>
          </div>

          <hr className="mb-16"></hr>

          <div className="flex flex-col gap-4">
            <a href="/mechanics">
              <h2>League Mechanics</h2>
            </a>

            <a href="/builds">
              <h2>Builds</h2>
            </a>

            <a href="/wantedItems">
              <h2>Wish List</h2>
            </a>
          </div>
        </nav>
        <div className="p-16 w-full">{children}</div>
      </body>
    </html>
  );
}
