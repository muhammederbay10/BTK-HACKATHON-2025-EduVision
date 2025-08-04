def build_classroom_prompt(students_data: list, class_info: dict, language: str = "en") -> str:
    """Build a comprehensive classroom attention analysis prompt."""

    # Language-specific instructions and headers
    language_config = {
        "english": {
            "instruction": "Please provide the report in English.",
            "headers": {
                "executive_summary": "EXECUTIVE SUMMARY",
                "individual_analysis": "INDIVIDUAL STUDENT ANALYSIS", 
                "temporal_analysis": "TEMPORAL ANALYSIS",
                "classroom_dynamics": "CLASSROOM DYNAMICS",
                "recommendations": "ACTIONABLE RECOMMENDATIONS",
                "metrics_summary": "METRICS SUMMARY"
            }
        },
        "turkish": {
            "instruction": "Lütfen raporu Türkçe olarak sağlayın. Türkçe eğitim terminolojisini kullanın.",
            "headers": {
                "executive_summary": "YÖNETİCİ ÖZETİ",
                "individual_analysis": "BİREYSEL ÖĞRENCİ ANALİZİ",
                "temporal_analysis": "ZAMANSAL ANALİZ", 
                "classroom_dynamics": "SINIF DİNAMİKLERİ",
                "recommendations": "UYGULANABİLİR ÖNERİLER",
                "metrics_summary": "METRİK ÖZETİ"
            }
        },
        "arabic": {
            "instruction": "يرجى تقديم التقرير باللغة العربية. استخدم المصطلحات التعليمية المناسبة باللغة العربية.",
            "headers": {
                "executive_summary": "الملخص التنفيذي",
                "individual_analysis": "تحليل الطلاب الفردي",
                "temporal_analysis": "التحليل الزمني",
                "classroom_dynamics": "ديناميكيات الفصل", 
                "recommendations": "التوصيات القابلة للتنفيذ",
                "metrics_summary": "ملخص المقاييس"
            }
        },
        "spanish": {
            "instruction": "Por favor, proporciona el informe en español. Utiliza terminología educativa apropiada en español.",
            "headers": {
                "executive_summary": "RESUMEN EJECUTIVO",
                "individual_analysis": "ANÁLISIS INDIVIDUAL DE ESTUDIANTES",
                "temporal_analysis": "ANÁLISIS TEMPORAL",
                "classroom_dynamics": "DINÁMICAS DEL AULA",
                "recommendations": "RECOMENDACIONES ACCIONABLES", 
                "metrics_summary": "RESUMEN DE MÉTRICAS"
            }
        },
        "french": {
            "instruction": "Veuillez fournir le rapport en français. Utilisez la terminologie éducative appropriée en français.",
            "headers": {
                "executive_summary": "RÉSUMÉ EXÉCUTIF",
                "individual_analysis": "ANALYSE INDIVIDUELLE DES ÉTUDIANTS",
                "temporal_analysis": "ANALYSE TEMPORELLE",
                "classroom_dynamics": "DYNAMIQUES DE CLASSE",
                "recommendations": "RECOMMANDATIONS PRATIQUES",
                "metrics_summary": "RÉSUMÉ DES MÉTRIQUES"
            }
        },
        "german": {
            "instruction": "Bitte erstellen Sie den Bericht auf Deutsch. Verwenden Sie angemessene deutsche Bildungsterminologie.",
            "headers": {
                "executive_summary": "ZUSAMMENFASSUNG",
                "individual_analysis": "INDIVIDUELLE STUDENTENANALYSE",
                "temporal_analysis": "ZEITANALYSE",
                "classroom_dynamics": "KLASSENDYNAMIK",
                "recommendations": "UMSETZBARE EMPFEHLUNGEN",
                "metrics_summary": "METRIKEN-ZUSAMMENFASSUNG"
            }
        },
        "italian": {
            "instruction": "Si prega di fornire il rapporto in italiano. Utilizzare la terminologia educativa appropriata in italiano.",
            "headers": {
                "executive_summary": "RIASSUNTO ESECUTIVO",
                "individual_analysis": "ANALISI INDIVIDUALE DEGLI STUDENTI",
                "temporal_analysis": "ANALISI TEMPORALE",
                "classroom_dynamics": "DINAMICHE DELLA CLASSE",
                "recommendations": "RACCOMANDAZIONI ATTUABILI",
                "metrics_summary": "RIASSUNTO DELLE METRICHE"
            }
        },
        "portuguese": {
            "instruction": "Por favor, forneça o relatório em português. Use terminologia educacional apropriada em português.",
            "headers": {
                "executive_summary": "RESUMO EXECUTIVO",
                "individual_analysis": "ANÁLISE INDIVIDUAL DE ESTUDANTES",
                "temporal_analysis": "ANÁLISE TEMPORAL",
                "classroom_dynamics": "DINÂMICAS DA SALA DE AULA",
                "recommendations": "RECOMENDAÇÕES ACIONÁVEIS",
                "metrics_summary": "RESUMO DAS MÉTRICAS"
            }
        },
        "chinese": {
            "instruction": "请用中文提供报告。请使用适当的中文教育术语。",
            "headers": {
                "executive_summary": "执行摘要",
                "individual_analysis": "个人学生分析",
                "temporal_analysis": "时间分析",
                "classroom_dynamics": "课堂动态",
                "recommendations": "可行建议",
                "metrics_summary": "指标摘要"
            }
        },
        "japanese": {
            "instruction": "日本語でレポートを提供してください。適切な日本語の教育用語を使用してください。",
            "headers": {
                "executive_summary": "エグゼクティブサマリー",
                "individual_analysis": "個別学生分析",
                "temporal_analysis": "時間分析",
                "classroom_dynamics": "教室の動態",
                "recommendations": "実行可能な推奨事項",
                "metrics_summary": "指標要約"
            }
        },
        "russian": {
            "instruction": "Пожалуйста, предоставьте отчет на русском языке. Используйте соответствующую русскую образовательную терминологию.",
            "headers": {
                "executive_summary": "РЕЗЮМЕ",
                "individual_analysis": "ИНДИВИДУАЛЬНЫЙ АНАЛИЗ СТУДЕНТОВ",
                "temporal_analysis": "ВРЕМЕННОЙ АНАЛИЗ",
                "classroom_dynamics": "КЛАССНАЯ ДИНАМИКА",
                "recommendations": "ПРАКТИЧЕСКИЕ РЕКОМЕНДАЦИИ",
                "metrics_summary": "СВОДКА ПОКАЗАТЕЛЕЙ"
            }
        }
    }

    # Get language config (default to English)
    lang_config = language_config.get(language.lower(), language_config["english"])
    language_instruction = lang_config["instruction"]
    headers = lang_config["headers"]

    prompt = f"""
You are an expert educational analyst specializing in classroom attention and engagement patterns. 
Analyze the following classroom session data and provide a comprehensive report.

IMPORTANT: {language_instruction}

CLASSROOM INFORMATION:
- Course: {class_info.get('course_name', 'Unknown')}
- Session Date: {class_info.get('date', 'Unknown')}
- Session Time: {class_info.get('session_time', 'Unknown')}
- Total Students: {len(students_data)}

STUDENT ATTENTION DATA (Aggregated in 3-minute intervals):
"""
    
    for i, student in enumerate(students_data, 1):
        prompt += f"""
STUDENT {i}:
- ID: {student['student_id']}
- Name: {student['name']}
- Total Session Duration: {student['total_session_minutes']} minutes
- Overall Attention Score: {student['overall_attention_score']}%
- Total Distractions: {student['total_distractions']}
- Intervals Analyzed: {student['intervals_analyzed']}

TIME INTERVAL BREAKDOWN:
"""
        for interval in student['time_intervals']:
            prompt += f"  • {interval['interval_start']} ({interval['interval_duration_minutes']}min): "
            prompt += f"{interval['interval_status']} - {interval['attention_rate']:.1f}% attention, "
            prompt += f"{interval['total_distractions']} distractions\n"
    
    # Dynamic section headers based on language
    prompt += f"""

ANALYSIS REQUIREMENTS:
You MUST use the exact headers shown below. Do not translate or modify them:

**1. {headers['executive_summary']}**
   - Overall classroom engagement level and key statistics
   - Most critical findings and immediate concerns
   - Session effectiveness assessment

**2. {headers['individual_analysis']}**
   - Detailed performance summary for each student
   - Attention progression patterns throughout the session
   - Individual strengths and areas for improvement
   - Students requiring immediate intervention or support

**3. {headers['temporal_analysis']}**
   - How attention levels evolved during the session timeline
   - Peak engagement periods and optimal learning windows
   - Attention decline patterns and timing
   - Interval-by-interval progression analysis
   - Consistency patterns across time periods

**4. {headers['classroom_dynamics']}**
   - Overall class engagement trends and collective behavior
   - Performance distribution and ranking insights
   - Comparison between high, average, and low performers
   - Class cohesion and group attention patterns
   - Peer influence on attention levels

**5. {headers['recommendations']}**
   - Specific, implementable strategies for improving engagement
   - Individual student intervention plans with priority levels
   - Optimal timing recommendations for different content types
   - Environmental modifications and teaching method adjustments
   - Follow-up monitoring suggestions

**6. {headers['metrics_summary']}**
   - Comprehensive statistical overview of class performance
   - Average class attention score and variance analysis
   - Distribution of student performance levels
   - Distraction frequency patterns and correlation analysis
   - Consistency scores and reliability metrics
   - Comparative benchmarks and improvement indicators

CRITICAL INSTRUCTIONS:
- You MUST start each section with the exact header shown above
- Use ** before and after each header exactly as shown
- Write all content in {language.title()}
- Use appropriate educational terminology for {language.title()}
- Do NOT translate the headers - use them exactly as provided
- Provide detailed analysis for each section

FORMATTING GUIDELINES:
- Structure content with clear bullet points and sub-sections
- Include specific data points and percentages where relevant
- Provide actionable insights rather than just observations
- Focus on educational outcomes and practical applications
- Maintain a professional tone suitable for educators and administrators
"""
    
    return prompt