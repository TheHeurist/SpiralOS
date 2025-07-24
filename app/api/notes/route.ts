// app/api/notes/route.ts
'use server';

import { NextRequest, NextResponse } from 'next/server';
import { v4 as uuidv4 } from 'uuid';

// In-memory note store (reset on restart)
let notes: { id: string; text: string }[] = [];

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const text = body.text?.trim();

    if (!text) {
      return NextResponse.json({ error: 'Missing note text' }, { status: 400 });
    }

    const id = uuidv4();
    const newNote = { id, text };
    notes.push(newNote);

    return NextResponse.json(newNote, { status: 201 });
  } catch (err) {
    return NextResponse.json({ error: 'Invalid JSON' }, { status: 400 });
  }
}

export async function GET() {
  return NextResponse.json(notes);
}
