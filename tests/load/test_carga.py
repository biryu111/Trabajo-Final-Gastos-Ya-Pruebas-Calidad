from locust import HttpUser, task, between

class UsuarioGastos(HttpUser):
    wait_time = between(1, 2)

    @task(3)
    def registrar_gasto(self):
        self.client.post("/gastos/", json={
            "descripcion": "Gasto de prueba",
            "monto": 10.0,
            "categoria": "otro"
        })

    @task(2)
    def listar_gastos(self):
        self.client.get("/gastos/")

    @task(1)
    def obtener_total(self):
        self.client.get("/gastos/total")
