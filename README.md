Gemini said
Aquí tienes el README.md exactamente igual, siguiendo el patrón de diseño, los colores y la estructura de bloques que me has mostrado. Está listo para copiar y pegar:

🚀 vErtex v6.0 - ENTERPRISE EDITION
vErtex v6.0 es la evolución definitiva de la suite de auditoría avanzada. Diseñada para entornos corporativos, esta versión Enterprise integra escaneo de vulnerabilidades críticas, análisis de infraestructura profunda y un motor de reportes ejecutivos con scoring de riesgo real.

📈 Historial de Versiones
Versión	Banner	Descripción
v6.0		OWASP Scanner + WAF Detect + DNSSEC + API Discovery.
v4.2		Malware Engine + Vulnerability Matrix + PDF Fix.
v4.1		Geolocalización + Reportes PDF iniciales.
v3.0		Escaneo de puertos avanzado y DNS.
v2.0		Manejo de excepciones y Auto-Banner.
🚀 Características Principales
OWASP Vulnerability Scanner:  Detección de XSS, SQLi y LFI.

WAF Fingerprinting:  Identificación de Firewalls (20+ Signatures).

DNS Security Audit:  Análisis de registros SPF, DMARC y CAA.

SSL/TLS Deep Scan:  Auditoría de certificados y cifrados.

Network Intelligence:  Mapeo de servicios y versiones.

Enterprise Reporting:  Generación de evidencias y scoring.

🛠️ Stack Tecnológico (Versiones)
Componente	Badge	Función
Requests		Auditoría HTTP/S y Fuzzing de endpoints.
Dnspython		Resolución y validación de seguridad DNS.
FPDF		Motor de generación de reportes técnicos.
Whois		Reconocimiento de dominio y propiedad.
📊 Sistema de Scoring (Matriz de Riesgo)
El motor de vErtex evalúa la seguridad del objetivo mediante una puntuación acumulativa:

Severidad	Estado	Impacto en el Score
CRITICAL		-25 Puntos (SQLi, Exposure, RCE).
HIGH		-15 Puntos (SSL obsoleto, WAF ausente).
MEDIUM		-10 Puntos (Falta de CSP, HSTS).
LOW		-5 Puntos (Info Leakage, Banners).
🛠️ Instalación y Uso
Optimizado para Kali Linux y sistemas basados en Debian.

1. Requisitos del sistema
Bash
sudo apt update && sudo apt install chromium-driver -y
2. Dependencias de Python
Bash
pip install requests dnspython python-whois colorama fpdf urllib3 --break-system-packages
3. Ejecución
Bash
python3 vErtex_v6.py -t <objetivo.com> --mode deep
⚠️ Descargo de Responsabilidad
Este software ha sido creado para uso profesional en auditorías éticas. El uso de vErtex contra activos sin permiso explícito es una violación de las leyes de ciberseguridad. El autor no asume responsabilidad por daños causados por el mal uso del script.

Desarrollado por albertChOXrX
vErtex: Precision Security & Deep Reconnaissance.
