// app/api/graph/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { graphData } from "@/app/api/graph/store";


export async function GET() {
  return NextResponse.json(graphData);
}

export async function POST(req: NextRequest) {
  const { type, data } = await req.json();

  if (type === 'node') {
    graphData.nodes.push(data);
    return NextResponse.json({ message: 'Node added', data });
  }

  if (type === 'link') {
    graphData.links.push(data);
    return NextResponse.json({ message: 'Link added', data });
  }

  return NextResponse.json({ error: 'Invalid type' }, { status: 400 });
}
