import fs from "node:fs/promises";
import path from "node:path";
import {pathToFileURL} from "node:url";
const ROOT="D:/gitprojects/financial-news-intelligence-platform-main/financial-news-intelligence-platform-main";
const SKILL="C:/Users/ARJIT/.codex/plugins/cache/openai-primary-runtime/presentations/26.1020.11127/skills/presentations";
const {importRuntimeModule}=await import(pathToFileURL(path.join(SKILL,"container_tools/runtime_helpers.mjs")).href);
const {FileBlob,PresentationFile}=await importRuntimeModule("@oai/artifact-tool");
const {finalizePresentation}=await import(pathToFileURL(path.join(SKILL,"container_tools/artifact_tool_utils.mjs")).href);
const p=await PresentationFile.importPptx(await FileBlob.load(path.join(ROOT,"deliverables","Stock_Market_Prediction_Dashboard_Presentation_Final.pptx")));
const s=p.slides.items[10].shapes.items.find(x=>x.name==="Rectangle 1");
if(!s)throw new Error("Screenshot-note placeholder not found");
s.text="Insert a fresh screenshot from the final running dashboard here before submission.\n\nShow the news sentiment view only.\nFinBERT confidence refers to article-tone classification,\nnot a 12-month growth probability.";
s.position={left:285,top:180,width:900,height:285};
s.text.style={fontSize:20,typeface:"Garamond",color:"#222222",wrap:"square",autoFit:"shrinkText"};
const BUILD=path.join(ROOT,"tmp","presentation_build");
const candidate=path.join(BUILD,"presentation-repaired-candidate.pptx");
await(await PresentationFile.exportPptx(p)).save(candidate);
const final=path.join(ROOT,"deliverables","Stock_Market_Prediction_Dashboard_Presentation_Ready.pptx");
await finalizePresentation({
 workspaceDir:ROOT,candidatePath:candidate,finalPath:final,
 pythonExecutable:"C:/Users/ARJIT/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe",
 integrityValidatorPath:path.join(SKILL,"container_tools/inspect_presentation_package_integrity.py"),
 layoutValidatorPath:path.join(SKILL,"container_tools/inspect_presentation_layout_geometry.py"),
 layoutArgs:["--expected-slide-size-emu","12192000,6858000","--validate-heading-fit","--require-native-table-slide","6"],
 requiredNativeTableOwnerSlides:[6],verifyArtifactToolImport:true,
 receiptPath:path.join(BUILD,"presentation-validation-ready.json")
});
console.log(final);

