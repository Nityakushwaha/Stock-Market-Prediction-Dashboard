from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT=Path(r"D:\gitprojects\financial-news-intelligence-platform-main\financial-news-intelligence-platform-main")
OUT=ROOT/"deliverables"; OUT.mkdir(exist_ok=True)
doc=Document(); sec=doc.sections[0]
sec.top_margin=Inches(.75); sec.bottom_margin=Inches(.7); sec.left_margin=Inches(.85); sec.right_margin=Inches(.85)
NAVY="17365D"; GRAY="666666"
for nm,sz in [("Normal",11),("Title",22),("Heading 1",16),("Heading 2",13),("Heading 3",11)]:
 s=doc.styles[nm]; s.font.name="Times New Roman"; s.font.size=Pt(sz)
 if nm!="Normal": s.font.bold=True; s.font.color.rgb=RGBColor.from_string(NAVY)
 s._element.rPr.rFonts.set(qn("w:eastAsia"),"Times New Roman")
doc.styles["Normal"].paragraph_format.space_after=Pt(5)
head=sec.header.paragraphs[0]; head.alignment=WD_ALIGN_PARAGRAPH.CENTER
rr=head.add_run("GL BAJAJ INSTITUTE OF TECHNOLOGY AND MANAGEMENT | SESSION 2026–2027"); rr.font.size=Pt(8); rr.font.color.rgb=RGBColor.from_string(GRAY)
foot=sec.footer.paragraphs[0]; foot.alignment=WD_ALIGN_PARAGRAPH.CENTER; foot.add_run("Stock Market Prediction Dashboard • Page ")
fld=OxmlElement("w:fldSimple"); fld.set(qn("w:instr"),"PAGE"); foot._p.append(fld)

def para(txt="",align=None,italic=False,bold=False):
 x=doc.add_paragraph()
 if align is not None:x.alignment=align
 r=x.add_run(txt);r.italic=italic;r.bold=bold;return x
def heading(txt,l=1):doc.add_heading(txt,level=l)
def page():doc.add_page_break()
def shade(cell,color):
 pr=cell._tc.get_or_add_tcPr();s=OxmlElement("w:shd");s.set(qn("w:fill"),color);pr.append(s)
def tab(headers,rows):
 t=doc.add_table(rows=1,cols=len(headers));t.style="Table Grid";t.alignment=WD_TABLE_ALIGNMENT.CENTER
 for i,v in enumerate(headers):
  c=t.rows[0].cells[i];c.text=str(v);shade(c,NAVY)
  for r in c.paragraphs[0].runs:r.bold=True;r.font.color.rgb=RGBColor(255,255,255);r.font.size=Pt(9)
 for row in rows:
  cells=t.add_row().cells
  for i,v in enumerate(row):
   cells[i].text=str(v);cells[i].vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
   for p in cells[i].paragraphs:
    p.paragraph_format.space_after=Pt(1)
    for r in p.runs:r.font.size=Pt(9)
 doc.add_paragraph()
def bullets(items):
 for v in items:doc.add_paragraph(v,style="List Bullet")
def nums(items):
 for i,v in enumerate(items,1):para(f"{i}. {v}")

# Cover
para("GL BAJAJ INSTITUTE OF TECHNOLOGY AND MANAGEMENT",WD_ALIGN_PARAGRAPH.CENTER,bold=True)
para("Greater Noida, Uttar Pradesh",WD_ALIGN_PARAGRAPH.CENTER)
para("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING (ARTIFICIAL INTELLIGENCE)",WD_ALIGN_PARAGRAPH.CENTER,bold=True)
logos=doc.add_table(rows=1,cols=2);logos.alignment=WD_TABLE_ALIGNMENT.CENTER
for cell in logos.rows[0].cells:cell.paragraphs[0].alignment=WD_ALIGN_PARAGRAPH.CENTER
logos.cell(0,0).paragraphs[0].add_run().add_picture(str(ROOT/"tmp"/"template_review"/"Im2.png"),width=Inches(1.35))
logos.cell(0,1).paragraphs[0].add_run().add_picture(str(ROOT/"tmp"/"template_review"/"Im1.jpg"),width=Inches(2.0))
doc.add_paragraph().paragraph_format.space_after=Pt(1)
para("PROJECT REPORT",WD_ALIGN_PARAGRAPH.CENTER,bold=True)
para("STOCK MARKET PREDICTION DASHBOARD",WD_ALIGN_PARAGRAPH.CENTER,bold=True)
para("An Explainable Indian Equity Growth Outlook System",WD_ALIGN_PARAGRAPH.CENTER,italic=True)
para("Submitted in partial fulfilment of the requirements for the award of the degree of\nBachelor of Technology in Computer Science and Engineering (Artificial Intelligence)",WD_ALIGN_PARAGRAPH.CENTER)
para("Submitted by\n[STUDENT NAME] | [ROLL NUMBER]\n[ADD OTHER TEAM MEMBERS, IF APPLICABLE]\n\nUnder the guidance of\n[SUPERVISOR NAME], [DESIGNATION]\n\nAcademic Session 2026–2027\nSubmission date: [DD MONTH 2026]",WD_ALIGN_PARAGRAPH.CENTER)
page()
heading("DECLARATION")
para("We declare that the project report entitled “Stock Market Prediction Dashboard: An Explainable Indian Equity Growth Outlook System” is prepared as part of the B.Tech CSE (AI) project work during academic session 2026–2027. Sources are acknowledged. Implementation status and limitations are stated transparently. This draft contains identity and approval fields to complete before submission.")
para("Place: Greater Noida     Date: [DATE]\n\n[STUDENT SIGNATURE(S)]\n[NAME(S) AND ROLL NUMBER(S)]")
page()
heading("CERTIFICATE")
para("This is to certify that the project report entitled “Stock Market Prediction Dashboard: An Explainable Indian Equity Growth Outlook System” is submitted by [STUDENT NAME(S)], [ROLL NUMBER(S)], of the Department of Computer Science and Engineering (Artificial Intelligence), GL Bajaj Institute of Technology and Management, during academic session 2026–2027, under my supervision.")
para("The current prototype analyses financial-news sentiment. Growth, valuation, and risk outputs described in this report are proposed extensions and are not presented as validated investment forecasts.")
para("Supervisor: [NAME AND DESIGNATION]\nSignature: ____________________     Date: ____________________")
page()
heading("ACKNOWLEDGEMENT")
para("We express our sincere gratitude to our project supervisor, [SUPERVISOR NAME], for guidance and feedback. We thank the Department of CSE (AI), GL Bajaj Institute of Technology and Management, and acknowledge the open-source libraries and research cited herein. Provider terms, data licences, and attribution requirements will be followed in demonstrations and distribution.")
page()
heading("ABSTRACT")
para("This project develops a dashboard for examining financial news about publicly traded companies and proposes a research extension that tests whether news and selected company/sector indicators can support an explainable long-term outlook for Indian equities. The working prototype is a Streamlit application: it queries configured news providers, aggregates and filters articles, applies the ProsusAI FinBERT financial-language model, and presents sentiment summaries, article feeds, comparisons, charts, and CSV export. The repository also contains a tested utility for creating a positive/non-positive label from adjusted prices at a 12-month horizon; it is not yet integrated with a trained prediction model or user-facing recommendation.")
para("The proposed next stage combines dated news sentiment with fundamentals such as year-on-year profit-margin change, sector context, and Google Trends search interest. The provisional target is a positive versus non-positive 12-month adjusted return. A calibrated growth outlook, a separately defined risk indicator, peer-relative valuation only where suitable data exists, and feature-level explanations will be evaluated. Chronological validation, leakage prevention, baseline comparisons, and uncertainty reporting are required before any predictive claim. This is an educational research prototype, not investment advice.")
para("Keywords: financial NLP, FinBERT, Indian equities, Streamlit, sentiment analysis, explainable machine learning.")
page()
heading("CONTENTS")
para("Update the Table of Contents in Word after opening this editable report.",italic=True)
for x in ["Declaration ..................................................... 2","Certificate ..................................................... 3","Acknowledgement ............................................. 4","Abstract ........................................................... 5","List of Figures and Tables ................................. 7","Chapter 1 — Introduction .................................... 8","Chapter 2 — Literature Review ............................. 9","Chapter 3 — System Analysis and Design .............. 9","Chapter 4 — Implementation and Current Results .. 11","Chapter 5 — Proposed Growth Outlook Methodology 12","Chapter 6 — Testing, Evaluation and Discussion ... 13","Chapter 7 — Conclusion and Future Work ............. 13","References ..................................................... 14","Appendix — Submission Checklist ..................... 14"]:para(x)
page()
heading("LIST OF FIGURES AND TABLES")
para("Figures: 3.1 Proposed architecture; 3.2 Research workflow; 4.1 Current dashboard screenshot; 4.2 Article/comparison screenshot; 5.1 Chronological evaluation design.")
para("Tables: 1.1 Objectives; 2.1 Related work; 3.1 Requirements; 3.2 Technology stack; 4.1 Status; 5.1 Candidate features; 6.1 Evaluation metrics.")
page()

heading("CHAPTER 1 — INTRODUCTION")
heading("1.1 Background",2)
para("Investors face a large volume of corporate announcements, news, market commentary, and financial statements. Financial-domain language models can classify article tone, but tone is not a direct measurement of future returns. A useful research system must align information with market dates, define an outcome, and evaluate it on unseen future periods.")
para("This project starts with a working news-intelligence dashboard and aims to extend it into a research tool for Indian listed equities. The future tool will combine news with company fundamentals, sector context, and public search-interest measures. It is intended to support evidence inspection, not issue buy/sell instructions.")
heading("1.2 Problem statement",2)
para("Users must gather company news from multiple sources and interpret it manually. Automated sentiment can help summarize language, but a positive label can be mistaken for a positive price forecast. The project addresses this usability gap and proposes a separate, testable workflow to assess whether selected dated information has value for a defined long-term outcome.")
heading("1.3 Aim and objectives",2)
tab(["No.","Objective","Status"],[
("1","Build dashboard for company news search and sentiment summaries.","Prototype implemented"),
("2","Aggregate, deduplicate, rank, and display news.","Prototype implemented"),
("3","Apply FinBERT to articles and show sentiment.","Implemented"),
("4","Define a 12-month positive/non-positive return target.","Helper implemented and unit-tested"),
("5","Explore fundamentals, sector growth, and search attention.","Proposed"),
("6","Train/evaluate an explainable Indian-equity model chronologically.","Proposed"),
("7","Present uncertainty and limitations without implying certainty.","Proposed")])
heading("1.4 Scope and boundaries",2)
para("Current scope: Streamlit interface, multi-provider news retrieval, article processing, sentiment analysis, and descriptive summaries. Planned research scope: an Indian equity subset with adequate historical news and adjusted-price coverage. The exact return target and universe require supervisor approval. Peer-relative valuation is distinct from sentiment and cannot be inferred from news alone.")
bullets(["Sentiment describes estimated article tone; it is not the probability a stock will rise.","Any 12-month classifier is uncertain and is not a guaranteed forecast.","Data access, search-index normalization, corporate actions, missing disclosures, and survivorship can affect results.","This academic prototype is not personalized investment advice."])

heading("CHAPTER 2 — LITERATURE REVIEW")
heading("2.1 Financial text sentiment",2)
para("Araci (2019) introduced FinBERT, adapting BERT-based language modeling to financial sentiment classification. This project uses ProsusAI/finbert through Transformers. Article-tone classification does not by itself establish causal impact on stock returns.")
heading("2.2 Search interest and attention",2)
para("Da, Engelberg, and Gao (2011) studied search volume as an investor-attention proxy in a U.S. equity setting. This motivates testing search interest as an attention feature, not as a standalone bullish signal. Google Trends values are normalized indices, not absolute counts; query, geography, period, and retrieval date must be recorded.")
heading("2.3 Model explanation",2)
para("Lundberg and Lee (2017) proposed SHAP as a framework for attributing model outputs to input features. SHAP can help inspect a prediction but does not prove that a feature caused the market outcome. Explanations must be paired with out-of-sample performance and calibration.")
heading("2.4 Related work and gap",2)
tab(["Work","Relevance","Project implication"],[
("Araci (2019), FinBERT","Financial-domain sentiment model.","Use tone as an input; separately validate the prediction task."),
("Da et al. (2011), attention","Search volume as attention in a U.S. study.","Test Indian-market relevance; do not interpret as fundamentals."),
("Lundberg & Lee (2017), SHAP","Feature attribution.","Explain model outputs, not causal mechanisms."),
("Repository README research note","Reports 2022/2023 sentiment-return experiment; out-of-sample association reportedly weak/insignificant.","Context only: not reproduced from raw data for this report.")])
heading("2.5 Research gap",2)
para("The engineering gap is to connect a usable dashboard to a clean, point-in-time Indian equity dataset and a defensible evaluation protocol. A complex model should only be preferred if it improves on transparent baselines on unseen periods and remains calibrated.")

heading("CHAPTER 3 — SYSTEM ANALYSIS AND DESIGN")
heading("3.1 Existing system",2)
para("The current app accepts one or more company names, retrieves recent news using configured providers, deduplicates and ranks articles, applies FinBERT sentiment to article text, and renders article-level and summary views. It supports multi-company comparison and CSV download. Credentials are local configuration and are intentionally excluded from this report.")
heading("3.2 Proposed architecture and workflow",2)
tab(["Layer","Responsibility / status"],[
("Presentation","Streamlit search, summaries, comparisons, feed, charts, export; future outlook panel."),
("News services","Adapters for NewsAPI, Marketaux, Finnhub; deduplication and relevance ranking."),
("NLP","FinBERT positive/neutral/negative article-tone probabilities."),
("Point-in-time data","Future: align news, prices, fundamentals, sector, search interest."),
("Target","Current utility: 12-month adjusted-price return and binary label."),
("Model/evaluation","Future: baseline/classifier, time-ordered evaluation, calibration, explanations.")])
para("Research workflow: choose universe → obtain dated inputs → validate and deduplicate → create sentiment/fundamental/search features → join only information available as of each date → create 12-month labels → chronological split → baseline comparison → calibrated outlook and explanations → dashboard with limitations.")
heading("3.3 Requirements",2)
tab(["ID","Requirement","Status"],[
("FR-01","Search company news and show relevant articles.","Implemented"),
("FR-02","Show sentiment summary and source/article context.","Implemented"),
("FR-03","Compare companies and export article data.","Implemented"),
("FR-04","Show 12-month outlook only after validated model integration.","Proposed"),
("FR-05","Show data coverage, uncertainty, explanations, and caveats.","Proposed"),
("FR-06","Provide valuation/risk view using separate definitions.","Proposed")])
heading("3.4 Technology stack",2)
tab(["Technology","Role"],[
("Python","Application and analysis"),("Streamlit","Interactive dashboard"),("pandas / NumPy","Tabular data processing"),
("Transformers / PyTorch","FinBERT inference"),("Plotly","Interactive charts"),("scikit-learn","Planned baseline modeling/evaluation"),
("NewsAPI, Marketaux, Finnhub","Configured news providers"),("Git","Version control; confirm repository status locally")])
heading("3.5 Quality and security",2)
bullets(["Record dataset source, date, model version, parameters, and splits for reproducibility.","Keep credentials out of source control and screenshots.","Handle provider failures and stale/missing data visibly.","Distinguish observed sentiment from forecast output in labels and layout.","Follow data-provider licensing and attribution requirements."])

heading("CHAPTER 4 — IMPLEMENTATION AND CURRENT RESULTS")
heading("4.1 Current application flow",2)
nums(["User enters a company name or comma-separated names.","Provider adapters request relevant articles; a failed provider does not necessarily stop other providers.","Articles are deduplicated and company relevance is ranked.","FinBERT processes article title and description and assigns sentiment probabilities.","Dashboard renders summaries and article tables; comparison and CSV export are available."])
heading("4.2 Verified code-level status",2)
para("The reviewed source has a Streamlit entry point, a news pipeline and aggregator, provider implementations for NewsAPI, Marketaux, and Finnhub, and a sentiment analyzer using ProsusAI/finbert. The analyzer returns class probabilities and a most-likely label. The app explicitly warns that sentiment is not a prediction of future share-price growth.")
para("src/analytics/growth_labels.py contains a helper that finds the first adjusted price on/after the 12-month anniversary within a default seven-calendar-day tolerance, computes forward return, and labels returns above zero positive and zero/below non-positive. Unit tests cover sorting, target gaps, zero return, and duplicate ticker-date rejection. This is target construction, not an integrated trained prediction model.")
heading("4.3 Implemented versus proposed",2)
tab(["Capability","Status/evidence"],[
("News search and sentiment dashboard","Working prototype; student previously launched it."),
("FinBERT article sentiment","Implemented; reflects text tone, not growth probability."),
("Company comparison and CSV export","Implemented in current app."),
("12-month target labels","Helper and tests present; not integrated with model/data ingestion."),
("Indian-equity growth classification","Not integrated; proposed."),
("Profit margin, India sector growth, Google Trends","Not integrated; proposed data/features."),
("Peer-relative valuation and risk class","Not integrated; definitions/data still needed."),
("SHAP explanations","Not integrated; proposed after model selection.")])
heading("4.4 Existing exploratory analysis",2)
para("The repository README describes a separate experiment with 2022 training and 2023 chronological testing and reports that sentiment coefficients significant in the training period were statistically insignificant in the out-of-sample period. It also describes a NIFTY-50-related sample. The reviewed data/raw folder contains only a placeholder, and results were not independently reproduced for this report. These are repository-reported preliminary findings, not newly verified results and not evidence of a validated 12-month classifier. Reproduce from original data/scripts before retaining detailed figures in a final submission.")
heading("4.5 Screenshots",2)
para("Insert fresh screenshots from the final running app after verifying company, timestamp, and provider coverage. Never include API keys or credential files. Candidate repository images are assets/screenshots/dashboard-overview.png, article-feed.png, comparison-view.png, and search-results.png; verify each matches the demonstrated version.")

heading("CHAPTER 5 — PROPOSED GROWTH OUTLOOK METHODOLOGY")
heading("5.1 Provisional outcome definition",2)
para("For each stock and information date t, provisional return R(t,t+12m) = adjusted_close(t+12m) / adjusted_close(t) − 1, using the first valid trading observation on or after the 12-month anniversary within a documented tolerance. Label positive when R > 0 and non-positive otherwise. The current helper uses adjusted_close and a default 7-day calendar tolerance. Confirm whether the target should instead be benchmark-relative excess return and whether the price field incorporates dividends.")
heading("5.2 Candidate features and safeguards",2)
tab(["Feature family","Candidate data","Safeguard"],[
("News tone","Sentiment probabilities/score, article count, recency, source count.","Issuer link, timestamps, deduplication; only past information."),
("Company fundamentals","YoY profit-margin change, revenue/profit growth, leverage, valuation ratios.","Use publication/availability date, not fiscal-period end; account for revisions."),
("Sector / India context","Sector index return/growth, industry grouping, macro context.","Document source/date/classification; point-in-time availability."),
("Search attention","Google Trends India query-interest series.","Normalized index; save query, period, geography, retrieval date."),
("Market baseline","Lagged returns, volatility, benchmark return.","Compute strictly from past; compare with simple baselines.")])
heading("5.3 Research pipeline",2)
nums(["Choose a documented Indian equity universe and licensed dated price, fundamental, news, and search data.","Normalize identifiers, dates, units, and missingness; document coverage.","Create features using only values available at each prediction date.","Construct 12-month labels; remove rows with no valid future target.","Split chronologically and address overlapping 12-month labels with a purge/embargo strategy.","Fit prior/majority and logistic-regression baselines before testing more complex models.","Tune only on earlier validation windows; preserve a later untouched test set.","Evaluate discrimination, calibration, class errors, coverage, stability by year/sector, and baseline improvement.","Use SHAP or another suitable attribution method after model selection; present uncertainty and caveats."])
heading("5.4 Dashboard output and valuation",2)
para("Keep four concepts separate: observed article sentiment; model-estimated probability of positive 12-month outcome; an independently defined risk indicator (such as volatility/drawdown); and peer-relative valuation only when current fundamentals and comparators are defensible. Display the as-of date, data coverage, model version, baseline comparison, and limitations. Do not present a single buy/sell verdict.")
para("“Undervalued” and “overvalued” require a defined valuation framework and peer group. News tone alone cannot establish valuation. A later module could compare ratios such as P/E or EV/EBITDA within industry peers, adjusted for growth, leverage, and data quality. Until implemented, valuation remains proposed.")

heading("CHAPTER 6 — TESTING, EVALUATION AND DISCUSSION")
heading("6.1 Current test evidence",2)
para("Unit tests are present for the 12-month label helper and cover return direction, target-date tolerance, missing future prices, zero return, and duplicate dates. This report has not run the full project test suite; record actual pass/fail output, environment, and date before claiming full test success.")
heading("6.2 Proposed metrics",2)
tab(["Metric","Purpose"],[
("Balanced accuracy / macro-F1","Class performance under imbalance."),
("Precision and recall by class","Error trade-offs for positive and non-positive outcomes."),
("ROC-AUC / PR-AUC","Ranking quality; PR-AUC is useful with rare positives."),
("Brier score / calibration curve","Whether estimated probabilities match observed frequencies."),
("Coverage / missingness","How much of the target universe can be evaluated."),
("Baseline comparison","Whether features/models add value beyond simple prevalence or financial baselines.")])
heading("6.3 Threats to validity",2)
bullets(["Look-ahead leakage in filings, revised data, news timestamps, or search series.","Overlapping 12-month labels and correlated adjacent observations.","Survivorship and selection bias in a current-constituent universe.","Provider coverage gaps and issuer/ticker matching errors.","Regime shifts; the README’s prior note reports an in-sample/out-of-sample divergence.","Spurious sector, size, or regime proxies and weak sample size.","A useful classifier may not imply tradable returns after costs, liquidity, and taxes."])
heading("6.4 Responsible use",2)
para("This is an academic decision-support research prototype, not a registered adviser and not personalized advice. Any demonstration or deployment should show data timestamps, provider terms, limitations, and a visible warning that outputs are uncertain.")

heading("CHAPTER 7 — CONCLUSION AND FUTURE WORK")
para("The project has a tangible foundation: a working financial-news dashboard, provider aggregation, FinBERT sentiment, company comparison, and export. It also has tested 12-month outcome-label construction. The next step is to build a reproducible, point-in-time dataset and test whether news, fundamentals, sector conditions, and search attention improve on transparent baselines for an explicitly defined Indian-equity outcome.")
heading("7.1 Future work",2)
nums(["Confirm title, scope, universe, target, and data sources with the supervisor.","Create a point-in-time data inventory and check licensing/attribution.","Reproduce the earlier research note only if original inputs and scripts are available.","Audit coverage and leakage in the labeled dataset.","Train baseline models and perform chronological validation/calibration.","Add explanations, risk and valuation modules only after approved definitions and tests.","Capture verified screenshots, complete placeholders, and rehearse a limitations-first demonstration."])

heading("REFERENCES")
for ref in [
"Araci, D. (2019). FinBERT: Financial Sentiment Analysis with Pre-trained Language Models. arXiv:1908.10063. https://arxiv.org/abs/1908.10063",
"Da, Z., Engelberg, J., & Gao, P. (2011). In Search of Attention. The Journal of Finance, 66(5), 1461–1499. https://doi.org/10.1111/j.1540-6261.2011.01679.x",
"Lundberg, S. M., & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. NeurIPS 30. https://proceedings.neurips.cc/paper/2017/hash/8a20a8621978632d76c43dfd28b67767-Abstract.html",
"ProsusAI. (n.d.). FinBERT model card. Hugging Face. https://huggingface.co/ProsusAI/finbert",
"scikit-learn developers. (n.d.). Cross-validation user guide. https://scikit-learn.org/stable/modules/cross_validation.html",
"Student-provided local project source. README.md, app.py, src/analytics/growth_labels.py, tests/test_growth_labels.py. Reviewed 22 October 2026; local, non-public source.",
"GL Bajaj Institute of Technology and Management. Project report, PPT, and poster templates supplied by the student."
]:para(ref)
heading("APPENDIX — RUN AND SUBMISSION CHECKLIST")
para("The app runs from its project environment with Streamlit and app.py. Required provider credentials belong in a local .env file and must never appear in screenshots, reports, or shared source. For a viva, demonstrate company search, sentiment summary, article evidence, comparison/export, then explain clearly that integrated growth prediction is not yet available.")
tab(["Item","Complete before final submission"],[
("Identity","Replace student names, roll numbers, group ID, supervisor name/designation."),
("Evidence","Replace/confirm screenshots against the final app."),
("Results","Reproduce numerical research results from source data or remove unsupported values."),
("References","Verify metadata and apply department citation style."),
("Document","Update table of contents and page fields after all edits."),
("Approval","Confirm scope, target, and format with supervisor.")])
doc.core_properties.title="Stock Market Prediction Dashboard: An Explainable Indian Equity Growth Outlook System"
doc.core_properties.subject="B.Tech CSE (AI) project report, academic session 2026–2027"
doc.core_properties.author="[STUDENT NAME(S)]"
path=OUT/"Stock_Market_Prediction_Dashboard_Project_Report.docx";doc.save(path);print(path)

