import requests
import json

class OllamaService:
    def __init__(self):
        self.base_url = "http://localhost:11434/api/generate"
        self.model = "llama3.2:1b"
    
    def get_educational_recommendation(self, project_context, limitations, user_question):
        try:
            prompt = f"""
            Eres un asistente educativo especializado en adaptar proyectos para docentes.
            
            PROYECTO ACTUAL:
            {project_context}
            
            LIMITACIONES DEL DOCENTE:
            {limitations}
            
            PREGUNTA DEL DOCENTE:
            {user_question}
            
            Proporciona recomendaciones PRACTICAS para adaptar este proyecto considerando:
            - Las limitaciones especificas mencionadas
            - Estrategias realistas para el aula
            - Recursos accesibles y de bajo costo
            - Temporizacion realista
            
            Responde de forma CONCRETA y UTIL, enfocandote en soluciones aplicables inmediatamente.
            """
            
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            }
            
            response = requests.post(self.base_url, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'No pude generar una respuesta en este momento.')
            else:
                return f"Error conectando con Ollama: {response.status_code}"
                
        except Exception as e:
            return f"Error: {str(e)}. Asegurate de que Ollama este ejecutandose."

# Respaldo de caida
class FallbackService:
    def get_educational_recommendation(self, project_context, limitations, user_question):
        recommendations = [
            "Sugiero dividir el proyecto en fases mas pequenas y manejables.",
            "Considera usar materiales reciclados o de bajo costo para las actividades.",
            "Adapta el tiempo segun tus limitaciones - enfocate en lo esencial primero.",
            "Puedes usar ejemplos concretos de la vida real para hacerlo mas accesible.",
            "Divide a los estudiantes en grupos para optimizar recursos y tiempo.",
            "Usa tecnologia basica como presentaciones simples o videos cortos.",
            "Enfocate en los objetivos de aprendizaje principales primero.",
            "Considera evaluacion formativa continua en lugar de solo examenes finales."
        ]
        
        import random
        base_response = f"""Basado en tu proyecto '{project_context[:50]}...' y tus limitaciones:

{random.choice(recommendations)}

Recomendacion adicional: {random.choice(recommendations)}

Puedes implementar esto gradualmente comenzando la proxima semana."""
        
        return base_response