import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";
const SKILL="C:/Users/ARJIT/.codex/plugins/cache/openai-primary-runtime/presentations/26.1020.11127/skills/presentations";
const {importRuntimeModule}=await import(pathToFileURL(path.join(SKILL,"container_tools/runtime_helpers.mjs")).href);
const {FileBlob,PresentationFile}=await importRuntimeModule("@oai/artifact-tool");
const {finalizePresentation}=await import(pathToFileURL(path.join(SKILL,"container_tools/artifact_tool_utils.mjs")).href);
const ROOT="D:/gitprojects/financial-news-intelligence-platform-main/financial-news-intelligence-platform-main";
const OUT=path.join(ROOT,"deliverables"), BUILD=path.join(ROOT,"tmp","presentation_build");
await fs.mkdir(OUT,{recursive:true}); await fs.mkdir(BUILD,{recursive:true});
const pptTemplate="D:/whatsaap/GLBITM PPT Format.pptx";
const posterTemplate="D:/whatsaap/GLBITM POSTER Format.pptx";
const slides=(p)=>p.slides.items;
function shape(slide,id){const s=slide.shapes.items.find(x=>String(x.id)===String(id));if(!s)throw Error("Missing shape "+id);return s;}
function set(slide,id,text,size=20){const s=shape(slide,id);s.text=text;s.text.style={fontSize:size,typeface:"Garamond",color:"#222222",wrap:"square",autoFit:"shrinkText"};return s;}
function addText(slide,text,pos,size=18,color="#222222",bold=false){
 const s=slide.shapes.add({geometry:"textbox",name:"Project content",position:pos,fill:"none",line:{style:"solid",fill:"none",width:0},text:{text,style:{fontSize:size,typeface:"Garamond",color,bold,wrap:"square",autoFit:"shrinkText",insets:{left:4,right:4,top:3,bottom:3}}}});
 return s;
}
function title(s,id,text){const sh=shape(s,id);sh.text=text;}
const deck=await PresentationFile.importPptx(await FileBlob.load(pptTemplate));
const S=slides(deck);
set(S[0],"12","STOCK MARKET PREDICTION DASHBOARD",25);
set(S[0],"3","SESSION 2026–2027",21);
set(S[0],"2","PRESENTED BY:\n[STUDENT NAME] — [ROLL NO.]\n[ADD TEAM MEMBERS]",17);
set(S[0],"14","UNDER SUPERVISION OF:\n[SUPERVISOR NAME]\n[DESIGNATION]\nGL BAJAJ",17);
const bodies={
1:"A research dashboard for understanding company news and testing whether dated news sentiment, fundamentals, sector context, and search interest can inform a long-term Indian equity outlook. Current app summarizes news tone; it does not yet produce a validated price-growth forecast.",
2:"1. Search company news and summarize sentiment.\n2. Combine dated news with company and sector indicators (planned).\n3. Define a 12-month positive/non-positive return target.\n4. Compare simple and explainable models chronologically.\n5. Show uncertainty and feature contributions; avoid buy/sell advice.",
3:"Hardware: Windows PC, 8 GB RAM minimum (16 GB recommended for local model inference), internet for provider/model access.\nSoftware: Python, Streamlit, pandas, Transformers/PyTorch, Plotly, scikit-learn (planned model), Git. Provider API credentials are configured privately; do not expose them in screenshots.",
4:"Base system: a working Streamlit financial-news dashboard using NewsAPI, Marketaux, and Finnhub adapters, article deduplication/relevance ranking, and ProsusAI FinBERT tone classification.\nRelated research motivates financial NLP and attention measures. The repository’s prior return experiment reported weak out-of-sample persistence; it is preliminary and not reproduced for this presentation.",
6:"Motivation: users face scattered news and can confuse positive article tone with future price growth. Proposed extension tests a clearly defined 12-month outcome using point-in-time fundamentals, sector context, and search attention. Valuation/risk must be defined separately. No investment signal is claimed until temporal tests beat simple baselines.",
};
for(const [idx,txt] of Object.entries(bodies)){const sl=S[Number(idx)];const body=sl.shapes.items.find(x=>String(x.id)==="3"||String(x.id)==="6");body.text=txt;body.position={...body.position,top:150,height:460,width:930};body.text.style={fontSize:21,typeface:"Garamond",color:"#222222",wrap:"square",autoFit:"shrinkText"};}
set(S[2],"12","OBJECTIVES",24);
set(S[4],"12","EXISTING SYSTEM / RELATED WORK",22);
set(S[5],"12","LITERATURE SURVEY",23);
set(S[6],"12","MOTIVATION / PROBLEM STATEMENT",22);
set(S[7],"12","PROPOSED PROJECT WORKFLOW",23);
set(S[8],"12","PROJECT MODULES — CURRENT AND PROPOSED",21);
set(S[9],"12","MODULE DESIGN AND DATA FLOW",22);
set(S[10],"12","CURRENT PROTOTYPE STATUS",22);
set(S[11],"12","CONCLUSION AND FUTURE SCOPE",22);
set(S[12],"12","REFERENCES",23);
// Flow slide: preserve original flow shapes/arrows and clarify implementation status.
set(S[7],"6","WORKING BASE\nNews retrieval + FinBERT\narticle-tone analysis",16);
set(S[7],"8","PROPOSED MODIFICATIONS\n12-month labels + fundamentals\nsector + search attention",16);
set(S[7],"11","EVALUATE\nChronological holdout\ncalibration + explanations",16);
set(S[7],"13","RESPONSIBLE OUTPUT\nGrowth outlook + uncertainty\nnot investment advice",16);
// Modules slide: retain numbered template labels; add editable descriptions.
set(S[8],"6","MODULE 1",19);set(S[8],"8","MODULE 2",19);set(S[8],"11","MODULE 3",19);
addText(S[8],"News aggregation: fetch, deduplicate, and rank articles from configured providers.",{left:470,top:145,width:690,height:66},18);
addText(S[8],"FinBERT sentiment: estimate positive / neutral / negative article tone and summarize it.",{left:470,top:268,width:690,height:80},18);
addText(S[8],"Growth research (in progress): build 12-month labels; join dated fundamentals and validate a model.",{left:470,top:418,width:690,height:95},18);
// Module details slide: split into current prototype and proposed extension.
set(S[9],"2","IMPLEMENTED TODAY",22);
addText(S[9],"News search • provider aggregation • article deduplication • relevance ranking • FinBERT tone • charts • comparison • CSV export",{left:285,top:175,width:920,height:105},19);
addText(S[9],"NEXT RESEARCH PHASE\nDefine India universe and dated data → join news, margins, sector and Trends → train a baseline → evaluate chronologically → explain output.\n\nThe 12-month label helper is tested; a growth classifier, risk score and valuation module are not integrated yet.",{left:285,top:350,width:920,height:210},19);
// Literature survey table, preserving template table location and editable cells.
const table=S[5].tables.items[0];
for(let c=table.columnCount-1;c>=5;c--)table.deleteColumns({index:c});
table.insertRows({index:2,count:2});
const survey=[
["Study / source","Method / focus","Relevance","Takeaway","Status here"],
["Araci (2019)","FinBERT financial NLP","Article tone","Domain-adapted text model","Used in prototype"],
["Da et al. (2011)","Search volume / attention","Investor attention","Attention ≠ fundamentals","Candidate feature"],
["Lundberg & Lee (2017)","SHAP attribution","Interpretability","Explanation ≠ causation","Planned"],
];
survey.forEach((row,r)=>row.forEach((v,c)=>table.cells.set(r,c,v)));
for(let c=0;c<5;c++)table.columns.get(c).width=208;
for(let r=0;r<4;r++)table.rows[r].height=90;
table.cells.block({row:0,column:0,rowCount:4,columnCount:5}).textStyle.fontSize=13;
// Current screenshot from the checked-in prototype; state its legacy label so it isn't mistaken for final branding.
const screenshotNote=shape(S[10],"2");
screenshotNote.text="Insert a fresh screenshot from the final running dashboard here before submission.\n\nShow the news sentiment view only. FinBERT confidence refers to article-tone classification, not a 12-month growth probability.";
screenshotNote.position={left:285,top:190,width:900,height:260};
screenshotNote.text.style={fontSize:20,typeface:"Garamond",color:"#222222",wrap:"square",autoFit:"shrinkText"};
set(S[11],"6","CURRENT\nCompany news retrieval, FinBERT sentiment, article feed, comparison, and export.\n\nNEXT\nValidated Indian-equity 12-month outlook using dated features, baselines, chronological testing, and explanations.\n\nLIMITS\nSentiment is not a stock forecast. Valuation and risk outputs remain future work. Educational use only.",18);
set(S[12],"2","[1] Araci (2019). FinBERT. arXiv:1908.10063. arxiv.org/abs/1908.10063\n[2] Da, Engelberg & Gao (2011). In Search of Attention. Journal of Finance 66(5). doi:10.1111/j.1540-6261.2011.01679.x\n[3] Lundberg & Lee (2017). A Unified Approach to Interpreting Model Predictions. NeurIPS 30.\n[4] ProsusAI/finbert model card. Hugging Face.\n[5] Student project source: README, app.py, growth_labels.py, tests. Reviewed 22 Oct 2026.",14);
set(S[12],"3","");
set(S[13],"3","Thank You");
const deckCandidate=path.join(BUILD,"deck-candidate.pptx");
await (await PresentationFile.exportPptx(deck)).save(deckCandidate);
const finalPpt=path.join(OUT,"Stock_Market_Prediction_Dashboard_Presentation_Final.pptx");
await finalizePresentation({
 workspaceDir:ROOT,candidatePath:deckCandidate,finalPath:finalPpt,pythonExecutable:"C:/Users/ARJIT/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe",
 integrityValidatorPath:path.join(SKILL,"container_tools/inspect_presentation_package_integrity.py"),
 layoutValidatorPath:path.join(SKILL,"container_tools/inspect_presentation_layout_geometry.py"),
 layoutArgs:["--expected-slide-size-emu","12192000,6858000","--validate-bullet-geometry","--validate-heading-fit","--require-native-table-slide","6"],
 requiredNativeTableOwnerSlides:[6],
 verifyArtifactToolImport:true,receiptPath:path.join(BUILD,"presentation-validation-final.json")
});
console.log(finalPpt);
// Poster template: all panels stay editable and aligned to the supplied layout.
const poster=await PresentationFile.importPptx(await FileBlob.load(posterTemplate));const P=slides(poster)[0];
set(P,"13","Project Title: Stock Market Prediction Dashboard\nSubtitle: An Explainable Indian Equity Growth Outlook System\nTeam Members: [NAME — ROLL NO.]\n[ADD MEMBERS]\nSupervisor: [NAME, DESIGNATION]",14);
set(P,"23","SESSION (2026–2027)  |  BATCH – 2023  |  FINAL YEAR PROJECT EVALUATION",20);
shape(P,"23").text.style={fontSize:20,typeface:"Garamond",color:"#FFFFFF",bold:true,alignment:"center"};
set(P,"15","This project begins with a working financial-news dashboard using FinBERT to summarize article tone. It proposes testing whether news, company fundamentals, Indian sector context, and search interest can support a 12-month equity growth outlook. Sentiment alone is not a return forecast.",15);
set(P,"16","Problem: financial news is scattered and sentiment can be confused with future growth. Scope: Indian equities, point-in-time data, a 12-month positive/non-positive adjusted-return target, transparent validation, and cautious interpretation.",15);
set(P,"17","CURRENT: Streamlit company search; NewsAPI / Marketaux / Finnhub adapters; article deduplication and relevance ranking; FinBERT positive/neutral/negative tone; charts, comparison, CSV export.\n\nPROPOSED: dated fundamentals + sector growth + Google Trends attention; baseline/model comparison; time-ordered evaluation; explanations and risk/valuation definitions.",14);
set(P,"18","Working prototype: news retrieval and FinBERT article sentiment. A tested utility constructs 12-month return labels from adjusted prices. No integrated growth classifier, valuation label, or risk score is claimed yet. Next: validate against an untouched later period. Educational research only; not investment advice.",14);
set(P,"19","Current prototype: news retrieval and FinBERT tone summary. The 12-month label helper is tested.\n\nPlanned evaluation: baseline comparison and chronological holdout. Prior README backtest not reproduced here; no 12-month classifier result is claimed.",13);
set(P,"20","Current: working news/sentiment prototype plus tested 12-month label utility.\n\nNext: build and validate a point-in-time Indian-equity outlook. This is academic research, not investment advice.",14);
set(P,"21","References:\nAraci (2019), FinBERT, arXiv:1908.10063.\nDa, Engelberg & Gao (2011), In Search of Attention, Journal of Finance.\nLundberg & Lee (2017), SHAP, NeurIPS.\nProsusAI/finbert model card.\nStudent project source, reviewed 22 Oct 2026.",13);
set(P,"22","1. Universe + dated data\n2. News relevance + FinBERT\n3. Point-in-time fundamentals, sector and search features\n4. 12-month target labels\n5. Chronological baseline/model tests\n6. Calibrated outlook + feature explanations",15);
set(P,"4","Group ID: [GROUP ID]",16);
const posterCandidate=path.join(BUILD,"poster-candidate.pptx");
await (await PresentationFile.exportPptx(poster)).save(posterCandidate);
const finalPoster=path.join(OUT,"Stock_Market_Prediction_Dashboard_Poster_Final.pptx");
await finalizePresentation({
 workspaceDir:ROOT,candidatePath:posterCandidate,finalPath:finalPoster,pythonExecutable:"C:/Users/ARJIT/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe",
 integrityValidatorPath:path.join(SKILL,"container_tools/inspect_presentation_package_integrity.py"),
 layoutValidatorPath:path.join(SKILL,"container_tools/inspect_presentation_layout_geometry.py"),
 layoutArgs:["--expected-slide-size-emu","9601200,12801600","--validate-bullet-geometry","--validate-heading-fit"],
 verifyArtifactToolImport:true,
 receiptPath:path.join(BUILD,"poster-validation-final.json")
});
console.log(finalPoster);

