import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const textExtensions = new Set([".html", ".js", ".json", ".css"]);

function walk(directory) {
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const fullPath = path.join(directory, entry.name);
    return entry.isDirectory() ? walk(fullPath) : [fullPath];
  });
}

for (const file of walk(root)) {
  if (!textExtensions.has(path.extname(file))) continue;

  let content = fs.readFileSync(file, "utf8");
  const original = content;

  content = content
    .replaceAll('"/avto-car-motors.ru/"', '"index.html"')
    .replaceAll('\\"/avto-car-motors.ru/\\"', '\\"index.html\\"')
    .replaceAll("/avto-car-motors.ru/", "")
    .replaceAll("/_next/", "_next/")
    .replaceAll(
      "https://halalhalalvov-cloud.github.io/avto-car-motors.ru",
      "https://polymat-coder.github.io/olimp-group",
    )
    .replaceAll("https://avto-car-motors.ru/logo.ico", "icon.ico")
    .replaceAll("https://avto-car-motors.ru/favicon.ico", "icon.ico");

  if (
    path.extname(file) === ".html" &&
    !content.includes('src="static-navigation.js')
  ) {
    content = content.replace(
      "</body>",
      '<script src="static-navigation.js"></script></body>',
    );
  }

  if (path.extname(file) === ".html") {
    content = content.replace(
      /src="static-navigation\.js(?:\?v=\d+)?"/,
      'src="static-navigation.js?v=5"',
    );
  }

  if (content !== original) {
    fs.writeFileSync(file, content, "utf8");
  }
}

const manifestPath = path.join(root, "manifest.json");
const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
manifest.start_url = "./";
manifest.scope = "./";
manifest.icons = manifest.icons.map((icon) => ({ ...icon, src: "logo.jpg" }));
fs.writeFileSync(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
