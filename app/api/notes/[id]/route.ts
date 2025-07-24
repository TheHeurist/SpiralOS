import { NextRequest, NextResponse } from 'next/server';

let notes: { id: string; text: string }[] = [];

export async function GET(request: NextRequest, context: any) {
  const id = context.params.id;
  const note = notes.find(n => n.id === id);
  if (!note) return NextResponse.json({ error: 'Not found' }, { status: 404 });
  return NextResponse.json(note);
}

export async function PUT(request: NextRequest, context: any) {
  const id = context.params.id;
  const { text } = await request.json();

  const idx = notes.findIndex(n => n.id === id);
  if (idx === -1) {
    // CREATE
    const newNote = { id, text };
    notes.push(newNote);
    return NextResponse.json(newNote, { status: 201 });
  } else {
    // UPDATE
    notes[idx].text = text;
    return NextResponse.json(notes[idx]);
  }
}

export async function DELETE(request: NextRequest, context: any) {
  const id = context.params.id;
  const idx = notes.findIndex(n => n.id === id);
  if (idx === -1) return NextResponse.json({ error: 'Not found' }, { status: 404 });

  const deleted = notes.splice(idx, 1);
  return NextResponse.json(deleted[0]);
}
