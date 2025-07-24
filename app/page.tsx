'use client';

import dynamic from "next/dynamic";

// Dynamically import SpiralGraphUI with SSR disabled
const SpiralGraphUI = dynamic(() => import("@/components/SpiralGraphUI"), { ssr: false });

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center">
      <SpiralGraphUI />
    </main>
  );
}
