import requests, os, urllib3, socket, ssl
import dns.resolver
from colorama import Fore, Style, init
from fpdf import FPDF
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

def show_banner():
    os.system('clear')
    print(f"""{Fore.CYAN}{Style.BRIGHT}
    ██╗   ██╗███████╗██████╗ ████████╗███████╗██╗  ██╗
    ██║   ██║██╔════╝██╔══██╗╚══██╔══╝██╔════╝╚██╗██╔╝
    ██║   ██║█████╗  ██████╔╝   ██║   █████╗   ╚███╔╝ 
    ╚██╗ ██╔╝██╔══╝  ██╔══██╗   ██║   ██╔══╝   ██╔██╗ 
     ╚████╔╝ ███████╗██║  ██║   ██║   ███████╗██╔╝ ██╗
      ╚═══╝  ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝ v4.0
    {Fore.WHITE}The Ultimate Security Suite | {Fore.RED}Author: albertChOXrX
    """)

class UltraReport(FPDF):
    def header(self):
        # Banner superior profesional
        self.set_fill_color(15, 25, 35)
        self.rect(0, 0, 210, 35, 'F')
        self.set_font('Arial', 'B', 22)
        self.set_text_color(255, 255, 255)
        self.cell(0, 15, 'vErtex | ADVANCED INTELLIGENCE', 0, 1, 'L')
        self.set_font('Arial', '', 9)
        self.cell(0, 5, f'Audit ID: {datetime.now().strftime("%Y%m%d%H%M")}', 0, 0, 'L')
        self.cell(0, 5, f'Fecha: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  ', 0, 1, 'R')
        self.ln(12)

    def draw_section(self, title):
        self.ln(5)
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(240, 240, 240)
        self.set_text_color(15, 25, 35)
        self.cell(0, 10, f"  {title.upper()}", 0, 1, 'L', True)
        self.ln(3)

class vErtexEngine:
    def __init__(self, target):
        self.target = target.replace("https://", "").replace("http://", "").strip("/")
        self.results = []
        self.pdf = UltraReport()
        self.screenshot_path = None
        self.target_ip = "N/A"

    def log(self, cat, msg, level="INFO"):
        self.results.append({"cat": cat, "msg": msg, "level": level})
        color = Fore.RED if level == "CRITICAL" else Fore.YELLOW if level == "MEDIUM" else Fore.GREEN
        print(f"{color}[*] {cat}: {msg}")

    def run_all(self):
        # 1. INFRAESTRUCTURA (DNS & IP)
        try:
            self.target_ip = socket.gethostbyname(self.target)
            self.log("NETWORK", f"IP Address: {self.target_ip}", "SUCCESS")
            answers = dns.resolver.resolve(self.target, 'A')
            for rdata in answers: self.log("DNS", f"A Record found: {rdata}", "SUCCESS")
        except: self.log("NETWORK", "Failed DNS Resolution", "CRITICAL")

        # 2. GEOLOCALIZACION (De la v3.2)
        try:
            data = requests.get(f"http://ip-api.com/json/{self.target_ip}", timeout=5).json()
            if data['status'] == 'success':
                self.log("GEO", f"Country: {data['country']} ({data['city']})", "SUCCESS")
                self.log("GEO", f"ISP: {data['isp']} | Org: {data.get('org')}", "INFO")
        except: self.log("GEO", "Geolocation service unavailable", "MEDIUM")

        # 3. ESCANEO DE PUERTOS (NMAP Style)
        ports = {21: "FTP", 22: "SSH", 80: "HTTP", 443: "HTTPS", 3306: "MySQL", 8080: "HTTP-ALT"}
        for port, service in ports.items():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.4)
            if s.connect_ex((self.target_ip, port)) == 0:
                self.log("PORT", f"Service {service} is OPEN on port {port}", "MEDIUM")
            s.close()

        # 4. FORENSE & VULNERABILIDADES
        try:
            res = requests.get(f"https://{self.target}", timeout=5, verify=False)
            h = res.headers
            self.log("FORENSIC", f"Server Banner: {h.get('Server', 'Hidden')}", "SUCCESS")
            if 'X-Frame-Options' not in h: self.log("VULN", "Clickjacking Vulnerability (No X-Frame)", "MEDIUM")
            if 'Content-Security-Policy' not in h: self.log("VULN", "XSS Vulnerability (No CSP)", "CRITICAL")
            
            # Analisis SSL
            ctx = ssl.create_default_context()
            with socket.create_connection((self.target, 443), timeout=3) as sock:
                with ctx.wrap_socket(sock, server_hostname=self.target) as ssock:
                    cert = ssock.getpeercert()
                    issuer = dict(x[0] for x in cert['issuer'])
                    self.log("SSL", f"Certificate Issued by: {issuer.get('organizationName')}", "SUCCESS")
        except: pass

        # 5. CAPTURA VISUAL
        from selenium import webdriver
        from selenium.webdriver.firefox.options import Options
        import time
        options = Options()
        options.add_argument("--headless")
        try:
            dr = webdriver.Firefox(options=options)
            dr.get(f"http://{self.target}")
            time.sleep(3)
            self.screenshot_path = f"ev_{self.target.replace('.','_')}.png"
            dr.save_screenshot(self.screenshot_path)
            dr.quit()
        except: self.log("VISUAL", "Screenshot capture failed", "MEDIUM")

    def generate_pdf(self):
        self.pdf.add_page()
        
        # Resumen Ejecutivo
        self.pdf.set_fill_color(30, 40, 50)
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.set_font("Arial", 'B', 12)
        self.pdf.cell(190, 12, f"  TARGET: {self.target} | IP: {self.target_ip}", 0, 1, 'L', True)
        self.pdf.set_text_color(0)

        # Evidencia Visual
        self.pdf.draw_section("Digital Evidence (Screenshot)")
        if self.screenshot_path:
            self.pdf.image(self.screenshot_path, x=15, w=180, h=95)
            self.pdf.ln(100)

        # Tabla de Hallazgos Integrada
        self.pdf.draw_section("Technical Findings & Vulnerability Matrix")
        self.pdf.set_font("Arial", 'B', 10)
        self.pdf.set_fill_color(220, 225, 230)
        self.pdf.cell(35, 8, " CATEGORY", 1, 0, 'L', True)
        self.pdf.cell(120, 8, " FINDING", 1, 0, 'L', True)
        self.pdf.cell(35, 8, " SEVERITY", 1, 1, 'L', True)

        self.pdf.set_font("Arial", '', 9)
        for r in self.results:
            # Color de texto basado en severidad
            if r['level'] == "CRITICAL": self.pdf.set_text_color(200, 0, 0)
            elif r['level'] == "MEDIUM": self.pdf.set_text_color(200, 140, 0)
            elif r['level'] == "SUCCESS": self.pdf.set_text_color(0, 120, 0)
            else: self.pdf.set_text_color(0, 0, 0)

            self.pdf.cell(35, 7, f" {r['cat']}", 1, 0)
            self.pdf.cell(120, 7, f" {r['msg'][:70]}", 1, 0)
            self.pdf.cell(35, 7, f" {r['level']}", 1, 1)
            self.pdf.set_text_color(0)

        name = f"vErtex_ULTIMATE_{self.target.replace('.','_')}.pdf"
        self.pdf.output(name)
        print(f"\n{Fore.CYAN}[+] vErtex v4.0: Reporte definitivo generado: {name}")

def main():
    show_banner()
    t = input(f"{Fore.YELLOW}🎯 Enter Target URL: ")
    if not t: return
    v = vErtexEngine(t)
    v.run_all()
    v.generate_pdf()

if __name__ == "__main__":
    main()
