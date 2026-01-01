#!/usr/bin/env node
/**
 * Clone sitemap.xml for alternate hosts/domains.
 * Example:
 *   node scripts/clone-sitemap.js --host https://conjugate-intelligence.com \
 *     --source sitemap.xml --from https://theheurist.github.io/SpiralOS \
 *     --output sitemaps/conjugate-intelligence.com.xml
 */

import fs from 'fs';
import path from 'path';
import { URL } from 'url';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function parseArgs(argv) {
  const options = {};
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!arg.startsWith('--')) continue;
    const key = arg.slice(2);
    const next = argv[i + 1];
    if (next && !next.startsWith('--')) {
      options[key] = next;
      i += 1;
    } else {
      options[key] = true;
    }
  }
  return options;
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function inferFromHost(xml) {
  const match = xml.match(/<loc>([^<]+)<\/loc>/i);
  if (!match) return null;
  try {
    const url = new URL(match[1]);
    return url.origin;
  } catch (error) {
    console.warn('Unable to infer host from first <loc> entry; specify --from explicitly.', error.message);
    return null;
  }
}

const options = parseArgs(process.argv.slice(2));

if (!options.host) {
  console.error('Missing required --host argument (e.g., https://conjugate-intelligence.com)');
  process.exit(1);
}

const host = options.host.replace(/\/$/, '');
const source = options.source || path.join(__dirname, '..', 'sitemap.xml');

if (!fs.existsSync(source)) {
  console.error(`Source sitemap not found: ${source}`);
  process.exit(1);
}

const sourceXml = fs.readFileSync(source, 'utf8');
const inferredFrom = options.from || inferFromHost(sourceXml) || 'https://theheurist.github.io/SpiralOS';
const from = inferredFrom.replace(/\/$/, '');
const output = options.output || path.join(__dirname, '..', 'sitemaps', `${new URL(host).hostname}.xml`);

if (!options.from && from === 'https://theheurist.github.io/SpiralOS') {
  console.warn(`Using default source host ${from}; pass --from to override.`);
}

const replacedXml = sourceXml.replace(new RegExp(escapeRegExp(from), 'g'), host);

fs.mkdirSync(path.dirname(output), { recursive: true });
fs.writeFileSync(output, replacedXml, 'utf8');

console.log(`Cloned sitemap from ${source}`);
console.log(`Host replaced: ${from} -> ${host}`);
console.log(`Written to: ${output}`);
