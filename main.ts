// main.ts — copies POST.json from this script's own directory to /output.
// Zero dependencies; Node built-ins only. Deterministic: every run writes
// the exact same bytes it read, and exits 0 on success.
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const sourcePath = join(scriptDir, "POST.json");
const outputDir = "/output";
const outputPath = join(outputDir, "POST.json");

const data = readFileSync(sourcePath);
mkdirSync(outputDir, { recursive: true });
writeFileSync(outputPath, data);
console.log(`Copied POST.json (${data.length} bytes) to ${outputPath}`);
