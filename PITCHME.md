++

#### Introducción - contexto

Con la nueva metodologia y el nuevo software la compañia busca:
* Mismo frente a cambios diários, obtener información en tiempo real de sus locales físicos |
* Reforzar el monitoreo de los locales, logrando mapear muchos puntos que hoy no tienen visibilidad |
* Ordenamiento centralizado de la infraestrutura de TI |
* Reportes de buena calidad, con alcance regional y actualizados |

++

#### Introducción - Por Fin

* Mejorar los tiempos de respuesta y la disponibilid de los servicios |
* Lograr tomar desiciones con mejor claridad de la información |

++

#### Introducción - Por Fin

Las informaciones claves y necesarias para el éxito de la solución, no están disponible en ningun lado y no existe ningun plano para ordenar esto.

El software que tiene que garantizar el flujo automatizado, y que debe ser implementado en 2 meses tiene gran cantidad de detalles.

++

#### Introducción - Pregunta Final

Sín la información principal el software tiene como ser implementado con éxito?

## @fa[angle-down] SI    |    NO @fa[angle-right]

++

#### Introducción - FIN

FIN

--

# Escenario Actual

++

#### Escenario Actual - Equipos

Un extracto de las conversaciones con las areas:
* Apertura de Tiendas |
* Soporte Técnico |
* Data Center |
* Mesa Especializada |
* NOC |
* Redes y Comunicaciónes (nível 2 y 3) |
* Monitoreo |

++

#### Escenario Actual - Día a día

* Información descentralizada hasta entre equipos del mismo Pais |
* No se tiene monitoreo de todos los puntos de falla de uno local |
* Los inventários de los Racks están en planillas, lo que dificulta la busqueda y la actualización |
* No hay información completa y de buena calidad acerca de las características de cada local |

++

#### Escenario Actual - ilustración
![actual](imgs/actual.png)
* lo mismo para RyC y DC ( 20 puntos offlines )

--

# Escenario Futuro

++

#### Escenario Futuro - ilustración

![topologia](imgs/netbox.png)

++

#### Escenario Futuro: objetivos macros

* Centralizar la información: Disminuir el tiempo en los procesos de busqueda de locales, redes y contactos |
* Integracioenes: Tener un punto central de información que se replica a reportes, monitoreos, y equipos |
* Accesibilidad: Técnicos en campo puedan agregar una balanza al monitoreo, por ejemplo |
* Inventario detallado: Ordenar los hardwares en sus locales y obtener informácion frente a una urgencia |
* IPAM: Documentacíon de toda los escopos de Red |

++

#### Escenario Futuro - Riesgo!!!!!!

* Nueva metodologia/herramienta sín alcance Regional |
* Ingreso de datos a la herramienta falla frente a uno cambio/cierre/apertura de un local |
* Orden no llegue con claridad hasta el area de soporte |
* DC no ingresen los detalles de los servidores, los contactos o las direciónes |
* RyC no documentan la redes y vlans |

++

#### Escenario Futuro - custo

* Custo de software = $0,00 |
* Full stack Developer (No exclusivo para esto proyecto. Tenemos mucho que hacer.) |

++

#### Escenario Futuro: Responsabilidades

> "- Por fin, el motivo de  la cita!"

william Shakespeare, poco antes de construir el edificio mas grande de la America Latina - 12 de junio de 2012)

++

#### Escenario Futuro: Responsabilidades

> "Compadre, voy a fumar un cigarrio y vuelvo manana!"

Diego “El Pitbull” Rivas, poco antes de la apertura del Jumbo Costanera - 11 de junio de 2012

++

#### Escenario Futuro: Responsabilidades

Cuando las equipos tengan claro cuanto tiempo y información se pierde
tenendo una estructura offline y fuera de estandar, van buscar mejorar
la calidad de sus trabajos.

La organización de la información es una tarea que no esta bien
definida, y mientras esto no empieze, el esforzo sin inteligencia y el
dolor de cabeza seran aliados de nuestro día a día.

--

# NETBOX

++

##### netbox: Where is Netbox?

[NetBox](https://netbox.readthedocs.io/en/latest/) is an open source web application initially conceived by the network engineering team at [DigitalOcean](https://www.digitalocean.com/). Designed to help network management:

* IP addr management (IPAM) - IPs, VRFs, and VLANs
* Equipment racks - Organized by group and site
* Devices - Devices and where they are installed
* Connections - Network, console, power conns
* Virtualization - Virtual machines and clusters
* Data circuits - Long-haul circuits and providers
* Secrets - Encrypted storage of credentials

++

#### netbox - ventajas técnicas

* posibilidad de integración con otras herramientas |
 * API y Webhook |
* docker |
 * LDAP/AD y kubernetes |
* python Django (lenguaje que ya trabajamos) |
 * postgresql - base de datos impecable y sín custo |
* buena interface web |
* open source y con gran cantidad de seguidores/desarrolladores |

