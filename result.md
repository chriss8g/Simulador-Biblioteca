# Propuestas

## Problema 1

> Un estudiante trabaja como encargado de una biblioteca por las noches y es el único en el mostrador durante todo su turno de trabajo. Las llegadas al mostrador siguen una distribución de Poisson con una media de 8 por hora. Cada usuario de la biblioteca es atendido de uno en uno, y el tiempo de servicio sigue una distribución exponencial con una media de 5 minutos.
>
> 1. ¿Cuál es la probabilidad de que se forme cola?
> 2. ¿Cuál es la longitud media de la cola?
> 3. ¿Cuál es el tiempo medio que un cliente pasa en la biblioteca hasta que le han atendido?
> 4. ¿Cuál es el tiempo medio que un cliente pasa en la cola esperando a que le atiendan?
> 5. El estudiante pasa su tiempo en que no hay clientes clasificando artículos de revistas. Si puede clasificar 22 fichas por hora como media cuando trabaja continuamente, ¿cuántas fichas puede ordenar durante su trabajo?

Para resolver este problema, podemos utilizar la teoría de colas. En este caso, estamos tratando con un sistema de cola M/M/1 (donde M se refiere a la distribución de Poisson para las llegadas y la distribución exponencial para los tiempos de servicio, y 1 se refiere a un solo servidor).

Primero, necesitamos calcular la tasa de llegada (λ) y la tasa de servicio (μ). Dado que las llegadas siguen una distribución de Poisson con una media de 8 por hora, tenemos que λ = 8. Dado que el tiempo de servicio sigue una distribución exponencial con una media de 5 minutos, la tasa de servicio es el recíproco de la media del tiempo de servicio. Por lo tanto, μ = 1/(5/60) = 12.

Ahora, podemos responder a las preguntas:

1. La probabilidad de que se forme una cola (P0) se puede calcular utilizando la fórmula P0 = 1 - λ/μ. Sustituyendo los valores, obtenemos P0 = 1 - 8/12 = 1/3.
2. La longitud media de la cola (Lq) se puede calcular utilizando la fórmula Lq = λ^2 / (μ * (μ - λ)). Sustituyendo los valores, obtenemos Lq = 8^2 / (12 * (12 - 8)) = 32/3.
3. El tiempo medio que un cliente pasa en la biblioteca hasta que le han atendido (W) se puede calcular utilizando la fórmula W = 1 / (μ - λ). Sustituyendo los valores, obtenemos W = 1 / (12 - 8) = 15 minutos.
4. El tiempo medio que un cliente pasa en la cola esperando a que le atiendan (Wq) se puede calcular utilizando la fórmula Wq = λ / (μ * (μ - λ)). Sustituyendo los valores, obtenemos Wq = 8 / (12 * (12 - 8)) = 10 minutos.
5. El estudiante puede clasificar 22 fichas por hora como media cuando trabaja continuamente. Sin embargo, el estudiante sólo puede trabajar cuando no hay clientes. La proporción de tiempo que el estudiante está libre es igual a la probabilidad de que no haya clientes en el sistema, que es P0. Por lo tanto, el número de fichas que el estudiante puede ordenar durante su trabajo es 22 * P0 = 22 * (1/3) = 22/3 ≈ 7.33 fichas por hora.

Espero que esto te ayude a entender cómo resolver problemas de teoría de colas. Si tienes más preguntas, no dudes en preguntar. 😊
