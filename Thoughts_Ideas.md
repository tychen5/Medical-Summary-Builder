## Tech Stack reference
* Nebius LLM API (Chat model & embedding model) + 🦜️🔗 LangChain  - https://python.langchain.com/docs/integrations/providers/nebius/
* RAG Vector store: Pinecone + LangChain (https://python.langchain.com/docs/tutorials/rag/ , https://python.langchain.com/docs/tutorials/qa_chat_history/)
* Document loaders: https://python.langchain.com/docs/how_to/document_loader_pdf/ , https://python.langchain.com/docs/integrations/document_loaders/microsoft_word/ , https://python.langchain.com/docs/integrations/document_loaders/ , https://github.com/nsasto/langchain-markitdown
* Secret Manager: .env file

## Ideas
0. 先建立所需要的模組與基礎建設與repo框架

1. Convert input data PDF (Medical File.pdf as the input source data) & DOCX (Medical Summary.docx as the output template format) to markdown.
    * In order to 將source data放入到Pinecone RAG knowledge base中
    * 並讀取最後要輸出的template
    * 還要可以讓使用者輸入prompt instruction來讓使用者可以customize their own tables。這個prompt主要會說明想要輸出的table format每個欄位的說明、想要萃取出來的資料、範例等等。
2. Use react agent ( https://langchain-ai.github.io/langgraph/agents/agents/#2-create-an-agent , https://langchain-ai.github.io/langgraph/reference/agents/#langgraph.prebuilt.chat_agent_executor.create_react_agent ) to fill the template's metadata data(Claimant name, SSN, DOB, AOD, DLI, Age, Education, Alleged impairments, etc.)，可以多次利用pinecone hybrid search from RAG knowledge base (https://python.langchain.com/docs/integrations/retrievers/pinecone_hybrid_search/) as the react agent's tool to search RAG iteratively.
    * 這些背景資料metadata也要往下帶入給判別萃取LLM作為context
3. 一次看PDF的三個頁面(首頁只多看第二頁、末頁只多看前一頁)，判斷中間那一頁的資料是否與使用者所輸入需要的table prompt instruction有相關符合(e.g., 為需要填入表格的Timeline of medical events: Date | Provider | Reason等等)；如果有相干，那就標記好抓出來該頁，如果沒相關就跳過
    * 利用LLM從source data中判別出重要的background context metadata（若資料過大量，接下來可以先進行summary）以及 可以填入表格資訊重要相干頁面 或是這個頁面並不重要不相關
4. 根據所萃取出來標記的每個頁面，將每一段的連續頁碼交給LLM來填入表格(動態依據使用者輸入的prompt 使用者輸入的prompt instructions - customize their own tables prompts。通常這個Prompt template 就會去包含一個instructions prompt 來產生不同需求的表格、規範每個欄位的需求說明以及範例等等)
5. 將表格填完以後可以再依時間排序輸出df，再依照sample report template的格式輸出一個word文件


# Summary
- **Repository scaffolding**: Established a modular Python package under [src/medical_summary_builder/](cci:7://file:///c:/Users/leoqa/Pcloud/Work_Sync/Personal%20Data/SuperInsight_AI%20Engineer_20250901/Medical-Summary-Builder/src/medical_summary_builder:0:0-0:0) with subpackages for ingestion, preprocessing, vectorstore, LLM clients, agents, pipelines, services, reporting, API, CLI, and utilities.  
- **Configuration & dependencies**: Added [requirements.txt](cci:7://file:///c:/Users/leoqa/Pcloud/Work_Sync/Personal%20Data/SuperInsight_AI%20Engineer_20250901/Medical-Summary-Builder/requirements.txt:0:0-0:0) capturing LangChain, LangGraph, Pinecone, FastAPI, Typer, and supporting libraries. Centralized runtime settings in [config.py](cci:7://file:///c:/Users/leoqa/Pcloud/Work_Sync/Personal%20Data/SuperInsight_AI%20Engineer_20250901/Medical-Summary-Builder/src/medical_summary_builder/config.py:0:0-0:0) with environment-variable support.  
- **Documentation**: Replaced [README.md](cci:7://file:///c:/Users/leoqa/Pcloud/Work_Sync/Personal%20Data/SuperInsight_AI%20Engineer_20250901/Medical-Summary-Builder/README.md:0:0-0:0) with a detailed guide covering capabilities, pipeline methodology, directory layout, setup steps, CLI/API usage, and enhancement roadmap.

# Key Artifacts
- **[requirements.txt](cci:7://file:///c:/Users/leoqa/Pcloud/Work_Sync/Personal%20Data/SuperInsight_AI%20Engineer_20250901/Medical-Summary-Builder/requirements.txt:0:0-0:0)** – Declares core dependencies for RAG, agent orchestration, API/CLI interfaces, and testing.  
- **`src/medical_summary_builder/…`** – Comprehensive package skeleton including [pipelines/orchestrator.py](cci:7://file:///c:/Users/leoqa/Pcloud/Work_Sync/Personal%20Data/SuperInsight_AI%20Engineer_20250901/Medical-Summary-Builder/src/medical_summary_builder/pipelines/orchestrator.py:0:0-0:0), [services/summary_builder.py](cci:7://file:///c:/Users/leoqa/Pcloud/Work_Sync/Personal%20Data/SuperInsight_AI%20Engineer_20250901/Medical-Summary-Builder/src/medical_summary_builder/services/summary_builder.py:0:0-0:0), [reporting/report_writer.py](cci:7://file:///c:/Users/leoqa/Pcloud/Work_Sync/Personal%20Data/SuperInsight_AI%20Engineer_20250901/Medical-Summary-Builder/src/medical_summary_builder/reporting/report_writer.py:0:0-0:0), and API/CLI entry points.  
- **[README.md](cci:7://file:///c:/Users/leoqa/Pcloud/Work_Sync/Personal%20Data/SuperInsight_AI%20Engineer_20250901/Medical-Summary-Builder/README.md:0:0-0:0)** – English-language documentation outlining methodology, inputs/outputs, architecture, and execution instructions.

# Next Steps
- **Implement extraction logic**: Flesh out placeholders in [MetadataRouter](cci:2://file:///c:/Users/leoqa/Pcloud/Work_Sync/Personal%20Data/SuperInsight_AI%20Engineer_20250901/Medical-Summary-Builder/src/medical_summary_builder/preprocessing/metadata_router.py:19:0-27:33), [PageRelevanceRanker](cci:2://file:///c:/Users/leoqa/Pcloud/Work_Sync/Personal%20Data/SuperInsight_AI%20Engineer_20250901/Medical-Summary-Builder/src/medical_summary_builder/preprocessing/page_ranker.py:14:0-26:9), and agent workflows to perform real LLM-driven parsing.  
- **Add tests & prompts**: Scaffold a `tests/` directory and populate `prompts/` for reproducible agent behavior.  
- **Integrate evaluation**: Develop verification scripts comparing generated summaries against expected outputs from `Data/Medical File.pdf`.


Cause of bug
Invalid structured output schema: Passing response_format=AgentSummary directly into ChatOpenAI violates OpenAI’s schema requirements (custom_tables lacked a required schema definition). This triggered the BadRequestError when hitting the gpt-5-nano endpoint.
Fixes implemented
AgentSummary
 schema (
src/medical_summary_builder/pipelines/orchestrator.py
): Replaced mutable defaults with Field(default_factory=...) so any JSON schema derived from the model is valid.
Removed response_format usage: Updated 
create_react_agent()
 invocation in 
MedicalSummaryPipeline.run()
 to stop passing response_format=AgentSummary.
Manual parsing fallback: The fallback extractor now asks the LLM to return JSON matching the expected keys and parses the text via 
_parse_json_string()
.