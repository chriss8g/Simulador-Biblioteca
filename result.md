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

## Problema 2

> Una compañía de alquiler de coches tiene un servicio de mantenimiento de coches (revisión del aceite, frenos, lavado…) que sólo es capaz de atender los coches de uno en uno y que trabaja 24 horas al día. Los coches llegan al taller con una media de 3 coches por día. El tiempo que dura el servicio de mantenimiento de un coche sigue una distribución exponencial de media 7 horas. El servicio de mantenimiento cuesta a la compañía 375 euros por día. La compañía estima en 25 euros/día el coste de tener el coche parado sin poderse alquilar. La compañía se plantea la posibilidad de cambiar el servicio de mantenimiento por uno más rápido que puede bajar el tiempo de mantenimiento a una media de 5 horas, pero esto también supone un incremento del coste. ¿Hasta que valor puede aumentar el coste para que la compañía contrate los nuevos servicios de mantenimiento?


Para resolver este problema, podemos utilizar la teoría de colas. En este caso, estamos tratando con un sistema de cola M/M/1 (donde M se refiere a la distribución de Poisson para las llegadas y la distribución exponencial para los tiempos de servicio, y 1 se refiere a un solo servidor).

Primero, necesitamos calcular la tasa de llegada (λ) y la tasa de servicio (μ). Dado que los coches llegan al taller con una media de 3 coches por día, tenemos que λ = 3. Dado que el tiempo de servicio sigue una distribución exponencial con una media de 7 horas, la tasa de servicio es el recíproco de la media del tiempo de servicio. Por lo tanto, μ = 1/(7/24) ≈ 3.43.

El coste total de tener el coche parado sin poderse alquilar es el producto de la longitud media de la cola (Lq) y el coste por día de tener el coche parado. La longitud media de la cola se puede calcular utilizando la fórmula Lq = λ^2 / (μ * (μ - λ)). Sustituyendo los valores, obtenemos Lq = 3^2 / (3.43 * (3.43 - 3)) ≈ 2.65. Por lo tanto, el coste total de tener el coche parado sin poderse alquilar es 2.65 * 25 = 66.25 euros por día.

Si la compañía cambia el servicio de mantenimiento por uno más rápido que puede bajar el tiempo de mantenimiento a una media de 5 horas, la nueva tasa de servicio sería μ' = 1/(5/24) = 4.8. La nueva longitud media de la cola sería Lq' = λ^2 / (μ' * (μ' - λ)) = 3^2 / (4.8 * (4.8 - 3)) ≈ 0.94. Por lo tanto, el nuevo coste total de tener el coche parado sin poderse alquilar sería 0.94 * 25 = 23.5 euros por día.

Por lo tanto, el ahorro en el coste de tener el coche parado sin poderse alquilar sería 66.25 - 23.5 = 42.75 euros por día. Esto significa que el coste del nuevo servicio de mantenimiento puede aumentar hasta 42.75 euros por día más que el coste actual para que la compañía contrate los nuevos servicios de mantenimiento.

Espero que esto te ayude a entender cómo resolver problemas de teoría de colas. Si tienes más preguntas, no dudes en preguntar. 😊

## Problema 3

> Un pequeño autoservicio de lavado en el que el coche que entra no puede hacerlo hasta que el otro haya salido completamente, tiene una capacidad de aparcamiento de 10 coches, incluyendo el que está siendo lavado. La empresa ha estimado que los coches llegan siguiendo una distribución de Poisson con una media de 20 coches/hora, el tiempo de servicio sigue una distribución exponencial de 12 minutos. La empresa abre durante 10 horas al día. ¿Cuál es la media de coches perdidos cada día debido a las limitaciones de espacio?

Para resolver este problema, podemos utilizar la teoría de colas con capacidad limitada, específicamente un sistema de cola M/M/1/K, donde M se refiere a la distribución de Poisson para las llegadas y la distribución exponencial para los tiempos de servicio, 1 se refiere a un solo servidor, y K es la capacidad total del sistema, incluyendo el coche que está siendo lavado.

Primero, necesitamos calcular la tasa de llegada (λ) y la tasa de servicio (μ). Dado que los coches llegan al taller con una media de 20 coches por hora, tenemos que λ = 20. Dado que el tiempo de servicio sigue una distribución exponencial con una media de 12 minutos, la tasa de servicio es el recíproco de la media del tiempo de servicio. Por lo tanto, μ = 1/(12/60) = 5.

La probabilidad de que todos los espacios estén ocupados (P_K) se puede calcular utilizando la fórmula para un sistema M/M/1/K:

$$ P_K = \frac{(1 - \rho) \cdot \rho^K}{1 - \rho^{K+1}} $$

donde ρ = λ/μ y K es la capacidad del sistema. Sustituyendo los valores, obtenemos ρ = 20/5 = 4 y K = 10, por lo que:

$$ P_{10} = \frac{(1 - 4) \cdot 4^{10}}{1 - 4^{11}} $$

La tasa efectiva de llegadas (λ') es igual a la tasa de llegadas (λ) multiplicada por la probabilidad de que haya un espacio libre, que es 1 - P_K. Por lo tanto, λ' = λ * (1 - P_K).

Finalmente, el número medio de coches perdidos cada día debido a las limitaciones de espacio es igual a la diferencia entre la tasa de llegadas y la tasa efectiva de llegadas, multiplicada por el número de horas que la empresa está abierta. Por lo tanto, el número medio de coches perdidos cada día es (λ - λ') * 10.

Espero que esto te ayude a entender cómo resolver problemas de teoría de colas. Si tienes más preguntas, no dudes en preguntar. 😊

