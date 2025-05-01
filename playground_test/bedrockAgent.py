import os
import boto3
from claudeAgent import Agent
from dotenv import load_dotenv
import json
import logging

# Cargar variables de entorno
load_dotenv()

class BedRockAgent(Agent):
    def __init__(self, model_id=None, inference_profile_arn=None):
        super().__init__()
        
        # Configurar cliente de Bedrock usando variables de entorno
        self.bedrock = boto3.client(
            'bedrock-runtime',
            region_name=os.getenv("AWS_REGION", "us-east-2"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
        self.name = "BedRockAgent"
        self.model_id = model_id
        self.inference_profile_arn = inference_profile_arn
        logging.info(f"BedRockAgent inicializado con modelo: {model_id or inference_profile_arn}")
    
    def process_message(self, message, system_prompt=None):
        """
        Procesa un mensaje usando el modelo de AWS Bedrock
        
        Args:
            message (str): El mensaje del usuario para procesar
            system_prompt (str, optional): Un prompt de sistema para contextualizar
            
        Returns:
            str: Respuesta generada por el modelo
        """
        
        try:
            # Determinar si es un modelo Claude 3.x (usa formato messages)
            is_claude3_model = any(x in (self.model_id or "") for x in ["claude-3", "claude-3-5", "claude-3-7"])
            
            # Para modelos Claude 3.x (usan formato messages)
            if is_claude3_model:
                messages = [{"role": "user", "content": message}]
                
                # Añadir mensaje del sistema si está disponible
                if system_prompt:
                    messages.insert(0, {"role": "user", "content": system_prompt})
                
                request_body = {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 4000,
                    "temperature": 0.7,
                    "messages": messages
                }
                
                # Determinar si usar ARN de perfil o model_id directamente
                actual_model_id = self.inference_profile_arn or self.model_id
                
                response = self.bedrock.invoke_model(
                    modelId=actual_model_id,
                    body=json.dumps(request_body)
                )
                
                response_body = json.loads(response["body"].read())
                return response_body["content"][0]["text"]
            
            
            # Para modelos antiguos de Anthropic (Claude 1 y 2)
            elif "anthropic" in (self.model_id or "").lower() and not is_claude3_model:
                prompt = f"Human: {message}\n\nAssistant:"
                if system_prompt:
                    prompt = f"Human: <system>{system_prompt}</system>\n\n{message}\n\nAssistant:"
                
                response = self.bedrock.invoke_model(
                    modelId=self.model_id,
                    body=json.dumps({
                        "prompt": prompt,
                        "max_tokens_to_sample": 2000,
                        "temperature": 0.7,
                    })
                )
                response_body = json.loads(response["body"].read())
                return response_body["completion"]
            
            # Para otros modelos de Amazon
            elif "amazon" in (self.model_id or "").lower():
                response = self.bedrock.invoke_model(
                    modelId=self.model_id,
                    body=json.dumps({
                        "inputText": message,
                        "textGenerationConfig": {
                            "maxTokenCount": 2000,
                            "temperature": 0.7,
                        }
                    })
                )
                response_body = json.loads(response["body"].read())
                return response_body["results"][0]["outputText"]
            
            # Configuración genérica
            else:
                response = self.bedrock.invoke_model(
                    modelId=self.model_id or "",
                    body=json.dumps({"prompt": message})
                )
                return json.loads(response["body"].read())
                
        except Exception as e:
            import traceback
            logging.error(f"Error en process_message: {str(e)}\n{traceback.format_exc()}")
            return f"Error al invocar el modelo: {str(e)}\n\n{traceback.format_exc()}"
    
    def run(self, user_input, system_prompt=None):
        """
        Ejecuta el agente con la entrada del usuario
        
        Args:
            user_input (str): Entrada del usuario
            system_prompt (str, optional): Prompt del sistema
            
        Returns:
            str: Respuesta generada por el modelo
        """
        return self.process_message(user_input, system_prompt)
    
    # Alias para mantener compatibilidad con otras interfaces
    def query(self, prompt, system_prompt=None):
        """Alias de run() para mantener compatibilidad"""
        return self.run(prompt, system_prompt)