from bs4 import BeautifulSoup
import  requests
import httpx

class Servers():
    def __init__(self):
        self.URL = "https://minecraftrating.ru/"
        self.URL_status = "https://api.mcsrvstat.us/3/"

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        }

    def get_servers(self, search: str | None = None, page: int = 1, version: str | None = None) -> list:
        try:
            if search is None:
                if version is None:
                    response = requests.get(url=self.URL + f"page/{page}/", headers=self.headers)
                else :
                    response = requests.get(url=self.URL + f"servera-{version}/page/{page}/", headers=self.headers)
            else :
                response = requests.get(url=self.URL + f"search/{search}/", headers=self.headers)

            bs = BeautifulSoup(response.text, "html.parser")
            ips = bs.find_all("var", class_="tooltip")

            result = []

            status_code = response.status_code
            print(status_code)

            for i in ips:
                result.append(i.get("data-clipboard-text"))

            if status_code == 200:
                return result
            else :
                return "none"
        except Exception:
            return "none"
    
    async def get_status_server(self, ip: str) -> dict:
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url=self.URL_status + ip, headers=self.headers)
        status_code = response.status_code
        print(status_code)

        status: dict = response.json()

        result = {
            "ip": ip,
            "name": status["motd"]["clean"][0].strip() if status.get("motd") and "clean" in status["motd"] else ip,
            "online": status["players"]["online"] if status.get("players") and "online" in status["players"] else "none",
            "max_online": status["players"]["max"] if status.get("players") and "max" in status["players"] else "none",
            "version": status["protocol"]["name"] if status.get("protocol") and "name" in status["protocol"] else "none",
            "icon": status["icon"] if status.get("icon") else "none"
        }

        return result if status_code == 200 else "none"






if __name__ == "__main__":
    ser = Servers()
    
    print(ser.get_servers(page=1, version="1.21.10"))
    print(ser.get_status_server(ip="mr.aresmine.me"))