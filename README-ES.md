🚀 Data-Driven UI Engine for Pygame
Este framework permite la generación de interfaces de usuario dinámicas y asíncronas en Pygame mediante una arquitectura orientada a datos (JSON) y una gestión de procesos desacoplada.
🛠 Arquitectura del Sistema
1. Motor Declarativo (JSON-Based)
La aplicación no se define mediante código "hardcoded", sino a través de un esquema JSON jerárquico por pantallas y elementos.
Agilidad: Cambios en la disposición, estilo o comportamiento de los elementos (inputs, botones, imágenes) se realizan exclusivamente en el esquema, sin alterar el núcleo del motor.
Inyección de Funciones: El sistema permite registrar funciones externas que son mapeadas dinámicamente. El motor las reconoce mediante un registro interno, permitiendo una extensibilidad total.
2. Gestión de Concurrencia: El Hilo "Obrero" (Worker Thread)
Para evitar que procesos pesados (cálculos estadísticos, acceso a disco o red) bloqueen el hilo principal de la UI (60 FPS), implementé un modelo de concurrencia basado en una FIFO Queue.
Aislamiento de Responsabilidades: El hilo principal se encarga exclusivamente del renderizado y la captura de eventos, mientras que el Worker Thread procesa la lógica de negocio.
Prevención de Race Conditions: Al centralizar la ejecución de funciones externas en un único hilo obrero a través de una cola, eliminamos conflictos de acceso a memoria y garantizamos un flujo de ejecución lineal y predecible.
Asincronía Real: Puedes seguir interactuando con la app o encolar nuevas tareas mientras el Worker procesa las anteriores.
3. Control de Flujo y Seguridad de Datos
El sistema prioriza la integridad de la información y el control del usuario sobre el ciclo de vida del software:
Cierre Seguro (Graceful Shutdown): Configurable vía JSON, el sistema permite determinar si el cierre de la aplicación debe esperar a que la cola de tareas se vacíe por completo o interrumpirse, evitando pérdidas de datos críticos.
Mecanismo de Interrupción (Panic Button): Implementación de un "Botón Stop" configurable que permite al usuario cancelar procesos del Worker en caso de bloqueos externos o tiempos de espera excesivos.
4. Componentes Modulares y Composición
El motor utiliza un sistema de cargadores específicos por componente, maximizando la reutilización mediante:
Clases Genéricas (Proto-elements): Uso de composición para elementos visuales, permitiendo que botones e iconos compartan la misma lógica de tintado, rotación y escalado.
Encapsulamiento: Cada elemento es responsable de su propio parsing y renderizado.
📈 Valor Ingenieril
Este framework resuelve el limitante histórico de Pygame (su naturaleza single-thread) transformándolo en un motor capaz de manejar aplicaciones de procesamiento de datos complejas con una UI fluida y profesional.