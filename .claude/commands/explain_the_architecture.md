### Explain the Software Architecture

To better understand the system's architecture from different angles, generate a series of `C4 model diagrams` using `Mermaid syntax`.

> The C4 model offers four zoom levels — from business context down to code — making it easier to communicate software architecture clearly.

Generate one diagram per level, with each diagram answering a specific architectural question.
Create those diagrams inside a `C4.md` file.

### Context Diagram — Where does this system fit in the world?

- Shows the system as a black box.
- Highlights how users and external systems interact with it.
- Answers: Who uses this system and why?

### Container Diagram — What are the main building blocks?

- Zooms into the system to show its major runtime units (e.g., web app, API, DB).
- Shows how containers communicate.
- Answers: How is the system deployed and what are its responsibilities?

### Component Diagram — What lives inside each container?

- Zooms into one container (usually the backend).
- Shows modules, services, controllers, and how they interact.
- Answers: What are the main responsibilities inside this container?

### Code Diagram — What's under the hood?

- Zooms into one component to show classes, methods, or files.
- Useful for reviewing structure, naming, and dependencies.
- Answers: How is this component implemented?
