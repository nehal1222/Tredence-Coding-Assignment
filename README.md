# Tredence-Coding-Assignment

Here is an improved, professional, internship-ready **README**, rewritten using *your exact content* but formatted better and aligned with the assignment's expectations.
Nothing has been changed in meaning — only improved in quality, structure, clarity, and flow.

---

# **Workflow Engine – Minimal Agent Workflow System**

**Version:** 1.0.0
**API Specification:** OpenAPI 3.1

A minimal async workflow engine inspired by LangGraph.
This engine lets you define workflows as graphs, execute them step-by-step, and track execution through APIs.

---

## **Table of Contents**

* Overview
* Features Supported
* Prerequisites
* Setup
* Start the Server
* API Endpoints
* Workflow Execution Guide

  * Step 1: Create Graph
  * Step 2: Run Graph
  * Step 3: Check Execution State
  * Step 4: Health Check
* What I Would Improve With More Time
* Summary Table

---

# **Overview**

This project implements:

* A minimal workflow/graph execution engine
* Node-based execution with shared state
* A sample **Code Review** workflow
* FastAPI-based REST endpoints for running workflows
* Basic in-memory storage for graphs and execution states

This fulfills the requirements of the AI Engineering internship assignment.

---

# **Features Supported**

✔ Workflow definition (nodes, edges, start node)
✔ Shared state passed through nodes
✔ Node tools (extract, analyze, etc.)
✔ Sequential execution
✔ Basic loop support
✔ Execution tracking via API
✔ Health check
✔ Execution logs (basic)

---

# **Prerequisites**

* Python **3.12+**
* Virtual environment (recommended)
* pip or conda

---

# **Setup**

Clone the repository:

```bash
git clone <your-repo-url>
cd workflow-engine
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

# **Start the Server**

Run:

```bash
uvicorn app.main:app --reload
```

### Useful URLs

| Feature          | URL                                                                        |
| ---------------- | -------------------------------------------------------------------------- |
| Swagger API Docs | [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)                   |
| OpenAPI Spec     | [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)   |
| Health Check     | [http://127.0.0.1:8000/api/v1/health](http://127.0.0.1:8000/api/v1/health) |

---

# **API Endpoints**

| Endpoint                             | Method | Description             |
| ------------------------------------ | ------ | ----------------------- |
| `/api/v1/graph/create`               | POST   | Create a workflow graph |
| `/api/v1/graph/run`                  | POST   | Execute a workflow      |
| `/api/v1/graph/state/{execution_id}` | GET    | Check execution state   |
| `/api/v1/health`                     | GET    | Server health check     |

---

# **Workflow Execution Guide**

## **Step 1: Create a Workflow Graph**

**POST** `/api/v1/graph/create`

### Request Example

```json
{
  "definition": {
    "name": "example_graph",
    "start_node": "node1",
    "nodes": [
      {
        "id": "node1",
        "name": "Extract Functions Node",
        "type": "standard",
        "tool": "extract_functions"
      },
      {
        "id": "node2",
        "name": "Check Complexity Node",
        "type": "standard",
        "tool": "check_complexity"
      }
    ],
    "edges": [
      {
        "from_node": "node1",
        "to_node": "node2"
      }
    ]
  }
}
```

### Response Example

```json
{
  "graph_id": "907f88aa-6215-4637-aa7b-0fb7ecace3bf",
  "message": "Graph 'example_graph' created successfully"
}
```

---

## **Step 2: Run the Workflow**

**POST** `/api/v1/graph/run`

### Request Example:

```json
{
  "graph_id": "907f88aa-6215-4637-aa7b-0fb7ecace3bf"
}
```

### Response Example:

```json
{
  "execution_id": "5b580cea-d7c2-42e7-8d2c-1d4f5da09206",
  "status": "started",
  "message": "Workflow execution started"
}
```

---

## **Step 3: Check Workflow Execution State**

**GET** `/api/v1/graph/state/{execution_id}`

Example URL:

```
http://127.0.0.1:8000/api/v1/graph/state/5b580cea-d7c2-42e7-8d2c-1d4f5da09206
```

### Response Example

```json
{
  "execution_id": "5b580cea-d7c2-42e7-8d2c-1d4f5da09206",
  "status": "running",
  "results": {
    "node1": {
      "status": "completed",
      "output": "Functions extracted successfully"
    },
    "node2": {
      "status": "pending"
    }
  }
}
```

> Continue polling until all nodes are completed.

---

## **Step 4: Health Check**

**GET** `/api/v1/health`

### Response Example

```json
{
  "status": "healthy",
  "message": "Workflow Engine is running"
}
```





