// app/layout.tsx

export const metadata = {
  title: 'SpiralOS UI',
  description: 'Conjugate Intelligence Interface',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
