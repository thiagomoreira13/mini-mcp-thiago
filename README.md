# Mini MCP Server Tester
│ └── index.html # Simple UI
├── requirements.txt # Dependencies
├── .env.example # Example of env variables (optional)
└── README.md # This file


---


## 🧠 Design Decisions


- Simple Flask app used to unify API + UI
- Frontend uses raw HTML/JS for simplicity
- Experiments stored in memory (would use DB in prod)
- Focused on clarity, rapid iteration, and usability


---


## 🧩 Next Steps (if more time)


- Store experiments in SQLite or file
- Add async concurrency to improve performance
- Add front-end field validation
- Improve error reporting
