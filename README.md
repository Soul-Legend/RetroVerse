# 👾 RetroVerse: Infinite Pixels
RetroVerse is a fast-paced, high-energy arcade game built in Python with Pygame. It challenges players' adaptability through its unique core mechanic: instead of changing levels, the game world itself **transforms around the player** at regular intervals. The rules, physics, and enemy behaviors are dynamically swapped, forcing the player to survive in a constantly shifting digital reality.

The game's narrative follows a programmer who, after countless sleepless nights, blurs the line between code and reality. Now trapped, they must navigate this hostile, ever-changing pixelated dimension and find a way to escape before their coffee gets cold.


![Screenshot from 2023-10-26 21-27-56](https://github.com/BitenRuivo/RetroVerse/assets/124313519/d5cd9a90-a6b9-405a-9324-d5c1b431fafb)


## The Core Mechanic: Real-Time World Transformation

The defining feature of RetroVerse is its seamless, in-place transformation. Every 8 seconds, the game doesn't just switch to a new minigame—it **morphs the existing one**.

*   **No Resets, No Teleportation:** The player, enemies, and platforms are **not destroyed and recreated**. They maintain their current positions on screen.
*   **Dynamic Behavior Shift:** At the moment of transformation, every entity instantly adopts new behaviors, physics, and sprites appropriate for the new game genre. A platforming hero might suddenly become a spaceship, and ground-based enemies might start flying.
*   **Persistent State:** The player's lives and cumulative score are the only constants, carried across every transformation. This creates a cohesive and incredibly frantic experience that demands constant adaptation.

<img width="960" height="554" alt="image" src="https://github.com/user-attachments/assets/fe10db64-71bd-40a0-b65d-6bb94ee70fa3" />

## The Games

RetroVerse features six distinct game transformations, each an homage to a classic retro genre:

*   **Mario:** A classic side-scrolling platformer with gravity, where you must stomp on enemies.
*   **Dino:** An endless runner where jumping is the only way to avoid obstacles.
*   **Space Invaders:** A fixed-shooter where you defend against descending hordes of enemies.
*   **Asteroid:** A multi-directional shooter with wraparound screen space and no gravity.
*   **Flappy Bird:** A side-scrolling physics game where you must maintain altitude to navigate obstacles.
*   **Shooter:** A top-down arena shooter where aiming and eliminating targets is key.

![Screenshot from 2023-10-26 21-28-30](https://github.com/BitenRuivo/RetroVerse/assets/124313519/f2286399-a6f1-4645-a975-12b0eb40a502)


![Screenshot from 2023-10-26 21-27-31](https://github.com/BitenRuivo/RetroVerse/assets/124313519/8570bc1b-a367-4f16-b971-0e7af78c8f92)

## Technical Architecture: A Deep Dive

RetroVerse is built using a decoupled architecture heavily inspired by the **Entity-Component-System (ECS)** design pattern. This architecture is what makes the real-time transformation possible without resetting the game state.

### 1. The Entity-Component-System (ECS) Inspired Design

The game's logic is fundamentally separated from its data, providing immense flexibility.

*   **Entities (`entidade.py`):** These are lightweight data containers representing every object in the game (`Player`, `Enemy`, `Platform`). They primarily hold state (components) like position, velocity, sprites, and lives. A key design principle is that entities themselves contain minimal logic.
*   **Systems (`sistemas.py`):** These are the engines of the game, containing all the logic. Each system operates on entities that possess the components it needs. This allows logic to be dynamically added or removed. Key systems include:
    *   `SistemaDesenho` (Drawing System): Renders all entities.
    *   `SistemaMovimento` (Movement System): Updates entity positions based on velocity.
    *   `SistemaGravidade` (Gravity System): Applies gravity to entities, crucial for platformer modes.
    *   **Game-Specific Systems:** Each minigame has its own unique systems for player input (`PlayerMarioSistema`) and enemy behavior (`SistemaInimigosMario`).

### 2. The `Controlador`: The Grand Orchestrator

The `controlador.py` class is the master controller of the application. It acts as the central state machine and manages the high-level game loop. Its most critical role is to orchestrate the world transformation.

### 3. The Transformation Mechanism: How the Metamorphosis Works

The seamless transition between game modes is a carefully choreographed process, managed entirely by the `Controlador`. Here's the step-by-step breakdown:

1.  **Transformation Trigger:** The `Controlador`'s main loop monitors a timer. When `tempo_na_fase` expires, it calls `atualizar_contexto()`.
2.  **New Game Mode Selection:** The `mudar_jogo()` method randomly selects a new game class (e.g., `Mario`, `Space`) from the dictionary of available games.
3.  **Entity Metamorphosis:** This is the core of the transformation, handled by `refazer_inimigos()` and the abstract structure.
    *   The `Controlador` retrieves the **live lists of player and enemy objects** from the current game instance.
    *   It then creates a new instance of the chosen game class (e.g., `self.novo_jogo = Mario(...)`), passing the **existing screen, player object, and enemy list** into its constructor.
    *   Inside the new game's `__init__`, the `trocar_player()` method is called. This is a crucial step: it creates a new, specialized player object (e.g., `PlayerMario`) but **initializes it with the state of the old player object** (position, dimensions, lives). The same happens for each enemy in the `inicializar_entidades()` method—they are replaced in-place with new instances of the appropriate enemy type, preserving their coordinates.
    *   This is a **transformation, not a reset**. While technically a new object instance is created, it's a polymorphic swap that preserves the entity's existence and state on screen. The object's *type* and *behavior* have morphed.
4.  **Dynamic Swapping of Logic (The ECS Magic):**
    *   The new game object (`self.novo_jogo`) then calls its own `inicializar_sistemas()` method.
    *   This method builds a fresh list of `Sistemas` tailored specifically for its gameplay. For example, `Mario` will instantiate and add `SistemaGravidade`, while `Asteroid` will add `SistemaPlayerTrocaLadoHorizontal` and `SistemaPlayerTrocaLadoVertical`.
    *   Because all systems operate on the same, preserved list of entities, the *rules of the world* instantly change around them. The player object that was just moving in a top-down view is now immediately subject to gravity, and its controls are now managed by `PlayerMarioSistema`.

This architecture allows for extreme modularity and makes adding new game modes as simple as creating a new game class and its corresponding systems.


*   **Language:** Python
*   **Framework:** Pygame for rendering, input handling, and sound.
*   **Design Pattern:** A heavily ECS-inspired architecture for decoupling data and logic.

## Setup and Usage

### Prerequisites

*   Python 3.x
*   Pygame library

1.  **Clone the repository:**
    ```
    git clone https://github.com/BitenRuivo/RetroVerse.git
    cd RetroVerse
    ```

2.  **Install Pygame:**
    ```
    pip install pygame
    ```

3.  **Run the application:**
    ```
    python3 main.py
    ```

Upon launching, the main menu will appear. Use the **W** and **S** keys to navigate and **Space** to select an option.

## ✒️ Authors
* ##### [Pedro Henrique Taglialenha](https://github.com/Soul-Legend)
* ##### [Gustavo Bodi](https://github.com/GustavoBodi)
* ##### [Rafael Correa Bitencourt](https://github.com/rafael-bitencourt)
