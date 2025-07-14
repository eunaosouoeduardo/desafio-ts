from locust import HttpUser, task, between, constant
from locust.exception import StopUser

class ConsolidadoAPI(HttpUser):
    wait_time = between(0, 0)
    count = 0

    @task
    def post_lancamento(self):
        # Simula inserção de um novo lançamento
        self.client.post("/lancamentos", json={"data": "2025-07-19", "valor": 100.0, "tipo": "CREDITO", "descricao": "Lançamento de crédito"})
        self.count += 1
        if self.count >=100:
            raise StopUser()
    #locust -f meu_arquivo.py --headless -u 1 -r 1 --host http://localhost:8000
