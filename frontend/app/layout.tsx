import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { getSession } from "./getSession";
import "./globals.css";
import { SidebarFooter } from "./SidebarFooter";

export const dynamic = "force-dynamic";

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

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const session = await getSession();
  return (
    <html lang="en" className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}>
      <head>
        <meta name="google-site-verification" content="2Adbh_n1Rgal41AZRTAirB3EoSzYyU8QUIqLnem4djE" />
      </head>
      <body className="min-h-full flex h-full overflow-hidden">
        <nav className="p-8 shadow-xl/30 min-w-60">
          <div className="grid grid-cols-1 grid-rows-[auto_auto_1fr_auto] justify-stretch h-full">
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

            <SidebarFooter session={session} />
          </div>
        </nav>
        <div className="p-16 w-full h-full overflow-scroll">{children}</div>
      </body>
    </html>
  );
}
