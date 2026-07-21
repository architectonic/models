import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const read = (name) => JSON.parse(fs.readFileSync(path.join(root, name), "utf8"));
const pkg = read("package.json");
const protocol = read("architectonic.protocol.json");
const errors = [];
const requireValue = (condition, message) => { if (!condition) errors.push(message); };
requireValue(protocol.schema_version === 1, "protocol schema_version must be 1");
requireValue(/^0\.2\./.test(protocol.protocol_version || ""), "protocol_version must be 0.2.x");
requireValue(protocol.package_version === pkg.version, "protocol package_version must match package.json");
requireValue(protocol.package_name === pkg.name, "protocol package_name must match package.json");
requireValue(Boolean(protocol.layer), "protocol layer is required");
requireValue(protocol.status === "experimental", "status must disclose experimental maturity");
requireValue(protocol.maturity === "pre-1.0", "maturity must disclose pre-1.0 state");
requireValue(Boolean(protocol.canonical_entry), "canonical_entry is required");
requireValue(fs.existsSync(path.join(root, protocol.canonical_entry || "")), `missing canonical entry ${protocol.canonical_entry}`);
const readme = fs.readFileSync(path.join(root, "README.md"), "utf8");
requireValue(/status:\s*experimental/i.test(readme), "README must disclose experimental status");
if (errors.length) { console.error(errors.join("\n")); process.exit(1); }
console.log(`${pkg.name}@${pkg.version} protocol validation passed`);
