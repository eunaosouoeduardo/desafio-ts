from locust import HttpUser, task, between, constant

class ConsolidadoAPI(HttpUser):
    #wait_time = between(1, 2)
    wait_time = constant(0)

    @task
    def get_consolidado(self):
        # Simula consulta de um consolidado especifico
        self.client.get("/consolidado/2025-07-19")

    # @task
    # def post_lancamento(self):
    #     # Simula inserção de um novo lançamento
    #     self.client.post("/lancamentos", json={"data": "2025-01-01", "valor": 100.0, "tipo": "CREDITO", "descricao": "Lançamento de crédito"})