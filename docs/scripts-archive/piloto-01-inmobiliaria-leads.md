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
2. Una inmobiliaria pierde el 40% de sus leads por esto. Lo arreglé con IA en una tarde
3. El sistema de captación con IA que las agencias venden por 2.000€ (te lo monto gratis)

---

## [HOOK · 0-20s]

> [PANTALLA: dashboard de n8n con un workflow ya montado, ejecutándose en vivo. Mensaje de WhatsApp entrando → respuesta automática en 3 segundos.]

Un estudio de la Asociación de Agentes Inmobiliarios reveló algo brutal: el 78% de los compradores contrata a la **primera** inmobiliaria que le responde. No a la mejor. A la **primera**. Y la mayoría de las agencias tardan horas en contestar un lead. En este video vas a ver, paso a paso y en pantalla, cómo montar un agente de inteligencia artificial que responde a cada cliente en menos de 30 segundos, califica si es serio, y agenda la visita solo. Sin escribir una sola línea de código. Quédate, porque al final te dejo la plantilla para que lo copies hoy mismo.

---

## [SECCIÓN 1 · El problema que cuesta dinero · 1.5 min]

> [PANTALLA: gráfico simple de "tiempo de respuesta vs probabilidad de cierre", caída pronunciada.]

Vamos a poner números sobre la mesa, porque esto no es teoría. Cuando alguien rellena un formulario en un portal inmobiliario, no está mirando solo tu anuncio. Está rellenando el de cinco agencias a la vez. El reloj empieza a correr en ese segundo.

Los datos del sector son consistentes: si respondes en los primeros 5 minutos, tienes hasta 9 veces más probabilidad de convertir ese lead en una visita. Si tardas una hora, ese lead ya está hablando con tu competencia. Si tardas hasta el día siguiente, está prácticamente muerto.

El problema es que un agente inmobiliario humano no puede estar disponible 24 horas. Duerme, conduce, está en visitas, es fin de semana. Y los leads no entienden de horarios: el 50% llegan fuera del horario de oficina.

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

> [PANTALLA: screencast real de n8n. Cada sub-paso se muestra construyéndose en vivo. Zoom en los puntos clave.]

Abro n8n. Si no lo tienes, en la descripción te dejo cómo instalarlo gratis en tu ordenador o en un servidor por unos pocos euros al mes —ahí uso Hostinger, te dejo el enlace.

**Paso uno: el disparador.** Añado un nodo "Webhook". Esto crea una dirección única a la que tu formulario o tu WhatsApp envían el mensaje del cliente. Copio esa dirección. [PANTALLA: copiar webhook URL.] Ya tenemos la puerta de entrada.

**Paso dos: conectar la IA.** Añado el nodo de modelo de lenguaje. Pego mi clave de API —te muestro dónde se consigue, es gratis empezar. Y aquí está la magia: en el campo de instrucciones, le escribo al modelo quién es. Mira esto:

> [PANTALLA: escribir el system prompt en el nodo.]

"Eres el asistente de una inmobiliaria. Cuando llegue un mensaje de un posible cliente, responde de forma cálida y profesional en español. Identifica: qué tipo de inmueble busca, su presupuesto, y su zona. Si da esos tres datos, ofrécele tres horarios para una visita. Si falta información, pregúntala con amabilidad. Nunca inventes propiedades que no existen."

Esa última frase es clave y es parte del sello de calidad: le prohibimos a la IA inventar. Esto evita el problema número uno de los chatbots malos.

**Paso tres: la decisión.** Añado un nodo "Switch". Esto es un cruce de caminos: si la IA marcó el lead como "caliente", va por un camino; si necesita seguimiento, por otro. [PANTALLA: configurar las dos ramas.]

**Paso cuatro: las acciones finales.** En la rama "caliente", conecto dos nodos: uno que crea el evento en Google Calendar con la visita, y otro que guarda el contacto. Aquí puedes usar un CRM especializado como GoHighLevel —el que usan muchas agencias, te dejo el enlace— o algo tan simple como una hoja de cálculo para empezar.

Y un último nodo: una notificación al agente humano por WhatsApp o email que dice "Nuevo lead calificado, visita reservada para el jueves a las 18h". El humano se despierta con la visita ya agendada.

> [PANTALLA: vista completa del workflow terminado, todas las cajas conectadas.]

Esto es todo el sistema. Ocho nodos. Cero código.

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
- **Dato del 78%/9x**: VERIFICAR con fuente real (Harvard Business Review "Lead Response Management Study" o similar) antes de publicar. Si no se verifica, suavizar a "los estudios del sector muestran que responder rápido multiplica la conversión".
- **Screencast**: grabar con OBS, n8n real. La pantalla es el contenido — cero necesidad de cara.
- **Voz**: Eleven v3, voz masculina/femenina neutra profesional. Stability 0.5.
