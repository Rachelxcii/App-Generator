# 🚀 Data-Driven UI Engine for Pygame

[![Python Version](https://img.shields.io/badge/python-3.14-blue)](https://www.python.org/downloads/)
[![Pygame](https://img.shields.io/badge/pygame-2.6.0+-green)](https://www.pygame.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight, asynchronous UI framework for Pygame that enables dynamic interface generation via JSON-based declarative schemas and decoupled process management.

---

## 🛠 System Architecture

### 1. Declarative Engine (JSON-Based)
The application layout and behavior are defined through a hierarchical JSON schema rather than hardcoded logic.
- **Agility:** Modify layout, styles, or element behaviors (inputs, buttons, images) exclusively in the schema without touching the core engine.
- **Function Injection:** Supports external function registration mapped dynamically. The engine recognizes these through an internal registry, allowing for full extensibility.

### 2. Concurrency Management: The Worker Thread
To prevent heavy processes (statistical calculations, disk/network access) from blocking the main UI thread (60 FPS), this framework implements a concurrency model based on a **FIFO Queue**.

- **Separation of Concerns:** The main thread handles rendering and event capture exclusively, while the **Worker Thread** processes business logic.
- **Race Condition Prevention:** By centralizing external function execution in a single worker thread via a queue, memory access conflicts are eliminated, ensuring a linear and predictable execution flow.
- **True Asynchrony:** Users can continue interacting with the app or queue new tasks while the Worker processes previous ones.

### 3. Flow Control and Data Integrity
The system prioritizes information integrity and user control over the software lifecycle:
- **Graceful Shutdown:** Configurable via JSON, determining if the app should wait for the task queue to empty or interrupt immediately to prevent critical data loss.
- **Panic Button:** Implementation of a configurable "Stop" mechanism that allows users to cancel Worker processes in case of external hang-ups or excessive wait times.

### 4. Modular Components & Composition
The engine uses specialized loaders for each component, maximizing reusability through:
- **Proto-elements:** Composition-based visual elements, allowing buttons and icons to share logic for tinting, rotation, and scaling.
- **Encapsulation:** Each element is responsible for its own parsing and rendering logic.

## 📈 Engineering Value
This framework addresses the historical limitation of Pygame (its single-threaded nature), transforming it into an engine capable of handling complex data-processing applications with a fluid, professional UI.

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.14**
- **Pygame 2.6.1+**

### Installation
```bash
git clone [https://github.com/Rachelxcii/App-Generator.git](https://github.com/Rachelxcii/App-Generator.git)
cd App-Generator
pip install -r requirements.txt
# App-Generator

If you want to attached external assets use the following folders:
- Images path: app-generator/assets/images (Also for icons)
- Fonts path: app-generator/assets/fonts
