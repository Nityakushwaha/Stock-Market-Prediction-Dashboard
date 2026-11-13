import fs from "node:fs/promises";
import path from "node:path";
import {pathToFileURL} from "node:url";
const ROOT="D:/gitprojects/financial-news-intelligence-platform-main/financial-news-intelligence-platform-main";
const SKILL="C:/Users/ARJIT/.codex/plugins/cache/openai-primary-runtime/presentations/26.1020.11127/skills/presentations";
const {importRuntimeModule}=await import(pathToFileURL(path.join(SKILL,"container_tools/runtime_helpers.mjs")).href);
const {FileBlob,PresentationFile}=await importRuntimeModule("@oai/artifact-tool");
const {finalizePresentation}=await import(pathToFileURL(path.join(SKILL,"container_tools/artifact_tool_utils.mjs")).href);
const src=path.join(ROOT,"deliverables","Stock_Market_Prediction_Dashboard_Presentation_Final.pptx");
const p=await PresentationFile.importPptx(await FileBlob.load(src));
for(const slide of p.slides.items){
 const h=slide.shapes.items.find(x=>x.name==="Rectangle 11");
 if(h && String(h.text??"").trim()) h.text.style={fontSize:22,typeface:"Garamond",color:"#FFFFFF",bold:true,alignment:"center",verticalAlignment:"middle",autoFit:"shrinkText"};
}
const BUILD=path.join(ROOT,"tmp","presentation_build");
const candidate=path.join(BUILD,"presentation-titlebar-candidate.pptx");
await(await PresentationFile.exportPptx(p)).save(candidate);
const final=path.join(ROOT,"deliverables","Stock_Market_Prediction_Dashboard_Presentation_Final_v2.pptx");
await finalizePresentation({
 workspaceDir:ROOT,candidatePath:candidate,finalPath:final,
 pythonExecutable:"C:/Users/ARJIT/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe",
 integrityValidatorPath:path.join(SKILL,"container_tools/inspect_presentation_package_integrity.py"),
 layoutValidatorPath:path.join(SKILL,"container_tools/inspect_presentation_layout_geometry.py"),
 layoutArgs:["--expected-slide-size-emu","12192000,6858000","--validate-heading-fit","--require-native-table-slide","6"],
 requiredNativeTableOwnerSlides:[6],verifyArtifactToolImport:true,
 receiptPath:path.join(BUILD,"presentation-validation-final-v2.json")
});
console.log(final);

