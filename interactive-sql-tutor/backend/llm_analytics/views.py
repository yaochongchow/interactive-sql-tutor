from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import openai
import os
from .permissions import IsAdminUserOrInstructor

openai.api_key = os.getenv("OPENAI_API_KEY")

@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdminUserOrInstructor])
def generate_read_query(request):
    prompt = request.data.get("prompt")

    if not prompt:
        return Response({"error": "Prompt is required."}, status=400)

    query = call_llm_for_read_query(prompt)
    return Response({"query": query})


def call_llm_for_read_query(prompt):
    schema_knowledge = """
You can only query the following Django models represented as SQL tables:

1. **User**
   - user_id (int)
   - name (str)
   - email (str)
   - role (enum('Student', 'Instructor', 'Admin'))
   - date_joined (datetime)

2. **SQLProblem**
   - problem_id (int)
   - title (str)
   - difficulty_level (str)
   - topic_id (int)

3. **Attempt**
   - attempt_id (int)
   - user_id (int) - ForeignKey to User
   - problem_id (int) - ForeignKey to SQLProblem
   - score (float)
   - status (str)
   - submission_date (datetime)
   - time_taken (float, in seconds)
   - hints_used (int)

4. **Topic**
- topic_id (VARCHAR)
- name 

Rules:
- Only generate SELECT queries using these fields and tables.
- Do NOT generate INSERT, UPDATE, DELETE, ALTER, or DDL statements.
- If asked for anything outside the schema, write operations, or not related to database management course design or SQL, reply with a warning.
- However, if the user is an **instructor** and asks for **help analyzing student performance, designing assignments, or getting insights about SQL/database course structure**, you may analyze based on the data, generate relevant queries, and suggest ideas for improvement.
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": schema_knowledge},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=200
    )
    return response.choices[0].message.content.strip()