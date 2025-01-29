from datetime import datetime
from database.vector_store import VectorStore
from services.synthesizer import Synthesizer
from timescale_vector import client

# Initialize VectorStore
vec = VectorStore()

# --------------------------------------------------------------
# 
# --------------------------------------------------------------

relevant_question = "Highly motivated and detail-oriented PHP Developer with 1 year of experience in software development, looking to leverage my skills in PHP, WordPress, HTML, CSS, and jQuery to design and develop scalable and responsive web applications. Proficient in working with teams to deliver high-quality projects and committed to staying up-to-date with emerging trends and technologies in web development."
results = vec.search(relevant_question, limit=3)

response = Synthesizer.generate_response(question=relevant_question, context=results)

print(f"\n{response.answer}")
print("\nThought process:")
for thought in response.thought_process:
    print(f"- {thought}")
print(f"\nContext: {response.enough_context}")

# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas

# # Replace this with your actual response.answer text
# response_answer = response.answer

# # Specify the output PDF file name
# output_pdf = "response_answer.pdf"

# # Create a canvas for the PDF
# pdf = canvas.Canvas(output_pdf, pagesize=letter)
# width, height = letter

# # Add the text to the PDF
# text_object = pdf.beginText(40, height - 40)  # Start 40 units from the top-left margin
# text_object.setFont("Times-Roman", 12)       # Set the font and size

# # Split the text into lines to fit the page
# lines = response_answer.split("\n")  # Split by line breaks
# for line in lines:
#     text_object.textLine(line)

# pdf.drawText(text_object)
# pdf.save()
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

# The string to be printed to the PDF
response_answer = response.answer

# Function to convert the string to a list of Paragraph objects
def convert_to_paragraphs(text):
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    bold_style = styles['Heading1']

    lines = text.split('\n')
    paragraphs = []

    for line in lines:
        if line.startswith('**') and line.endswith('**'):
            # Bold text
            paragraphs.append(Paragraph(line.strip('**'), bold_style))
        elif line.startswith('- '):
            # Bullet points
            paragraphs.append(Paragraph(line, normal_style))
        else:
            # Normal text
            paragraphs.append(Paragraph(line, normal_style))

    return paragraphs

# Create a PDF document
pdf_filename = "suitability_report.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

# Convert the string to a list of Paragraph objects
paragraphs = convert_to_paragraphs(response_answer)

# Build the PDF
doc.build(paragraphs)

print(f"PDF generated: {pdf_filename}")








# --------------------------------------------------------------
# Irrelevant question
# --------------------------------------------------------------

# irrelevant_question = "What is the weather in Tokyo?"

# results = vec.search(irrelevant_question, limit=3)

# response = Synthesizer.generate_response(question=irrelevant_question, context=results)

# print(f"\n{response.answer}")
# print("\nThought process:")
# for thought in response.thought_process:
#     print(f"- {thought}")
# print(f"\nContext: {response.enough_context}")

# --------------------------------------------------------------
# Metadata filtering
# --------------------------------------------------------------

# metadata_filter = {"Category": "PHP Developer"}

# results = vec.search(relevant_question, limit=3, metadata_filter=metadata_filter)

# response = Synthesizer.generate_response(question=relevant_question, context=results)

# print(f"\n{response.answer}")
# print("\nThought process:")
# for thought in response.thought_process:
#     print(f"- {thought}")
# print(f"\nContext: {response.enough_context}")

# --------------------------------------------------------------
# Advanced filtering using Predicates
# --------------------------------------------------------------

# predicates = client.Predicates("category", "==", "Shipping")
# results = vec.search(relevant_question, limit=3, predicates=predicates)


# predicates = client.Predicates("category", "==", "Shipping") | client.Predicates(
#     "category", "==", "Services"
# )
# results = vec.search(relevant_question, limit=3, predicates=predicates)


# predicates = client.Predicates("category", "==", "Shipping") & client.Predicates(
#     "created_at", ">", "2024-09-01"
# )
# results = vec.search(relevant_question, limit=3, predicates=predicates)

# # --------------------------------------------------------------
# # Time-based filtering
# # --------------------------------------------------------------

# # September — Returning results
# time_range = (datetime(2024, 9, 1), datetime(2024, 9, 30))
# results = vec.search(relevant_question, limit=3, time_range=time_range)

# # August — Not returning any results
# time_range = (datetime(2024, 8, 1), datetime(2024, 8, 30))
# results = vec.search(relevant_question, limit=3, time_range=time_range)

