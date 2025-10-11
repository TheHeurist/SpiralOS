/**
 * SpiralOS Lattice Compiler
 * Scans /docs/ekr/pearls/ and produces a single lattice.json
 */

import { readdirSync, readFileSync, writeFileSync } from "fs";
import yaml from "js-yaml";

const pearlsDir = "./docs/ekr/pearls";
const files = readdirSync(pearlsDir).filter(f => f.endsWith(".yaml"));

const lattice = files.map(file => {
  const data = yaml.load(readFileSync(`${pearlsDir}/${file}`, "utf8"));
  return data;
});

writeFileSync("./docs/ekr/lattice.json", JSON.stringify(lattice, null, 2));
console.log(`✅ Compiled ${lattice.length} pearls into lattice.json`);
