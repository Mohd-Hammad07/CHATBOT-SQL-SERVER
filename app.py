#import all necessary libraries 


# Function to initialize the SQL Server database connection
# Function to initialize the SQL Server database connection
def init_database(server: str, database: str) -> SQLDatabase:
    conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
    return SQLDatabase.from_uri(f"mssql+pyodbc:///?odbc_connect={conn_str}")

# Function to get the SQL chain
def get_sql_chain(db):
    template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.
    
    <SCHEMA>{schema}</SCHEMA>
    
    Conversation History: {chat_history}
    
    Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.
    
    For example:
    Question: which 3 artists have the most tracks?
    SQL Query: SELECT TOP 3 ArtistId, COUNT(*) as track_count FROM Track GROUP BY ArtistId ORDER BY track_count DESC;
    Question: Name 10 artists
    SQL Query: SELECT TOP 10 Name FROM Artist;
    Question: Name 6 artist with most tracks
    SQL Query: SELECT TOP 6 a.Name, COUNT(t.TrackId) as track_count FROM Artist a 
            JOIN Album al ON a.ArtistId = al.ArtistId 
            JOIN Track t ON al.AlbumId = t.AlbumId 
            GROUP BY a.Name 
            ORDER BY track_count DESC;
            
    
    Your turn:

    Question: {question}
    SQL Query:
    """
    
    prompt = PromptTemplate.from_template(template)
  
    # Initialize the LLM once
    llm = ChatGroq(model="..............", temperature=0)
  
    def get_schema(_):
        return db.get_table_info()
  
    return (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | llm
        | StrOutputParser()
    )

# Function to get the natural language response
def get_response(user_query: str, db: SQLDatabase, chat_history: list):
    sql_chain = get_sql_chain(db)
  
    template = """
    You are a data analyst who answers user questions about the company's database based on SQL queries and responses.
    Your task is to provide a clear and direct answer to the user's question using the SQL response. Format the answer as a list with each item on a new line, without any additional text or formatting.
    
    1. **Introduction**: Clearly state the number of items (e.g., "The top 3 artists with the most tracks are:")
    2. **List**: Format each item on a new line with proper indentation, including relevant details from the SQL response.
    Here is the information you have:

    - **Conversation History**: {chat_history}
    - **SQL Query**: <SQL>{query}</SQL>
    - **User Question**: {question}
    - **SQL Response**: {response}

    Provide the answer formatted as a list with each item on a new line.
    """""
  
    prompt = PromptTemplate.from_template(template)
  
    # Use the LLM initialized once
    llm = ChatGroq(model="........", temperature=0)
  
    chain = (
        RunnablePassthrough.assign(query=sql_chain).assign(
            schema=lambda _: db.get_table_info(),
            response=lambda vars: db.run(vars["query"]),
        )
        | prompt
        | llm
        | StrOutputParser()
    )
  
    return chain.invoke({
        "question": user_query,
        "chat_history": chat_history,
    })

# Initialize chat history and database connection in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello! I'm a SQL assistant. Ask me anything about your database."),
    ]

if "db" not in st.session_state:
    st.session_state.db = None  # Initialize with None

load_dotenv()

st.set_page_config(page_title="Chat with SQL Server", page_icon=":speech_balloon:")

st.title("Chat with SQL Server")

with st.sidebar:
    st.subheader("Settings")
    st.write("This is a simple chat application using SQL Server. Connect to the database and start chatting.")
    
    st.text_input("Server", value="Server name ", key="Server")
    st.text_input("Database", value="Database", key="Database")
    
    if st.button("Connect"):
        with st.spinner("Connecting to database..."):
            db = init_database(
                st.session_state["Server"],
                st.session_state["Database"]
            )
            st.session_state.db = db
            st.session_state.server = st.session_state["Server"]  # Save the server name
            st.session_state.database = st.session_state["Database"]  # Save the database name
            st.success("Connected to database!")
    

# Display chat history
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)

# Handle user input and response
user_query = st.chat_input("Type a message...")
if user_query is not None and user_query.strip() != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    
    with st.chat_message("Human"):
        st.markdown(user_query)
        
    if st.session_state.db is not None:  # Check if db is initialized
        with st.chat_message("AI"):
            response = get_response(user_query, st.session_state.db, st.session_state.chat_history)
            st.markdown(response)
        
        st.session_state.chat_history.append(AIMessage(content=response))
    else:
        st.error("Please connect to the database first.")
