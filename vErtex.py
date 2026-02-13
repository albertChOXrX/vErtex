import requests
import dns.resolver
import os
import urllib3
import socket
import ssl
from colorama import Fore, Style, init
from fpdf import FPDF
from datetime import datetime

# Configuración inicial
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

def show_banner():
    os.system('clear')
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}
        __   __        _            
        \ \ / /__ _ __| |_ _____ __ 
         \ V / -_) '_ \  _/ -_) \ / 
          \_/\___|_|  \__\___/_\_\  
                                    
        {Fore.WHITE}Ultimate Security & Forensics Suite v3.0
        {Fore.RED}Nombre del Programa: vErtex
        {Fore.RED}Autor: albertChOXrX
{Style.RESET_ALL}"""
    print(banner)

class RAJA_Report(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'vErtex: REPORT DE AUDITORIA INTEGRAL', 0, 1, 'C')
        self.ln(5)

class vErtexEngine:
    def __init__(self, target):
        self.target = target.replace("https://", "").replace("http://", "").strip("/")
        self.results = []
        self.pdf = RAJA_Report()
        self.screenshot_path = None
        self.target_ip = None
        self.scan_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def log(self, text, status="info"):
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.results.append((status, text))
        color = Fore.GREEN if status == "success" else Fore.RED if status == "error" else Fore.BLUE
        symbol = "[✓]" if status == "success" else "[✗]" if status == "error" else "[*]"
        print(color + f" [{timestamp}]{symbol} {text}")

    # 1. MÓDULO RED (DNS & PORTS)
    def network_recon(self):
        self.log("--- FASE 1: RECONOCIMIENTO DE RED ---")
        try:
            self.target_ip = socket.gethostbyname(self.target)
            self.log(f"IP Objetivo: {self.target_ip}", "success")
            
            # DNS
            answers = dns.resolver.resolve(self.target, 'A')
            for rdata in answers: self.log(f"Registro DNS A: {rdata}", "success")
            
            # Escaneo rápido de puertos críticos
            ports = [21, 22, 80, 443, 3306, 8080]
            for port in ports:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.3)
                if s.connect_ex((self.target_ip, port)) == 0:
                    self.log(f"Puerto Abierto: {port}", "success")
                s.close()
        except: self.log("Error en fase de red", "error")

    # 2. MÓDULO GEOPOSICIÓN
    def get_geo(self):
        self.log("--- FASE 2: GEOLOCALIZACION ---")
        try:
            data = requests.get(f"http://ip-api.com/json/{self.target_ip}", timeout=5).json()
            if data.get('status') == 'success':
                info = f"Ubicacion: {data['city']}, {data['country']} | ISP: {data['isp']}"
                self.log(info, "success")
        except: self.log("Error al rastrear ubicación", "error")

    # 3. MÓDULO FORENSE (SSL & HEADERS)
    def forensics(self):
        self.log("--- FASE 3: ANALISIS FORENSE ---")
        # SSL
        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.target, 443), timeout=3) as sock:
                with context.wrap_socket(sock, server_hostname=self.target) as ssock:
                    cert = ssock.getpeercert()
                    issuer = dict(x[0] for x in cert['issuer'])
                    self.log(f"Certificado emitido por: {issuer.get('organizationName')}", "success")
        except: self.log("Sin SSL o certificado no válido", "error")
        
        # Headers & Tech
        try:
            res = requests.get(f"http://{self.target}", timeout=5, verify=False)
            server = res.headers.get('Server', 'Oculto')
            self.log(f"Web Server: {server}", "success")
            if 'wp-content' in res.text: self.log("CMS: WordPress detectado", "success")
        except: self.log("Error en fingerprinting", "error")

    # 4. MÓDULO VISUAL (SCREENSHOT)
    def visual_capture(self):
        self.log("--- FASE 4: CAPTURA VISUAL ---")
        from selenium import webdriver
        from selenium.webdriver.firefox.options import Options
        import time
        options = Options()
        options.add_argument("--headless")
        options.set_preference("accept_insecure_certs", True)
        try:
            driver = webdriver.Firefox(options=options)
            driver.get(f"http://{self.target}")
            time.sleep(4)
            path = f"evidencia_{self.target.replace('.', '_')}.png"
            driver.save_screenshot(path)
            self.screenshot_path = path
            driver.quit()
            self.log("Captura visual completada", "success")
        except: self.log("Error en captura visual", "error")

    def generate_pdf(self):
        self.pdf.add_page()
        self.pdf.set_font("Arial", 'B', 12)
        self.pdf.cell(0, 10, f"vErtex Report - {self.scan_time}", ln=True)
        self.pdf.cell(0, 10, f"TARGET: {self.target}", ln=True)
        self.pdf.ln(5)
        
        if self.screenshot_path and os.path.exists(self.screenshot_path):
            self.pdf.image(self.screenshot_path, x=10, w=180)
            self.pdf.ln(115)

        self.pdf.set_font("Arial", size=9)
        for status, text in self.results:
            try:
                clean_text = text.encode('latin-1', 'ignore').decode('latin-1')
                self.pdf.multi_cell(0, 6, f"[{status.upper()}] {clean_text}")
            except: continue

        name = f"Reporte_Completo_{self.target.replace('.', '_')}.pdf"
        self.pdf.output(name)
        print(Fore.YELLOW + f"\n[+] Auditoria finalizada. Reporte: {name}")

def main():
    show_banner()
    t = input(Fore.YELLOW + "🎯 Ingrese URL (ej: google.com): ")
    if not t: return

    v = vErtexEngine(t)
    v.network_recon()   # Red y Puertos
    v.get_geo()         # Geo
    v.forensics()       # SSL y Huellas
    v.visual_capture()  # Foto
    v.generate_pdf()    # Reporte Final

if __name__ == "__main__":
    main()
