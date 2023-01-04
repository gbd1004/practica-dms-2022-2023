# **PRÁCTICA 01**

___


<br/>
<br/>

En el presente documento se redactará el informe sobre la práctica 01 de la asignatura de Diseño y mantenimiento del software.

## **Alumnos**

El grupo de alumnos que realizará la práctica está compuesto por:
* Guillermo Arcal García (gag1005@alu.ubu.es)
* Gonzalo Burgos de la Hera (gbd1004@alu.ubu.es)
* Santiago Díaz Gómez-Guillamón (sdg1002@alu.ubu.es)
* Gadea Lucas  Pérez (glp1002@alu.ubu.es)

## **Tabla de contenido**

- [**PRÁCTICA 01**](#práctica-01)
  - [**Alumnos**](#alumnos)
  - [**Tabla de contenido**](#tabla-de-contenido)
  - [**Repositorio**](#repositorio)
  - [**Diseño Frontend**](#diseño-frontend)
    - [**Arquitectura de dos niveles (Documento-Vista)**](#arquitectura-de-dos-nivelesdocumento-vista)
  - [**Diseño Backend**](#diseño-backend)
    - [**Arquitectura de tres capas**](#arquitectura-de-tres-capas)
  - [**Sobre Auth**](#sobre-auth)
  - [**Decisiones de diseño**](#decisiones-de-diseño)
    - [***Patrón fachada***](#patrón-fachada)
    - [***Aspecto reports***](#aspecto-reports)
    - [***Votos***](#votos)
  - [**De cara al futuro**](#de-cara-al-futuro)
  - [**BIBLIOGRAFÍA**](#bibliografía)
  
## **Repositorio**

El _fork_ del repoositorio usado por los alumnos es el siguiente:  https://github.com/gbd1004/practica-dms-2022-2023.


<br/>
<br/>

---
___

<br/>
<br/>
<!-- # Memoria -->
<h1 style="border-bottom: none">
    <b>Memoria</b>
</h1>

A continuación se explicarán las decisiones de diseño tomadas a lo largo de la práctica con su justificación correspondiente.





##  **Diseño Frontend**
En el _frontend_ se pueden distinguir las siguientes capas:
1.  <ins>Capa de presentación:</ins> En esta capa se implementan los métodos que hacen llamadas a las fachadas (_web controllers_).
2. <ins>Capa de datos:</ins> En esta capa se hace llamada al ```backendservice``` (del que se hablará más adelante) y el ```authservice```, que funcionan a modo de fachadas para poder acceder a los subsistemas que poseen los datos de la API.

Por otro lado, en el _frontend_ también se encuentran los archivos HTML y el resto de programación web que conformará el aspecto de la página.


###  **Arquitectura de dos niveles (Documento-Vista)**

Una de las arquitecturas más tradicionales es la de dos capas, i.e.: [Cliente, servidor]. Como se ha mencionado ya, nuestro _frontend_ posee dos capas diferenciadas, por un lado, una capa a nivel de presentación y, por otro, una capa a nivel de datos. La lógica del _frontend_ está repartida entre el nivel de datos y el de presentación.

![Ilustración 3: Arquitectura de dos capas.](img/arch_2ly.png)


Para futuras modificaciones, se propone reutilizar el código de los ficheros HTML de _macros_. Para poder extender más fácilmente el código (principio SOLID __Open/Closed__) se haría uso del polimorfismo (herencia). Así pues, se crearía un fichero ```lists.html``` que funcionaría como una interfaz común de la que heredarían los subelementos ```list_questions.html```, ```list_answer.html```, ```list_comments.html```, etc... Se deberá tener en cuenta el principio ___Liskov's substitution___ de forma que se pueda sustituir una instancia de ```lists.html``` por una instancia de uno de los subelementos sin modificar el comportamiento del programa. De esta forma lograríamos reducir el fuerte acoplamiento actual y garantizaríamos que todas estas listas estén abiertas a su extensión (pero no a su modificación).


## **Diseño Backend**
Aunque por lo general el _backend_ suele tener tres capas (i.e.: servicio, negocio y datos), en ocasiones se incluye una capa superior de presentación, como se ha hecho en este caso. La razón de esta decisión recae en la naturaleza de la aplicación, i.e. una API REST. Así pues, en esta capa se incluyen los controladores REST. Por otro lado, puesto que no se hace uso de la capa de servicios, finalmente, nos decidimos por una arquitectura de tres capas: [Presentación, Lógica, Datos]. 

Así pues en la capa de _backend_ se pueden distinguir las siguientes capas:

1. <ins>Capa de datos:</ins> En esta capa se implementa la BBDD local que soporta la API. Sin embargo, no se hace directamente a través de _scripts_ SQL, sino a trés de un ORM. En este caso, se ha hecho uso de SQLAlchemy, que permite, a través de código escrito en Python, mapear y relacionar objetos de la "BBDD". Otro detalle importante es la división de los resultados: _results_ y _resultsets_. En el primer módulo se encuentra la definición de las tablas y la representación de cada objeto. En el segundo módulo se encuentran aquellas sentencias SELECT que devuelven listas de registros, los crean o modifican.
2. <ins>Capa de lógica:</ins> En esta capa se determina el manejo específico que la aplicación hace con los datos. En este nivel se procesa la información recopilada en el nivel de presentación contra otra información de la capa de datos (en el proceso, se añaden y modifican los registros).
3. <ins>Capa de presentación:</ins> En la capa de presentación se encuentran aquellos métodos enfocados a que las acciones de los usuarios interactuen con el backend. Estos métodos se ejecutan en el servidor. En este caso, respetando las directivas del fichero ```spec.yml```, se da formato JSON a los datos obtenidos de la BBDD a través de la capa de lógica. De esta forma, el _frontend_ podrá manejar los datos de las respuestas de los métodos REST fácilmente (i.e.: diccionarios). Adicionalmente se devuelve también el código de respuesta HTTP.



### **Arquitectura de tres capas**
 En este caso, se usará una arquitectura multicapa (i.e. se separan los componentes en distintas capas físicas). Estas capas están formadas por distintos subsistemas y están organizadas jerárquicamente siguiendo una dependencia siempre hacia capas inferiores. En otras palabras, una capa dependerá exclusivamente de las capas inferiores. Esta encapsulación permite la reutilización del código y permite mentener el principio DRY (_"Don't repeat yourself "_).


![Ilustración 1: Arquitectura de 3 capas](img/arq_3ly.png)


Se listan a continuación las razones por las que se ha decidido cambiar la arquitectura del _backend_:
* Gracias a esta arquitectura se puede mantener el principio SOLID  _"Single Responsability"_, ya que permite que cada capa tenga una única responsabilidad.
* Fácil implementación de la arquitectura. Además, nos permite localizar los fallos más fácilmente durante el proceso de programación el código.
* Los servicios de cada nivel se pueden personalizar y optimizar sin que afecte a los demás niveles (_Open/Close Principle_). 
* Esta arquitectura tiene como característica una mejor seguridad dado el aislamiento y separación entre las capas (por ejemplo, evita las inyecciónes de código SQL).

<br/>

<div style="border-style: solid;text-align:justify" >
 <ins> <b>NOTA</b></ins>:
 Para poder mapear correctamente la base de datos, se ha optado por utilizar el atributo de mapeado de SQLAlchemy: "Polimorphic Identity". De esta forma, se crea una ISA con discriminante "type". Aunque físicamente se crean dos subclases y una superclase, la ventaja es que se mapean como si fuese una sola. Este diseño se ha implementado tanto para los registros de votos como los de reportes.
</div>

<br/>

![Ilustración 2: Identidad polimórfica](img/bbdd.png)


<br/>




## **Sobre Auth**
La autenticación en el servidor implementada está basada en _tokens_. En palabras simples, se envía al servidor un _token_ "firmado" en cada una de las _requests_. Este _token_ se obtiene tras realizar el login (introduciendo un usuario y constraseña correctos). 

En resumidas cuentas, el flujo de datos para la autentificación es el siguiente:
* De forma transparente, el consumidor pide un token al proveedor.
* El consumidor redirige al usuario a una página segura pasándo el token de usuario como parámetro.
* El usuario se autentica validando el _token_.
* El proveedor envía al usuario de vuelta a la página del consumidor (esta vez con su identidad).

![Ilustración 3: Autentificación basada en tokens](img/auth.png)

<br/>

## **Decisiones de diseño**
### ***Patrón fachada***
Para poder acceder al _backend_ desde el _frontend_, se hace uso de la clase ```backendservice``` que hace la función de fachada. De esta forma, se abstrae el _backend_ evitando que este tenga que lidiar directamente con el cliente HTTP, establecer la conexión, interpretar la respuesta obtenida, etc...

### ***Aspecto reports***
Finalmente, es preciso recordar que una vez que los reportes son aceptados o rechazados por el moderador, ya no se pueden volver a modificar (aunque no se eliminan del almacenamiento de la BBDD). Por lo tanto, se ha decidido ocultar el botón de aquellos reportes cuyo estado ya haya sido determinado.

### ***Votos***
Se ha decidido eliminar la opción de votos negativos, dejándo solamnete un valor de "popularidad" de cada respuesta o comentario. Esta práctica es común en muchas plataformas, ya que evita conflictos entre los usuarios.

<br/>

## **De cara al futuro**
Las aplicaciones como la implementada a lo largo de la presente práctica tienen un sinfín de posibilidades de desarrollo y se pueden añadir muchas funcionalidades a cada uno de sus componentes. En nuestro caso, nos hemos centrado en el usuario y hemos decidido seguir una línea basada en el perfil personal del mismo, lo que nos permite atraer la atención de los posibles usuarios y lograr que se registren con el fin de personalizar sus perfiles. Para ello, se listan a continuación las mejoras posibles encontradas:

* La primera medida a tomar es darle un nombre llamativo a la aplicación que atraiga a los usuarios. En este caso se ha decidido llamar: "TechTalk". Se ha diseñado un logo simple que representa la aplicación.
<br/>
<img src="img/logo.png" width="200" />
<br/>
Este rótulo se situará en la parte superior derecha de las distintas interfaces (la parte izquierda está reservada para los enlaces hacia las distintas secciones).

* Creación de un área personal. En la barra superior de la aplicación, se propone añadir una nueva sección centrada exclusivamente en la información relativa al usuario registrado. En esta sección, se podrán distinguir los siguientes elementos:
	- Perfil del usuario: modificación de credenciales, foto de perfil, descripción, etc...
	- Sección en la que el usuario puede ver todos los elementos que ha publicado.
	- Añadir un símbolo de "Ayuda" para que se pueda acceder al manual de usuario _online_.
	- Gráfica de popularidad en función de las participaciones del usuario y los votos recibidos (se puede incluir también el número de visitas a las preguntas o respuestas).
	- Además, se pretende personalizar aún más la aplicación con opciones multilenguaje. Es decir, se quiere internacionalizar la aplicación.
  <br/>
  <img src="img/interfaz.png" width="200" />
  <br/>
* Por otro lado, incluir en el registro de los usuarios un campo con un correo electrónico. De esta forma, se incrementa la seguridad con el sistema de doble confirmación y con el aviso de nuevos accesos desde dispositivos no registrados previamente. También evitará el posible registro indebido de _bots_ en el sistema o multicuentas masivas. Sin embargo, el punto principal de esta medida es el envío de notificaciones cuando otro usuario interactúe con alguna de las preguntas, respuestas o comentarios realizados por el usuario en cuestión. Para dejar esta idea más clara se ha decidido diseñar un correo de prueba que se adjunta a continuación: 
<br/>
<img src="img/correo.jpeg" width="6000" />
<br/>

* Se pretende también determinar (añadiendo un tipo de rol más) qué usuarios son expertos, de forma que puedan verificar respuestas dadas (lo cuál da prestigio y fiabilidad a la respuesta).
* Tapar contenido sensible (NSFW) hasta que el usuario decida que quiere visualizarlo.

### **Opciones de diseño**
Para las medidas anteriores, se propone realizar las siguientes implementaciones:
* Para que el usuario pueda modificar sus credenciales, se utilizarán **formularios** en el _frontend_. Para ello se aprovecharán los _templates_ y _macros_ ya creados aprovechando el polimorfismo.
* Para almacenar la información personal de los usuarios, se propone crear un nuevo _script_ en la carpeta ```resultset``` (dms2223backend/dms2223backend/data/db) de nombre ```statisticsdb.py```. En ella se implementarán los métodos estadísticos que se quiera mostrar.
<br/>
<div style="border-style: solid;text-align:justify" >
 <ins> <b>NOTA</b></ins>:
  En este caso, NO se creará una tabla de usuarios.
  Puesto que no se crea una tabla de usuarios, sino que se sigue utilizando el servicio Auth (haciendo uso del token de usuario), estas estadísticas no quedan almacenadas, sino que se calculan cada vez. El generar y mostrar estas gráficas constantemente, podría suponer mucha carga computacional y, por ende, una desventaja. Por ello, estos métodos GET que muestran gráficas y estadísticas tendrán un comportamiento lazy, i.e.: solamente se mostrarán cuando el usuario acceda a la sección de estadísticas (situada en su área personal).
</div>
<br/>

* Algunos métodos posibles son los siguientes:

  - Primero, se creará un método ```user_elements()``` que obtenga los elmentos del usuario en cuestión (pasando como parámetro solamente el _token_). Al contrario que el resto de estadísticas, se mostrarán estos resultados en el apartado de "mis elementos" (situada también en el área personal). Esto permitiirá al usuario acceder facilmente a su propio contenido.
  <br/>
  Ejemplo:
  <br/>
  
  ```
  preguntas_user: list = query(Pregunta).where(Pregunta.owner == token).all()
  ``` 
  <br/>

  - Actividad del usuario a lo largo del tiempo. Se obtendrá el número de elementos publicados por el usuarios (con ```owner == token```) teniendo en cuenta su atributo ```timestamp```.
  <br/>
  Este método tendrá como parámetros de entrada el intervalo de días en los que se quiere mostrar la actividad y los elementos que se quieren consultar, a saber, preguntas, respuestas, comentarios, votos o la combinación de varios de ellos. Se permitirá mostrar más de uno a la vez (parámetros de entrada de caracter _Optional_).
  <br/>
  Ejemplo:
  <br/>

  ```
  actividad_preguntas_dia = query(Pregunta).where(Pregunta.owner == token, Pregunta.timestamp.day == timestamp).count()
  ``` 
  <br/>

  - Cálculo de popularidad de los elementos en función de los votos recibidos. Para ello se recurrirá al método ```user_elements()``` que nos devuelve todos los elementos del usuario, y se obtendrá el número de votos de cada uno, iterando por los identificadores de dichos elementos.
  <br/>
  Ejemplo:
  <br/>

  ```
  for elem in user_elements(token):
    popularidad: int = query(Vote).where(Vote.eid == elem.id).count()
  ``` 
  <br/>

* Para mostrar estos gráficos (en el _frontend_), se crearán ficheros en JavaScript. En la referencia [3] se muestran algunos ejemplos. Para hacer un diagrama de barras por ejemplo, se empleará este código:
```
new Chart("grafico_barras", {
  type: "bar",
  data: {
    labels: xValues,
    datasets: [{
      backgroundColor: ["red", "green","blue"],
      data: yValues
    }]
  }
});
```

* Para modificar la información personal de los usuarios, se propone realizar operaciones UPDATE en dms2223auth (además de añadir el correo electrónico en ```user```).

* Para notificar a los usuarios de que alguno de sus elementos han sido votados, respondidos o reportados, se empleará el patrón **Observador**. Para ello, habrá un observador que observe estos cambios y los notifique. Recordemos que esta notificación llegará al usuario a través de su correo electrónico (previamente añadido).

* Por otro lado, se pretende añadir una capa de lógica en el _frontend_, usando así una arquitectura de tres capas. Ahí se añadirán las opciones avanzadas de multilenguaje, _theme_, censura NSFW, etc...


### **Otras medidas**
Se proponen también otras mejoras que se escapan un poco de la línea de personalización del usuario mencionada hasta el momento.
* Mejorar el diseño gráfico de la interfaz.
* Opción para "desvotar".
* Posibilidad de modificar las preguntas, respuestas o comentarios (se marcará la fecha de la edición).
* Filtro/buscador para encontrar discusiones a partir de palabras clave.
* Posibilidad de ordenar las discusiones por identificador, fecha, polularidad, etc...
* Posibilidad de establecer etiquetas (_tags_).
* Edición avanzada (markdown, html, etc..).
* Anuncios personalizados que permitirán la monetización de la aplicación para invertir en futuras mejoras.
* Otra medida es la creación de comunidades, que podrían agrupar conjuntos de discusiones temáticas que atraigan a usuarios interesados en ese tema.
* [TODO (opcional): Capa lógica frontend para edicion avanzada y tapar contenido sensible]
* [TODO (opcional): Posibles mejores para caso de que la página crezca mucho]




<br/>
<br/>

___
---

<br/>
<br/>

## **BIBLIOGRAFÍA**

- [1] title: "Capas, cebollas y colmenas: arquitecturas en el backend."
author: "Cabrera, A.A."
date: "2019"
link: https://www.adictosaltrabajo.com/2019/07/02/capas-cebollas-y-colmenas-arquitecturas-en-el-backend/

- [2] title: "Arquitectura de una API REST. Desarrollo de aplicaciones web."
author: "juanda.gitbooks"
date: (n.d.)
link: https://juanda.gitbooks.io/webapps/content/api/arquitectura-api-rest.html.

- [3] title: "Chart.js."
author: "w3schools"
date: (n.d.)
link: https://www.w3schools.com/ai/ai_chartjs.asp.









