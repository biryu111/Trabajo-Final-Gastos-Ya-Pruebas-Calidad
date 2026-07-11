from locust import HttpUser, task, between

class UsuarioGastos(HttpUser):
    wait_time = between(1, 2)
    token = None

    def on_start(self):
        response = self.client.post("/auth/login", json={
            "correo": "prueba@gastosya.com",
            "password": "prueba123"
        })
        if response.status_code == 200:
            self.token = response.json().get("token")

    def get_headers(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    @task(3)
    def registrar_gasto(self):
        self.client.post("/gastos/", json={
            "descripcion": "Gasto de prueba",
            "monto": 10.0,
            "categoria": "otro"
        }, headers=self.get_headers())

    @task(2)
    def listar_gastos(self):
        self.client.get("/gastos/", headers=self.get_headers())

    @task(1)
    def obtener_total(self):
        self.client.get("/gastos/total", headers=self.get_headers())

    @task(1)
    def ver_categorias(self):
        self.client.get("/gastos/categorias", headers=self.get_headers())
