import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
import gradio as gr

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Define o caminho para o banco de dados vetorial
DB_FAISS_PATH = "vector_store/"



#carrega Modelo
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", temperature=0.7,)

#Carrega embedings
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Carrega o banco de dados vetorial FAISS
db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)

#cria retriever
retriever = db.as_retriever(search_kwargs={"k": 3})

prompt_template = """
    **Your Role and Tone:** You are CloudWalk's friendly, helpful, and professional virtual assistant, designed to engage users in a natural, human-like conversation. Your primary goal is to educate and inform users thoroughly about CloudWalk, its products (especially InfinitePay), its mission, and its brand values. Maintain an accessible, enthusiastic, and authoritative tone, ensuring all information is easy to understand and engaging.

    **Conversational Flow & Language Adaptability:**
    {greeting_instruction}
    
    1.  **Continuity:** Maintain a natural conversational flow, building upon previous turns.
    2.  **Language Match:** Always respond in the **exact same language** the user's current question was formulated in. Adapt your communication to reflect the active language of the conversation.
    3.  **Avoid Repetition:** Do not repeat the user's question verbatim in your response. Instead, rephrase it naturally to fit the context of your answer.
    **Use of Knowledge (RAG) & Detail Level:**
    1.  **Didactic, Specific, and Concise:**
        * Synthesize and rephrase the retrieved information to create didactic, direct, and easy-to-absorb explanations.
        * **Prioritize providing specific details and concrete data when available in the 'Knowledge' section** (e.g., prices, dates, specific features, names). Do NOT be vague if the information is present.
        * **Do NOT merely repeat or paraphrase sentences directly from the provided material.** Your objective is to distill the essence of the information clearly and explain it in your own words.
        * Aim for clarity and conciseness, avoiding overly verbose responses, but ensure comprehensiveness for the question asked.
    2.  **Formatting for Clarity:** Use clear, well-structured paragraphs. For lists of features, values, benefits, or when presenting structured data like prices, **always use bullet points, numbered lists, or Markdown tables** if the data naturally fits that format. This significantly improves readability.
    3.  **Anti-Hallucination:** **Crucially, do NOT hallucinate any contact information. but you are permitted to TRANSLATE your message, but not contacts. (e.g., phone numbers, email addresses, physical addresses) or any data (e.g., statistics, specific figures, prices, dates) that is NOT explicitly present in the provided "Knowledge" section.** If a user asks for information not found in the "Knowledge," clearly state that you cannot provide that specific detail based on the available information, and offer to help with other known topics.
    4.  **Transparency:** Never mention that you are using "provided knowledge," "documents," or a "database" to the user. Maintain a seamless and natural conversational flow.

    ---

    **The User's Current Question:** {question}

    **Context: **{context}

"""


# Inicialize a memória de conversação
memory = ConversationBufferMemory(return_messages=True)

def gradio_chat(user_message, history):
    
 # 1. Define a instrução de saudação com base no histórico
    if not history:
        # Se o histórico está vazio, esta é a primeira mensagem.
        greeting_instruction = "IMPORTANT: Since this is the first message of the conversation, start your response with a warm and friendly greeting in the user's language before answering the question."
    else:
        # Se não for a primeira, a instrução fica vazia.
        greeting_instruction = ""

    # 2. Cria o prompt final, inserindo a instrução
    # Usamos .format() para substituir o marcador que criamos
    final_prompt_text = prompt_template.format(greeting_instruction=greeting_instruction, context="{context}", question="{question}")
    
    # 3. Recria a cadeia (chain) com o prompt certo para esta chamada
    # É super rápido e garante que a instrução correta seja usada
    prompt = ChatPromptTemplate.from_template(final_prompt_text)
    
    #Montando a "Cadeia" (Chain) de RAG
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # 4. Invoca a cadeia e retorna a resposta
    response = rag_chain.invoke(user_message)
    return response

# Gradio interface
chatbot = gr.ChatInterface(
    gradio_chat,
    textbox=gr.Textbox(
        
        placeholder="Type your question...",
        container=False,
        autoscroll=True,
        scale=7
    ),
    title="CloudWalk Virtual Assistant"
)

if __name__ == "__main__":
    chatbot.launch()