import requests
import dns.resolver
import threading
import os
import urllib3
from colorama import Fore, Style, init
from fpdf import FPDF
from datetime import datetime

# Silenciar avisos de certificados (SSL)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

init(autoreset=True)

# --- 1. CONFIGURACIÓN DEL REPORTE PDF ---
class RAJA_Report(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'vErtex: SECURITY AUDIT REPORT', 0, 1, 'C')
        self.ln(5)

# --- 2. MOTOR DE LA HERRAMIENTA ---
class RajaEngine:
    def __init__(self, target):
        self.target = target.replace("https://", "").replace("http://", "").strip("/")
        self.results = []
        self.pdf = RAJA_Report()
        self.screenshot_path = None

    def log(self, text, status="info"):
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.results.append((status, text))
        if status == "success": print(Fore.GREEN + f" [{timestamp}][✓] {text}")
        elif status == "error": print(Fore.RED + f" [{timestamp}][✗] {text}")
        else: print(Fore.BLUE + f" [{timestamp}][*] {text}")

    def analyze_headers(self):
        url = f"https://{self.target}"
        try:
            res = requests.get(url, timeout=10, verify=False)
            headers = res.headers
            self.log(f"Analizando cabeceras en {url}")
            checks = {
                "Content-Security-Policy": "Proteccion XSS",
                "X-Frame-Options": "Proteccion Clickjacking",
                "Strict-Transport-Security": "HSTS"
            }
            for h, desc in checks.items():
                if h in headers:
                    self.log(f"{h}: Configurado", "success")
                else:
                    self.log(f"{h}: AUSENTE", "error")
        except Exception as e:
            self.log(f"Error web: {str(e)}", "error")

    def dns_recon(self):
        self.log(f"Iniciando DNS Recon para {self.target}")
        for r_type in ['A', 'MX']:
            try:
                answers = dns.resolver.resolve(self.target, r_type)
                for rdata in answers:
                    self.log(f"Registro {r_type}: {rdata}", "success")
            except:
                continue

    def take_screenshot(self):
        self.log("Iniciando captura de pantalla...")
        from selenium import webdriver
        from selenium.webdriver.firefox.options import Options
        import time
        options = Options()
        options.add_argument("--headless")
        options.set_preference("accept_insecure_certs", True)
        try:
            driver = webdriver.Firefox(options=options)
            driver.set_page_load_timeout(30)
            url = f"https://{self.target}" if not self.target.startswith('http') else self.target
            driver.get(url)
            time.sleep(5) 
            driver.set_window_size(1280, 720)
            path = f"evidencia_{self.target.replace('.', '_').replace('/', '_')}.png"
            driver.save_screenshot(path)
            self.screenshot_path = path
            driver.quit()
            self.log(f"Captura guardada: {path}", "success")
        except Exception as e:
            self.log(f"Fallo captura: {e}", "error")

    def generate_pdf(self):
        self.log("Generando reporte PDF final...")
        self.pdf.add_page()
        self.pdf.set_font("Arial", 'B', 14)
        self.pdf.cell(0, 10, f"OBJETIVO: {self.target}", ln=True)
        self.pdf.ln(5)

        # Insertar imagen si existe
        if self.screenshot_path and os.path.exists(self.screenshot_path):
            try:
                self.pdf.set_font("Arial", 'B', 12)
                self.pdf.cell(0, 10, "EVIDENCIA VISUAL:", ln=True)
                self.pdf.image(self.screenshot_path, x=10, w=180)
                self.pdf.ln(5)
            except Exception as e:
                self.log(f"No se pudo insertar imagen en PDF: {e}", "error")

        # Resultados a color
        for status, text in self.results:
            try:
                clean_text = text.encode('latin-1', 'ignore').decode('latin-1')
                if status == "error": self.pdf.set_text_color(200, 0, 0)
                elif status == "success": self.pdf.set_text_color(0, 120, 0)
                else: self.pdf.set_text_color(0, 0, 0)
                self.pdf.multi_cell(0, 8, f"[{status.upper()}] {clean_text}")
            except: continue

        self.pdf.set_text_color(0, 0, 0)
        clean_name = self.target.replace(".", "_").replace("/", "_")
        filename = f"Reporte_vErtex_{clean_name}.pdf"
        
        try:
            self.pdf.output(filename)
            print(Fore.YELLOW + f"\n[+] SISTEMA: Reporte final generado en {filename}")
        except Exception as e:
            print(Fore.RED + f"\n[!] Error al guardar PDF: {e}")
def get_geo(self):
        self.log("Rastreando ubicación del servidor...")
        try:
            import socket
            ip = socket.gethostbyname(self.target)
            data = requests.get(f"http://ip-api.com/json/{ip}").json()
            if data['status'] == 'success':
                info = f"Ubicacion: {data['city']}, {data['country']} ({data['isp']})"
                self.log(info, "success")
                self.results.append(("success", f"GEOLOCALIZACIÓN: {info}"))
        except:
            self.log("No se pudo obtener la geo-ubicación", "error")

# --- 3. LANZADOR PRINCIPAL ---
def main():
    os.system('clear')
    print(Fore.CYAN + Style.BRIGHT + "🦅 vErtex |Developed by ----> AlBerKOMA| Herramienta de Auditoria Personalizada")
    print(Fore.WHITE + "—" * 60)
    
    target_input = input(Fore.YELLOW + "🎯 Ingrese URL objetivo: ")
    if not target_input:
        print(Fore.RED + "[!] No has introducido un objetivo.")
        return

    engine = RajaEngine(target_input)

    # Ejecución secuencial para evitar conflictos de hilos con Selenium
    engine.analyze_headers()
    engine.dns_recon()
    engine.take_screenshot()
    engine.generate_pdf()

if __name__ == "__main__":
    main()
