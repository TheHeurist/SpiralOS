import { readdirSync, readFileSync, writeFileSync } from "fs";
import yaml from "js-yaml";

const pearlsDir = "./docs/ekr/pearls";
const files: string[] = readdirSync(pearlsDir).filter((f: string) => f.endsWith(".yaml"));

const lattice = files.map((file: string) => {
  const data = yaml.load(readFileSync(`${pearlsDir}/${file}`, "utf8")) as Record<string, unknown>;
  return data;
});

writeFileSync("./docs/ekr/lattice.json", JSON.stringify(lattice, null, 2));
console.log(`✅ Compiled ${lattice.length} pearls into lattice.json`);
