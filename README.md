# ai_agent_coder

Experimental tool for using ai-agents for coding. Initially focusing on Machine Learning related problems.

### Core Idea

Division into smaller complexity tasks:

- Planner:
    - ask for architecture sugestions with classes and their main relationship;
    - return, in json format, a dictionary of modules to implement and a description of each;
    - parser with retry;
    - reflection agent to validate answer generation;

- Coder:
    - ask for module implementation;
    - give user context and general architecture structure;
    - give the module name and implementation details;
    - add a "if __name__ == '__MAIN__'" for a small validation execution;
    - add a print of Success by the end of the __main__ statement;
    - parser with retry;

- CodeFixer:
    - run the __main__ of each module;
    - subprocess call should return 0 if succeed, if different than 0, call CodeFixer;
    - run the main script and check for errors;

- Code Fine-tuning:
    - unit tests;
    - addition of RAG;


Maybe add:
- Wikipedia based RAG;
- search for other forms of RAG;
