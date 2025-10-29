from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import csv
import json
from .models import Project, Conversation
from .services import OllamaService, FallbackService
from io import StringIO
from datetime import datetime, timedelta
from .resource_generator import ResourceGenerator
from django.http import HttpResponse
from .models import Project, Conversation, GeneratedResource

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

class ResourceGenerator:
    def generate_lesson_plan_csv(self, project_context, limitations, activities):
        """Genera CSV con plan de clase detallado"""
        output = StringIO()
        writer = csv.writer(output)
        
        # Cabecera
        writer.writerow(['Plan de Clase Generado por IA', '', '', ''])
        writer.writerow(['Proyecto:', project_context[:50], 'Fecha:', datetime.now().strftime("%d/%m/%Y")])
        writer.writerow(['Limitaciones consideradas:', limitations[:100], '', ''])
        writer.writerow([])
        
        # Actividades
        writer.writerow(['SEMANA', 'DiA', 'ACTIVIDAD', 'MATERIALES', 'DURACIoN', 'EVALUACIoN', 'RECOMPENSA'])
        
        activities_list = activities.split('\n') if isinstance(activities, str) else activities
        day_counter = 1
        week_counter = 1
        
        for i, activity in enumerate(activities_list[:20]):  # Maximo 20 actividades
            if activity.strip():
                writer.writerow([
                    f"Semana {week_counter}",
                    f"Dia {day_counter}",
                    activity[:100],  # Truncar si es muy largo
                    "Material basico",
                    "45 min",
                    "Observacion directa",
                    f"{i*10} puntos"
                ])
                day_counter += 1
                if day_counter > 5:  # Nueva semana despues de 5 dias
                    day_counter = 1
                    week_counter += 1
        
        writer.writerow([])
        writer.writerow(['SISTEMA DE RECOMPENSAS', '', '', '', '', '', ''])
        writer.writerow(['PUNTOS', 'RECOMPENSA', 'CRITERIO', '', '', '', ''])
        writer.writerow(['50', 'Insignia digital', 'Completar primera actividad', '', '', '', ''])
        writer.writerow(['100', 'Elegir actividad', 'Completar semana 1', '', '', '', ''])
        writer.writerow(['200', 'Reconocimiento especial', 'Proyecto completo', '', '', '', ''])
        
        return output.getvalue()

    def generate_student_tracker_csv(self, student_names, activities):
        """Genera CSV para seguimiento de estudiantes"""
        output = StringIO()
        writer = csv.writer(output)
        
        # Cabecera
        writer.writerow(['SEGUIMIENTO DE ESTUDIANTES - SISTEMA GAMIFICADO'])
        writer.writerow([])
        
        # Encabezados de actividades
        activity_headers = ['ESTUDIANTE']
        activities_list = activities.split('\n')[:10] if isinstance(activities, str) else activities[:10]
        
        for i, activity in enumerate(activities_list):
            if activity.strip():
                activity_headers.append(f'Act.{i+1}')
        
        activity_headers.extend(['PUNTOS TOTAL', 'NIVEL', 'RECOMPENSAS'])
        writer.writerow(activity_headers)
        
        # Datos de estudiantes (ejemplo)
        for student in student_names[:30]:  # Maximo 30 estudiantes
            row = [student]
            total_points = 0
            
            for i in range(len(activities_list)):
                if activities_list[i].strip():
                    points = "50" if i % 2 == 0 else "25"  # Ejemplo alternado
                    row.append(points)
                    total_points += int(points)
            
            # Calcular nivel y recompensas
            level = min((total_points // 100) + 1, 5)
            rewards = "Insignia" if total_points >= 50 else "En progreso"
            
            row.extend([str(total_points), f"Nivel {level}", rewards])
            writer.writerow(row)
        
        return output.getvalue()

    def generate_gamification_template_json(self, project_context, activities):
        """Genera plantilla de gamificacion en JSON"""
        template = {
            "proyecto": project_context[:100],
            "fecha_creacion": datetime.now().isoformat(),
            "sistema_gamificacion": {
                "niveles": [
                    {"nivel": 1, "puntos_requeridos": 0, "recompensa": "Insignia Iniciador"},
                    {"nivel": 2, "puntos_requeridos": 100, "recompensa": "Insignia Explorador"},
                    {"nivel": 3, "puntos_requeridos": 250, "recompensa": "Insignia Maestro"}
                ],
                "actividades": [],
                "recompensas_especiales": [
                    {"tipo": "virtual", "nombre": "Elegir proxima actividad", "costo_puntos": 150},
                    {"tipo": "reconocimiento", "nombre": "Mencion en clase", "costo_puntos": 200},
                    {"tipo": "privilegio", "nombre": "Ayudante del dia", "costo_puntos": 100}
                ]
            },
            "evaluacion": {
                "criterios": [
                    {"criterio": "Participacion", "peso": 0.3},
                    {"criterio": "Creatividad", "peso": 0.4},
                    {"criterio": "Colaboracion", "peso": 0.3}
                ],
                "escala_puntos": "0-50 por actividad"
            }
        }
        
        # Agregar actividades
        activities_list = activities.split('\n') if isinstance(activities, str) else activities
        for i, activity in enumerate(activities_list[:15]):
            if activity.strip():
                template["sistema_gamificacion"]["actividades"].append({
                    "id": i + 1,
                    "nombre": activity[:80],
                    "puntos_base": 50,
                    "bonus_posible": 25,
                    "materiales": "Adaptar segun disponibilidad",
                    "duracion_estimada": "45 minutos"
                })
        
        return json.dumps(template, indent=2, ensure_ascii=False)




@csrf_exempt
def generate_lesson_plan(request, project_id):
    """Generar plan de clase en CSV"""
    project = get_object_or_404(Project, id=project_id)
    
    recent_conversations = Conversation.objects.filter(project=project).order_by('-created_at')[:5]
    activities_text = "\n".join([conv.user_message for conv in recent_conversations if "actividad" in conv.user_message.lower()])
    
    generator = ResourceGenerator()
    csv_content = generator.generate_lesson_plan_csv(
        project.context,
        project.limitations,
        activities_text or "Actividades personalizadas segun el proyecto"
    )
    
    response = HttpResponse(csv_content, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="plan_clase_{project.name}.csv"'
    
    # Guardar en base de datos
    GeneratedResource.objects.create(
        project=project,
        resource_type='csv',
        title=f"Plan de Clase - {project.name}",
        description="CSV con planificacion detallada de actividades",
        file_content=csv_content
    )
    
    return response

@csrf_exempt
def generate_student_tracker(request, project_id):
    """Generar tracker de estudiantes en CSV"""
    project = get_object_or_404(Project, id=project_id)
    
    # Estudiantes de ejemplo
    student_names = [
        "Ana Garcia", "Carlos Lopez", "Maria Rodriguez", "Jose Martinez", 
        "Laura Hernandez", "Miguel Gonzalez", "Elena Perez", "David Sanchez"
    ]
    
    # Obtener actividades
    activities = Conversation.objects.filter(project=project).values_list('user_message', flat=True)[:10]
    
    generator = ResourceGenerator()
    csv_content = generator.generate_student_tracker_csv(student_names, list(activities))
    
    response = HttpResponse(csv_content, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="seguimiento_estudiantes_{project.name}.csv"'
    
    GeneratedResource.objects.create(
        project=project,
        resource_type='csv',
        title=f"Seguimiento Estudiantes - {project.name}",
        description="CSV para tracking de progreso estudiantil",
        file_content=csv_content
    )
    
    return response

@csrf_exempt
def generate_gamification_template(request, project_id):
    """Generar plantilla de gamificacipn en JSON"""
    project = get_object_or_404(Project, id=project_id)
    
    activities = Conversation.objects.filter(project=project).values_list('user_message', flat=True)[:15]
    
    generator = ResourceGenerator()
    json_content = generator.generate_gamification_template_json(project.context, list(activities))
    
    response = HttpResponse(json_content, content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="gamificacion_{project.name}.json"'
    
    GeneratedResource.objects.create(
        project=project,
        resource_type='json',
        title=f"Plantilla Gamificacion 11 {project.name}",
        description="JSON con estructura de gamificacion",
        file_content=json_content
    )
    
    return response

def resources_dashboard(request, project_id):
    """Dashboard de recursos generados"""
    project = get_object_or_404(Project, id=project_id)
    resources = GeneratedResource.objects.filter(project=project).order_by('-created_at')
    
    return render(request, 'chatbot/resources.html', {
        'project': project,
        'resources': resources
    })