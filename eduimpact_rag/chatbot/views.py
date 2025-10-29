from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Project, Conversation
from .services import OllamaService, FallbackService

def home(request):
    """Pagina principal para crear nuevo proyecto"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        context = request.POST.get('context')
        limitations = request.POST.get('limitations')
        
        if name and context:
            project = Project.objects.create(
                name=name,
                description=description,
                context=context,
                limitations=limitations
            )
            return redirect('chat_interface', project_id=project.id)
    
    return render(request, 'chatbot/home.html')

def project_list(request):
    """Lista de proyectos existentes"""
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'chatbot/project_list.html', {'projects': projects})

def chat_interface(request, project_id):
    """Interfaz de chat con el asistente"""
    project = get_object_or_404(Project, id=project_id)
    conversations = Conversation.objects.filter(project=project)
    return render(request, 'chatbot/chat.html', {
        'project': project,
        'conversations': conversations
    })

@csrf_exempt
def chat_message(request, project_id):
    """Procesar mensajes del chat"""
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        data = json.loads(request.body)
        user_message = data.get('message', '')
        
        # Intentar con Ollama primero, luego fallback
        try:
            ai_service = OllamaService()
            response = ai_service.get_educational_recommendation(
                project.context,
                project.limitations,
                user_message
            )
        except:
            fallback_service = FallbackService()
            response = fallback_service.get_educational_recommendation(
                project.context,
                project.limitations,
                user_message
            )
        
        # Guardar en la base de datos
        conversation = Conversation.objects.create(
            project=project,
            user_message=user_message,
            ai_response=response
        )
        
        return JsonResponse({
            'success': True,
            'response': response,
            'timestamp': conversation.created_at.strftime("%H:%M")
        })

@csrf_exempt
def delete_project(request, project_id):
    """Eliminar proyecto"""
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        project.delete()
        return JsonResponse({'success': True})