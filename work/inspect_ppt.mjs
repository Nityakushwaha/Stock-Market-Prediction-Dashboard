import { pathToFileURL } from "node:url";
const { importRuntimeModule } = await import(pathToFileURL("C:/Users/ARJIT/.codex/plugins/cache/openai-primary-runtime/presentations/26.1020.11127/skills/presentations/container_tools/runtime_helpers.mjs").href);
import { writeFile } from "node:fs/promises";
const { FileBlob, PresentationFile } = await importRuntimeModule("@oai/artifact-tool");
for (const file of ["D:/whatsaap/GLBITM PPT Format.pptx","D:/whatsaap/GLBITM POSTER Format.pptx"]) {
 const p = await PresentationFile.importPptx(await FileBlob.load(file));
 console.log("\nFILE",file,"slides",p.slides.items.length);
 p.slides.items.forEach((s,i)=>{
  console.log("\nSLIDE",i+1);
  for (const sh of s.shapes.items) {
   const tx=String(sh.text??"").replace(/\s+/g," ").trim();
   console.log(JSON.stringify({id:sh.id,name:sh.name,text:tx.slice(0,220),pos:sh.position}));
  }
  for (const t of (s.tables?.items ?? [])) console.log("TABLE", JSON.stringify({id:t.id, name:t.name, rows:t.rowCount, cols:t.columnCount, position:t.position}));
 });
}
