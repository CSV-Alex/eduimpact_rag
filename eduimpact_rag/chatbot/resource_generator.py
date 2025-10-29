import csv
import json
from io import StringIO
from datetime import datetime, timedelta

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
        writer.writerow(['SEMANA', 'DIA', 'ACTIVIDAD', 'MATERIALES', 'DURACION', 'EVALUACION', 'RECOMPENSA'])
        
        activities_list = activities.split('\n') if isinstance(activities, str) else activities
        day_counter = 1
        week_counter = 1
        
        for i, activity in enumerate(activities_list[:20]):
            if activity.strip():
                writer.writerow([
                    f"Semana {week_counter}",
                    f"Dia {day_counter}",
                    activity[:100],
                    "Material basico",
                    "45 min",
                    "Observacion directa",
                    f"{i*10} puntos"
                ])
                day_counter += 1
                if day_counter > 5:
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
        writer.writerow(['SEGUIMIENTO DE ESTUDIANTES 11 SISTEMA GAMIFICADO'])
        writer.writerow([])
        
        # Encabezados de actividades
        activity_headers = ['ESTUDIANTE']
        activities_list = activities.split('\n')[:10] if isinstance(activities, str) else activities[:10]
        
        for i, activity in enumerate(activities_list):
            if activity.strip():
                activity_headers.append(f'Act.{i+1}')
        
        activity_headers.extend(['PUNTOS TOTAL', 'NIVEL', 'RECOMPENSAS'])
        writer.writerow(activity_headers)
        
        # Datos de estudiantes
        for student in student_names[:30]:
            row = [student]
            total_points = 0
            
            for i in range(len(activities_list)):
                if activities_list[i].strip():
                    points = "50" if i % 2 == 0 else "25"
                    row.append(points)
                    total_points += int(points)
            
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