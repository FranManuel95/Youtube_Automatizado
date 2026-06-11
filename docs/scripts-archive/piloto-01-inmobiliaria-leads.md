# Guion piloto 01 — Canal "Automatización IA para negocios"

- **Nicho**: automatizacion_ia_inmobiliaria
- **Formato**: faceless (voz IA Eleven v3 + screencast + motion graphics)
- **Duración objetivo**: ~11-12 min
- **Lead magnet**: plantilla n8n gratis (workflow básico) → email list
- **Producto**: "Kit Inmobiliaria IA" €49-97
- **Afiliados**: Make, n8n, GoHighLevel (recurrentes)

**Título**: El agente de IA que responde TODOS los leads de una inmobiliaria en 30 segundos (plantilla n8n GRATIS)

**Títulos A/B alternativos**:
1. Construí un agente de IA que cierra visitas inmobiliarias mientras duermes (n8n, sin código)
2. Tu inmobiliaria responde tarde a los leads. La IA lo hace en segundos (n8n, sin código)
3. El sistema de captación con IA que las agencias venden por 2.000€ (te lo monto gratis)

---

## [HOOK · 0-20s]

> [PANTALLA: dashboard de n8n con un workflow ya montado, ejecutándose en vivo. Mensaje de WhatsApp entrando → respuesta automática en 3 segundos.]

Según el National Association of Realtors, alrededor de 7 de cada 10 compradores entrevistan a un solo agente antes de decidir. Lee eso otra vez: la mayoría no compara. Se queda con el primero que les da una buena primera impresión. Y la mayoría de las agencias tardan horas en contestar un lead, cuando ya es tarde. En este video vas a ver, paso a paso y en pantalla, cómo montar un agente de inteligencia artificial que responde a cada cliente en segundos, califica si es serio, y agenda la visita solo. Sin escribir una sola línea de código. Quédate, porque al final te dejo la plantilla para que lo copies hoy mismo.

---

## [SECCIÓN 1 · El problema que cuesta dinero · 1.5 min]

> [PANTALLA: gráfico simple de "tiempo de respuesta vs probabilidad de cierre", caída pronunciada.]

Vamos a poner números sobre la mesa, porque esto no es teoría. Cuando alguien rellena un formulario en un portal inmobiliario, no está mirando solo tu anuncio. Está rellenando el de cinco agencias a la vez. El reloj empieza a correr en ese segundo.

Y los datos sobre velocidad de respuesta son demoledores. Un estudio de Harvard Business Review que analizó un millón y cuarto de leads encontró que contactar en la primera hora multiplica por casi siete la probabilidad de cualificar ese lead, frente a esperar solo una o dos horas más. Y la investigación del MIT lo lleva más lejos: responder en cinco minutos en lugar de treinta multiplica por veintiuno esa probabilidad. Veintiuno. Si tardas hasta el día siguiente, ese lead está prácticamente muerto.

El problema es que un agente inmobiliario humano no puede estar disponible 24 horas. Duerme, conduce, está en visitas, es fin de semana. Y los leads no entienden de horarios: una buena parte de las consultas llega por la tarde-noche y los fines de semana, justo cuando la oficina está cerrada.

Aquí es donde entra la automatización. No para reemplazar al agente —eso es lo que vende humo— sino para hacer la primera respuesta, calificar al lead y reservar la visita, de modo que el humano solo dedique su tiempo a los clientes que de verdad van a comprar.

---

## [SECCIÓN 2 · La arquitectura del sistema · 2 min]

> [PANTALLA: diagrama de bloques dibujado en pantalla: Formulario/WhatsApp → n8n → IA (clasifica) → Calendario + CRM + Notificación.]

Antes de tocar nada, entendamos las piezas. Esto es lo bonito de la automatización moderna: son bloques que encajan, no programación.

**Pieza uno: la entrada.** El lead llega por un sitio: un formulario de la web, un mensaje de WhatsApp, o un anuncio de un portal. Esto es el disparador.

**Pieza dos: el cerebro, que es n8n.** n8n es una herramienta de automatización visual. Piensa en ella como un tablero donde conectas cajas con flechas. Cada caja hace una acción. Es gratuita si la instalas tú mismo, y según su documentación oficial —que te enlazo en la descripción— soporta más de 400 integraciones. No vas a programar: vas a arrastrar y conectar.

**Pieza tres: la inteligencia.** Conectamos n8n a un modelo de IA —Claude o GPT— que lee el mensaje del cliente, entiende qué busca, y redacta una respuesta natural. No un robot frío que dice "su consulta es importante". Una respuesta que parece de una persona del equipo.

**Pieza cuatro: las acciones.** La IA decide: si el lead es serio, le ofrece horarios de visita y los reserva en el calendario. Si tiene dudas, las responde. Y en todos los casos, registra el contacto en el CRM y avisa al agente humano.

Cuatro piezas. Ninguna requiere saber programar. Vamos a montarlas en pantalla.

---

## [SECCIÓN 3 · Montaje paso a paso (el core) · 4.5 min]

> [PANTALLA: workflow COMPLETO ya montado en n8n. Recorrido con zoom por cada pieza — formato showcase: no se construye en vivo, se muestra el sistema terminado por dentro.]

Este es el sistema completo, funcionando, dentro de n8n. Ocho cajas conectadas. Vamos a recorrerlo pieza por pieza para que entiendas exactamente qué hace cada una — y al final te lo llevas tal cual está, como plantilla.

**Pieza uno: la puerta de entrada.** [PANTALLA: zoom al nodo Webhook.] Este primer nodo es un Webhook: una dirección única a la que tu formulario web o tu WhatsApp envían el mensaje del cliente en el momento en que lo escribe. No hay que programar nada: n8n te da la dirección y la pegas en tu formulario.

**Pieza dos: el cerebro.** [PANTALLA: abrir el nodo de IA y mostrar el campo de instrucciones.] Aquí está la magia de verdad. Este nodo conecta con el modelo de inteligencia artificial, y lo importante no es la conexión — es lo que le decimos. Mira las instrucciones que tiene escritas:

"Eres el asistente de una inmobiliaria. Cuando llegue un mensaje de un posible cliente, responde de forma cálida y profesional en español. Identifica: qué tipo de inmueble busca, su presupuesto, y su zona. Si da esos tres datos, ofrécele tres horarios para una visita. Si falta información, pregúntala con amabilidad. Nunca inventes propiedades que no existen."

Fíjate en la última frase, porque es la diferencia entre un sistema serio y un chatbot malo: le prohibimos a la IA inventar. Sin esa instrucción, el problema número uno de estos agentes es que se inventan pisos que no existen.

**Pieza tres: el cruce de caminos.** [PANTALLA: zoom al nodo Switch y sus dos ramas.] Este nodo decide: si la IA marcó el lead como "calificado" —tiene tipo, presupuesto y zona— va por la rama de arriba. Si falta información, va por la de abajo y simplemente le pregunta al cliente lo que falta.

**Pieza cuatro: las acciones.** [PANTALLA: zoom a los nodos de Calendar y notificación.] En la rama calificada pasan dos cosas a la vez: se crea el evento de la visita en el calendario, y le llega un aviso al agente humano: "Nuevo lead calificado, visita reservada". Aquí puedes enchufar un CRM como GoHighLevel —el que usan muchas agencias, te dejo el enlace abajo— o empezar con algo tan simple como una hoja de cálculo.

[PANTALLA: vista general del workflow completo otra vez.] Eso es todo. Ocho nodos, cero código, y un sistema que trabaja mientras tú no estás. Si quieres montarlo tú mismo desde cero también puedes —n8n es gratis instalándolo en tu ordenador, o por unos pocos euros al mes en un servidor; te dejo cómo en la descripción.

---

## [SECCIÓN 4 · Demo en vivo + cómo adaptarlo · 1.5 min]

> [PANTALLA: enviar un mensaje de prueba "Hola, busco piso de 2 habitaciones en Valencia, hasta 200.000€" y ver la respuesta llegar.]

Vamos a probarlo de verdad. Mando un mensaje como si fuera un cliente: "Hola, busco un piso de dos habitaciones en Valencia, presupuesto hasta 200.000 euros."

Y mira: en tres segundos, la IA responde con el nombre del cliente, confirma lo que busca, y le ofrece tres horarios para visitar. [PANTALLA: respuesta llegando.] El evento aparece en el calendario. El agente recibe el aviso. Todo solo.

¿Y si no eres de inmobiliaria? Este mismo sistema sirve para una clínica dental que agenda primeras consultas, un gimnasio que capta socios, o un despacho que filtra clientes. Cambias el texto de las instrucciones de la IA y ya está. La arquitectura es idéntica. En los próximos videos voy a montar exactamente eso para otros sectores.

---

## [CTA · 30s]

> [PANTALLA: tarjeta final con el enlace a la plantilla + suscripción.]

Te he dejado este workflow completo como **plantilla gratuita** para que lo importes a tu n8n y lo tengas funcionando hoy mismo: el enlace está en la descripción, solo te pido tu correo para enviártelo. Y si quieres la versión avanzada —con calificación de leads por presupuesto, seguimiento automático a los que no responden, y conexión con los portales inmobiliarios— tienes el Kit Inmobiliaria IA completo, también abajo.

Si esto te ha resultado útil, suscríbete: cada semana monto un sistema de automatización con IA para un negocio distinto, paso a paso y sin código. Nos vemos en el próximo.

---

## Notas de producción (anti-AI-Slop + compliance)

- **Fuentes oficiales a citar en pantalla/descripción**: docs.n8n.io (400+ integraciones), docs.anthropic.com (API). Refuerza E-E-A-T.
- **Disclaimer descripción**: "Contenido educativo. Las funciones y precios de las herramientas cambian; verifica en su documentación oficial. No garantizamos resultados de negocio."
- **Yellow-icon a evitar**: NO usar "gana millones", "no trabajes", "reemplaza empleados". Tono = utilidad, no get-rich-quick.
- **Datos VERIFICADOS** (usar estas fuentes en pantalla):
  - "7 de cada 10 entrevistan a un solo agente" → NAR 2024 Profile of Home Buyers and Sellers (https://www.nar.realtor/research-and-statistics). NO decir "el primero que responde".
  - "7x en primera hora" → Harvard Business Review, "The Short Life of Online Sales Leads" (2011), 1,25M leads (https://hbr.org/2011/03/the-short-life-of-online-sales-leads).
  - "21x en 5 min" → MIT / Lead Response Management Study, Dr. James Oldroyd (https://www.leadresponsemanagement.org/lrm_study/).
  - "fuera de horario": afirmación CUALITATIVA, sin porcentaje (el 50% no es verificable).
- **Screencast**: grabar con OBS, n8n real. La pantalla es el contenido — cero necesidad de cara.
- **Voz**: Eleven v3, voz masculina/femenina neutra profesional. Stability 0.5.
