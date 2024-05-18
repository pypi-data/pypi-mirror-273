import os
import subprocess
from .base_model import AIModel
from .setting import cache_path


from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama as OllamaLC
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


class OllamaLlava(AIModel):
    name = "ollama_llava"
    model = None
    qachain = None
    ollama_process = None

    def __init__(self) -> None:
        super().__init__()

    def clear(self):
        if self.ollama_process:
            self.ollama_process.kill()

    def load_model(self, args):
        subprocess.call(
            f'chmod +x {os.path.join(cache_path, "ollama-darwin")}', shell=True
        )
        self.ollama_process = subprocess.Popen(
            [os.path.join(cache_path, "ollama-darwin") + " serve"],
            shell=True,
            # set env OLLAMA_MODELS=models path
            env={"OLLAMA_MODELS": os.path.join(cache_path, "ollama"), **os.environ},
        )
        self.model = OllamaLC(
            base_url="http://localhost:11434",
            model="llava",
            # callbacks=[StreamingStdOutCallbackHandler()],
        )

    def run_model(self, args):
        _, encoded = args.get("url").split("base64,")
        print(encoded)
        llm_with_image_context = self.model.bind(images=[encoded.strip()])
        return llm_with_image_context.invoke(args.get("query"))


class OllamaMistral(AIModel):
    name = "ollama_mistral"
    model = None
    qachain = None
    ollama_process = None

    def __init__(self) -> None:
        super().__init__()

    def clear(self):
        if self.ollama_process:
            self.ollama_process.kill()

    def load_model(self, args):
        subprocess.call(
            f'chmod +x {os.path.join(cache_path, "ollama-darwin")}', shell=True
        )
        self.ollama_process = subprocess.Popen(
            [os.path.join(cache_path, "ollama-darwin") + " serve"],
            shell=True,
            # set env OLLAMA_MODELS=models path
            env={"OLLAMA_MODELS": os.path.join(cache_path, "ollama"), **os.environ},
        )
        self.model = OllamaLC(
            base_url="http://localhost:11434",
            model="mistral",
            # callbacks=[StreamingStdOutCallbackHandler()],
        )

    def run_model(self, args):
        if args.get("task") == "retrive":
            return self.task_retrieve(args)
        elif args.get("task") == "query":
            return self.task_query(args)
        elif args.get("task") == "chat":
            return self.task_chat(args)

    def task_retrieve(self, args):
        loader = WebBaseLoader(args.get("url"))
        data = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
        all_splits = text_splitter.split_documents(data)
        oembed = OllamaEmbeddings(base_url="http://localhost:11434", model="mistral")
        vectorstore = Chroma.from_documents(documents=all_splits, embedding=oembed)
        self.qachain = RetrievalQA.from_chain_type(
            self.model, retriever=vectorstore.as_retriever()
        )

    def task_query(self, args):
        return self.qachain.run(args.get("query"))

    def task_chat(self, args):
        for chunk in self.model.stream(args.get("user")):
            yield chunk
