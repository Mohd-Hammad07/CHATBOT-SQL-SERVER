# SQL Server Chatbot Application

## Overview

This repository contains a simple, interactive chatbot application built using Streamlit, LangChain, and SQL Server. The chatbot allows users to interact with a SQL Server database through natural language queries. It translates user questions into SQL queries and retrieves data from the connected SQL Server database.

### Key Features:
- **Database Interaction**: Users can connect to a SQL Server database and execute queries by simply typing their questions.
- **Natural Language Processing**: Powered by LangChain and OpenAI's models, the chatbot converts natural language questions into SQL queries.
- **Streamlit UI**: A user-friendly interface is built using Streamlit, making it easy to interact with the chatbot and the database.

## Installation

### Prerequisites

Before running the application, ensure that you have the following installed:

- **Python 3.8+**
- **SQL Server** (Accessible on your machine or network)
- **ODBC Driver for SQL Server** (Version 17 or higher)

### Clone the Repository

```bash
git clone https://github.com/yourusername/sql-server-chatbot.git
cd sql-server-chatbot
```

### Install Dependencies

Create a virtual environment and install the necessary Python packages:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the root directory of the project and add your OpenAI API key:

```bash
OPENAI_API_KEY=your_openai_api_key
```

### Running the Application

Once the dependencies are installed, you can start the Streamlit application:

```bash
streamlit run app.py
```

### Connecting to SQL Server

1. Open the application in your web browser (Streamlit will provide a URL).
2. In the sidebar, enter your SQL Server details:
   - **Server**: The name of your SQL Server instance (e.g., `Your Server Name `).
   - **Database**: The name of the database you want to connect to (e.g., `Database`).
3. Click the **Connect** button to establish a connection to the database.

## How It Works

### User Interface

- The application features a sidebar where you can configure the database connection settings.
- The main interface displays a chatbox where users can type questions about the database.

### Chatbot Interaction

- Once connected to the SQL Server database, users can ask questions in natural language.
- The chatbot, powered by LangChain and OpenAI's GPT-4 model, interprets the question, generates the corresponding SQL query, and executes it against the connected database.
- The query results are then displayed in the chat interface.

### Example Queries

- **User**: "Show me the top 5 employees by salary."
- **Chatbot**: `SELECT TOP 5 * FROM Employees ORDER BY Salary DESC;`

- **User**: "How many orders were placed in 2023?"
- **Chatbot**: `SELECT COUNT(*) FROM Orders WHERE YEAR(OrderDate) = 2023;`

### Error Handling

If the application encounters any issues connecting to the database, an error message will be displayed in the interface. Ensure that:
- The server name and database name are correct.
- The SQL Server instance is running and accessible.

## Customization

You can customize the chatbot to suit your specific needs:
- **Model**: Change the OpenAI model in the `get_sql_chain` function if required.
- **Database Schema**: Modify the prompt template to include more or less schema information.
- **User Interface**: Use Streamlit’s rich features to add more interactivity or style the UI to your preference.

## Troubleshooting

- **Connection Issues**: Ensure that your SQL Server allows remote connections and that the firewall settings are correctly configured.
- **ODBC Driver**: Make sure the correct ODBC driver is installed on your system. You can check this using the ODBC Data Source Administrator on Windows.

## Contribution

Contributions to improve this project are welcome. Feel free to open issues or submit pull requests.

### License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgments

This application was built using the following technologies:
- **[Streamlit](https://streamlit.io/)**: For building the web application interface.
- **[LangChain](https://langchain.com/)**: For natural language processing and SQL query generation.
- **[OpenAI API](https://openai.com/)**: For powering the chatbot's conversational abilities.
- **[SQL Server](https://www.microsoft.com/en-us/sql-server)**: As the database management system.


