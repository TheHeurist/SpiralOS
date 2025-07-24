'use server';

import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const msg = searchParams.get('msg') || 'Hello from SpiralOS API';
  return NextResponse.json({ echo: msg });
}
