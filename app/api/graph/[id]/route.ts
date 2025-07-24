// app/api/graph/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { graphData } from '@/app/api/graph/store';

export async function PUT(req: NextRequest) {
  const id = req.nextUrl.pathname.split('/').pop() || '';
  const { name, group } = await req.json();

  const node = graphData.nodes.find((n) => n.id === id);
  if (!node) {
    return NextResponse.json({ error: 'Node not found' }, { status: 404 });
  }

  node.name = name ?? node.name;
  node.group = group ?? node.group;

  return NextResponse.json(node);
}

export async function DELETE(req: NextRequest) {
  const id = req.nextUrl.pathname.split('/').pop() || '';

  const node = graphData.nodes.find((n) => n.id === id);
  if (!node) {
    return NextResponse.json({ error: 'Node not found' }, { status: 404 });
  }

  graphData.nodes = graphData.nodes.filter((n) => n.id !== id);
  graphData.links = graphData.links.filter(
    (l) => l.source !== id && l.target !== id
  );

  return NextResponse.json(node);
}
